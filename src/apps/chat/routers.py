import uuid

from rejson import Path

from fastapi import APIRouter, Depends
from starlette import status

from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from .cache import Cache
from .connection import ConnectionManager
from .producer import Producer
from .redis_conf import Redis
from .schemas import Chat, ChatCreate, Message
from .stream import StreamConsumer
from ..auth.services import get_current_verified_active_user
from ..user.models import User
from ..user.services import UserService

# https://github.com/stephensanwo/fullstack-ai-chatbot
# https://www.freecodecamp.org/news/how-to-build-an-ai-chatbot-with-redis-python-and-gpt/

# https://github.com/leonh/redis-streams-fastapi-chat/blob/master/chat.py

manager = ConnectionManager()

chat_router = APIRouter()

redis = Redis()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>LXPay Chat</h1>
        <h2>Your username: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/api/chat/ws/${client_id}/`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@chat_router.get('/')
async def chat_page():
    return HTMLResponse(html)


@chat_router.get('/my-chats/')#, response_model=list(Chat))
async def get_all_user_chats(current_user: User = Depends(get_current_verified_active_user)):
    json_client = redis.create_rejson_connection()
    cache = Cache(json_client)
    chats = await cache.get_all_user_chats(current_user)
    return chats

@chat_router.post('/create/', response_model=Chat)
async def create_chat(new_chat: ChatCreate, current_user: User = Depends(get_current_verified_active_user)):
    # Create new chat session
    json_client = redis.create_rejson_connection()

    chat_id = str(uuid.uuid4())

    first_chat_member = str(current_user.id)
    existing = await UserService.get_user_by_id(new_chat.second_member_id.user_id)

    if existing:
        chat_session = Chat(
            id=chat_id,
            members=[first_chat_member, str(new_chat.second_member_id.user_id)],
            messages=[]
        )

        # Store chat session in redis JSON with the token as key
        json_client.jsonset('chats', Path.rootPath(), chat_session.dict())

        # Set a timeout for redis data
        #redis_client = await redis.create_connection()
        #await redis_client.expire(chat_session.id, 60 * 60)  # 60 minutes
        return chat_session.dict()


@chat_router.websocket("/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: str,
        current_user: User = Depends(get_current_verified_active_user)
):
    if chat_id is None or chat_id == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    redis_client = await redis.create_connection()

    existing = await redis_client.exists(chat_id)
    if not existing:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")

    await manager.connect(websocket)
    json_client = redis.create_rejson_connection()
    consumer = StreamConsumer(redis_client)
    producer = Producer(redis_client)
    cache = Cache(json_client)
    prev_data = await cache.get_chat_history(chat_id)
    print(prev_data)

    try:
        while True:
            data = await websocket.receive_text()
            msg = Message(user_id=str(current_user.id), msg=data)
            stream_data = {str(chat_id): str(msg.dict())}
            #channel_name = f"{chat_id}_channel"

            print(manager.number_of_connections)
            if manager.number_of_connections > 1:
                await producer.add_to_stream(stream_data, 'message_channel')
            await cache.add_message_to_cache(token=chat_id, message_data=msg.dict())

            if manager.number_of_connections > 1:
                response = await consumer.consume_stream(stream_channel='message_channel', count=1, block=0)
                if response:
                    #print('PURE_RESPONSE: ', response)
                    for stream, messages in response:
                        for message in messages:
                            response_token = [k.decode('utf-8')
                                              for k, v in message[1].items()][0]

                            message_id = response[0][1][0][0].decode('utf-8')

                            if chat_id == response_token:
                                response_message = [v.decode('utf-8')
                                                    for k, v in message[1].items()][0]
                                dict_message = eval(response_message)

                                await manager.send_personal_message(dict_message)
                                await consumer.delete_message(stream_channel='message_channel',
                                                              message_id=message_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
