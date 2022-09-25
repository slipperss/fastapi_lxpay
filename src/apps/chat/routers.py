import os
import uuid

import socketio
from fastapi import APIRouter, Depends, HTTPException

from .pubsub import parse_message, get_request_data, listener, send_message_to_channel
from .schemas import MessageOut, ChatOut, ChatIn
from .services import ChatService
from ..auth.services import get_current_verified_active_user
from ..user.models import User


chat_router = APIRouter()

arm = socketio.AsyncRedisManager(
    f"redis://{os.environ.get('REDIS_USER')}:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}"
)
sio = socketio.AsyncServer(client_manager=arm, async_mode='asgi', cors_allowed_origins=[])
asgi_app = socketio.ASGIApp(sio)


@chat_router.get('/my-chats/')
async def get_all_user_chats(current_user: User = Depends(get_current_verified_active_user)):
    chats = await ChatService.get_all_user_chats(current_user)
    return chats


@chat_router.post('/create/', response_model=ChatOut)
async def create_chat(
        new_chat: ChatIn,
        current_user: User = Depends(get_current_verified_active_user)
):
    if new_chat.members[0].user_id == new_chat.members[1].user_id:
        raise HTTPException(status_code=405, detail="There can't be two identical users in a chat")
    obj = await ChatService.chat_create(new_chat)
    return obj


@chat_router.post('/history/{chat_id}', response_model=list[MessageOut])
async def get_chat_history(
        chat_id: uuid.UUID,
        current_user: User = Depends(get_current_verified_active_user)
):
    messages = await ChatService.get_all_messages_in_chat(chat_id)
    return messages


@sio.on('connect')
async def connect_handler(sid, environ):
    session_data = await get_request_data(environ)
    chat = await ChatService.get_chat_by_id(session_data['chat'])
    if not chat:
        await sio.disconnect(sid)

    existing = await ChatService.check_existing_user_in_chat(chat=chat, user_id=session_data['user_id'])
    if not existing:
        await sio.disconnect(sid)

    sio.enter_room(sid=sid, room=session_data['chat'])
    await sio.save_session(sid, session_data)

    """ pubsub realization """
    # await arm.pubsub.subscribe(session_data['chat'])
    # asyncio.create_task(listener(sio, session_data['chat'], arm.pubsub))


@sio.on('message')
async def message_handler(sid, msg):
    session_data = await sio.get_session(sid)
    message = await ChatService.message_create(msg=msg, user_id=session_data['user_id'], chat_id=session_data['chat'])
    parsed_message = parse_message(message, session_data)
    await sio.emit(event='message', data=parsed_message, room=session_data['chat'])
    # await send_message_to_channel(arm.redis, session_data, parsed_message) #pubsub
