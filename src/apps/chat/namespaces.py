import socketio

from src.apps.chat.models import Chat
from src.apps.chat.services import ChatService


class ChatMainNamespace(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        session_data = {'user': await ChatService.get_request_user(environ)}
        session_data.update({'chat_id': environ.get('HTTP_CHAT')})
        chat = await ChatService.get_chat_by_id(session_data['chat_id'])
        if not chat:
            await self.disconnect(sid)

        existing = await ChatService.check_existing_user_in_chat(
            chat=chat,
            user_id=session_data['user']['id']
        )
        if not existing:
            await self.disconnect(sid)

        self.enter_room(sid=sid, room=str(session_data['chat_id']))
        await self.save_session(sid, session_data)

    async def on_message(self, sid, msg):
        session_data = await self.get_session(sid)
        message = await ChatService.message_create(
            msg=msg,
            user_id=session_data['user']['id'],
            chat_id=session_data['chat_id'],
        )
        parsed_message = ChatService.parse_message(
            message,
            user_id=session_data['user']['id'],
            username=session_data['user']['username'],
        )
        await self.emit(event='message', data=parsed_message, room=session_data['chat_id'])
        await self.emit(
            event='message',
            data=parsed_message,
            room=session_data['chat_id'],
            namespace='/notification',
            skip_sid=sid
        )

    async def on_disconnect(self, sid):
        await self.disconnect(sid)


class ChatNotificationNamespace(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        session_data = {'user': await ChatService.get_request_user(environ)}
        user_chats = await Chat.filter(members=session_data['user']['id'])
        for chat in user_chats:
            self.enter_room(sid, str(chat.id), namespace='/notification')

    async def on_disconnect(self, sid):
        await self.disconnect(sid)
