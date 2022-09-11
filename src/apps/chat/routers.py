import uuid

from fastapi import APIRouter, Depends, HTTPException, Path, Header, Request, Body

from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from .connection import ConnectionManager
from .producer import Producer
from .redis_conf import Redis
from .schemas import ChatIn, ChatOut, MessageOut
from .services import ChatService
from .stream import StreamConsumer
from ..auth.services import get_current_verified_active_user, get_current_user
from ..user.models import User


manager = ConnectionManager()

chat_router = APIRouter()

redis = Redis()


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


@chat_router.websocket('/{chat_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: uuid.UUID = Path(default=...),
        sec_websocket_protocol=Header(default=...)
):
    current_user = await get_current_user(sec_websocket_protocol)

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

    try:
        # Connecting
        await manager.connect(websocket, sec_websocket_protocol)
        print(f"{current_user.username} connected to chat")
        redis_client = await redis.create_connection()
        consumer = StreamConsumer(redis_client)
        producer = Producer(redis_client)

        while True:
            data = await websocket.receive_text()
            if data:
                # Post message to database and create stream_data to paste it in stream channel
                message = await ChatService.message_create(msg=data, user_id=current_user.id, chat_id=chat_id)
                stream_data = Producer.create_stream_data(
                    chat_id=chat_id,
                    message=message,
                    user_id=current_user.id,
                    username=current_user.username
                )
                stream_channel = f'{chat_id}_channel'
                await producer.add_to_stream(stream_channel=stream_channel, data=stream_data)

                # Get message from channel
                response = await consumer.consume_stream(stream_channel=stream_channel, count=1, block=0)
                if response:
                    for stream, messages in response:
                        for message in messages:
                            message, channel_msg_id = await StreamConsumer.parse_message_from_stream(message, chat_id)
                            await manager.send_personal_message(message)  # Send message with websocket
                            await consumer.delete_message(stream_channel=stream_channel,  # delete message from channel
                                                          message_id=channel_msg_id)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
