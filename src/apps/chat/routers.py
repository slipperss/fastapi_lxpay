import uuid

from fastapi import APIRouter, Depends, HTTPException, Path

from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from .connection import ConnectionManager
from .producer import Producer
from .redis_conf import Redis
from .schemas import ChatIn, ChatOut
from .services import ChatService
from .stream import StreamConsumer
from ..auth.services import get_current_verified_active_user
from ..user.models import User


manager = ConnectionManager()

chat_router = APIRouter()

redis = Redis()


@chat_router.get('/my-chats/', response_model=list[ChatOut])
async def get_all_user_chats(current_user: User = Depends(get_current_verified_active_user)):
    chats = await ChatService.get_all_user_chats(current_user)
    return chats


@chat_router.post('/create/')
async def create_chat(new_chat: ChatIn, current_user: User = Depends(get_current_verified_active_user)):
    if new_chat.members[0].user_id == new_chat.members[1].user_id:
        raise HTTPException(status_code=405, detail="There can't be two identical users in a chat")
    obj = await ChatService.chat_create(new_chat)
    return obj


@chat_router.post('/history/{chat_id}')
async def get_chat_history(chat_id: uuid.UUID, current_user: User = Depends(get_current_verified_active_user)):
    messages = await ChatService.get_all_messages_in_chat(chat_id)
    return messages


@chat_router.websocket("/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: uuid.UUID = Path(default=..., description='chat id'),
        current_user: User = Depends(get_current_verified_active_user)
):
    # Checking if the specified chat exists
    chat = await ChatService.get_chat_by_id(chat_id)
    if not chat:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=404, detail="Chat doesn't exist")

    # Checking if the user from the request is in the specified chat
    existing = await ChatService.check_existing_user_in_chat(chat=chat, user=current_user)
    if not existing:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=403, detail="You haven't permissions to connect this chat")

    redis_client = await redis.create_connection()
    # Checking if a channel for messaging has been created
    # existing = await redis_client.exists(str(chat_id))
    # if not existing:
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     raise HTTPException(status_code=404, detail="Channel doesn't exist")

    # Connecting
    await manager.connect(websocket)
    consumer = StreamConsumer(redis_client)
    producer = Producer(redis_client)
    try:
        while True:
            data = await websocket.receive_text()
            message = await ChatService.message_create(msg=data, user_id=current_user.id, chat_id=chat_id)

            if manager.number_of_connections > 1:
                stream_data = Producer.create_stream_data(chat_id=chat_id, message=message, user_id=current_user.id)
                stream_channel = f'{chat_id}_channel'
                await producer.add_to_stream(stream_channel=stream_channel, data=stream_data)

            if manager.number_of_connections > 1:
                response = await consumer.consume_stream(stream_channel=stream_channel, count=1, block=0)
                if response:
                    for stream, messages in response:
                        for message in messages:
                            response_token = [k.decode('utf-8')
                                              for k, v in message[1].items()][0]
                            message_id = response[0][1][0][0].decode('utf-8')
                            if str(chat_id) == response_token:
                                response_message = [v.decode('utf-8')
                                                    for k, v in message[1].items()][0]
                                dict_message = eval(response_message)
                                await manager.send_personal_message(dict_message)
                                await consumer.delete_message(stream_channel=stream_channel,
                                                              message_id=message_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
