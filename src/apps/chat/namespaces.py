import datetime

import socketio

from src.apps.auth.services import get_current_user
from src.apps.chat.models import Chat
from src.apps.chat.services import ChatService
from src.apps.user.services import UserService


class ChatMainNamespace(socketio.AsyncNamespace):
    connected_users = {}

    def _set_server(self, server):
        self.server = server
        self.server.manager.online_users = {}
        self.server.manager.chat_connected = {}

    async def on_connect(self, sid, environ):
        session = {}
        current_user = await get_current_user(environ['HTTP_TOKEN'])
        chat = await ChatService.get_chat_by_id(environ['HTTP_CHAT'])
        if not chat:
            await self.disconnect(sid)

        existing = await ChatService.check_existing_user_in_chat(
            chat=chat,
            user_id=current_user.id
        )
        if not existing:
            await self.disconnect(sid)

        self.enter_room(sid=sid, room=str(chat.id))

        existing = self.server.manager.chat_connected.get(chat.id)
        if existing is None:
            self.server.manager.chat_connected.update({chat.id: []})

        await ChatService.read_user_messages_in_chat(
            chat=chat,
            user_id=current_user.id
        )
        session.update({'user': current_user})
        session.update({'chat': chat})

        await self.save_session(sid, session)
        self.server.manager.chat_connected.get(chat.id)\
                                          .append(current_user.id)

    async def on_message(self, sid, msg):
        session = await self.get_session(sid)
        message = await ChatService.message_create(
            msg=msg,
            user_id=session['user'].id,
            chat_id=session['chat'].id,
        )
        for member in await session['chat'].members:
            if member.id != session['user'].id:
                if member.id in self.server.manager.chat_connected.get(session['chat'].id):
                    message.is_read = True
                    await message.save()

        parsed_message = ChatService.parse_message(
            message,
            user_id=session['user'].id,
            username=session['user'].username,
        )
        await self.emit(
            event='message',
            data=parsed_message,
            room=str(session['chat'].id)
        )
        await self.emit(
            event='message',
            data={str(session['chat'].id): parsed_message},
            room=str(session['chat'].id),
            namespace='/notification'
        )

    async def on_check_online(self, sid, data):
        existing = self.server.manager.online_users.get(data['user_id'])
        if existing:
            await self.emit(
                event='check_online',
                data={'online': True},
                to=data['to_sid']
            )
        else:
            user = await UserService.get(id=data['user_id'])
            await self.emit(
                event='check_online',
                data={'online': str(user.last_activity)},
                to=data['to_sid']
            )

    async def on_disconnect(self, sid):
        session = await self.get_session(sid)
        self.server.manager.chat_connected.get(session['chat'].id)\
                                          .remove(session['user'].id)
        await self.disconnect(sid)


class ChatNotificationNamespace(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ):
        current_user = await get_current_user(environ['HTTP_TOKEN'])
        user_chats = await Chat.filter(members=current_user.id)
        if not user_chats:
            await self.disconnect(sid)
        else:
            for chat in user_chats:
                self.enter_room(sid, str(chat.id))

        session = {'user': current_user}
        await self.save_session(sid, session)
        self.server.manager.online_users.update({str(current_user.id): sid})
        await UserService.model.filter(id=current_user.id)\
                               .update(is_online=True)

    async def on_disconnect(self, sid):
        session = await self.get_session(sid)
        self.server.manager.online_users.pop(str(session['user'].id))
        await self.disconnect(sid)
        await UserService.model.filter(id=session['user'].id) \
            .update(is_online=False)
        await UserService.model.filter(id=session['user'].id) \
                               .update(last_activity=datetime.datetime.utcnow())

