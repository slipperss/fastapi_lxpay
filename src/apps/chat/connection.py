from copy import copy

from typing import List

from starlette.websockets import WebSocket

from src.apps.auth.services import get_current_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.number_of_connections: int = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.number_of_connections += 1

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.number_of_connections -= 1

    async def send_personal_message(self, message: str):
        for connection in self.active_connections:
            token = connection.headers.get('Authorization').split(' ')[1]
            user = await get_current_user(token)
            print('---------')
            print(user.username)
            print(not str(user.id) == str(message['user']))
            if not str(user.id) == str(message['user']):
                print('Enter', user.username)
                new_message = copy(message)
                new_message['username'] = user.username
                await connection.send_text(str(new_message))
                print('---------')
                break
