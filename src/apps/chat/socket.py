import os

from dotenv import load_dotenv

import socketio

from src.apps.chat.namespaces import ChatMainNamespace, ChatNotificationNamespace

load_dotenv()

# arm = socketio.AsyncRedisManager(
#     f"redis://{os.environ.get('REDIS_USER')}:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}"
# )
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])

sio.register_namespace(ChatMainNamespace('/chat'))
sio.register_namespace(ChatNotificationNamespace('/notification'))

asgi_app = socketio.ASGIApp(sio)

