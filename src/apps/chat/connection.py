from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.number_of_connections: int = 0
        self.user_tokens = []

    async def connect(self, websocket: WebSocket, subprotocol: str):
        """
        Подключаемся к сокету если аналогичный пользователь еще не подключен к нему
        и если подключенных юзеров меньше 2
        """
        new_connection_token = websocket.headers.get('Sec-WebSocket-Protocol')

        if new_connection_token in self.user_tokens:
            raise Exception('This user is already connected')

        if not self.number_of_connections < 2:
            raise Exception("Could not connect to the chat")

        await websocket.accept(subprotocol=subprotocol)

        self.active_connections.append(websocket)
        self.number_of_connections += 1
        self.user_tokens.append(new_connection_token)

    async def disconnect(self, websocket: WebSocket):
        """ Отключаемся от сокета """
        token = websocket.headers.get('Sec-WebSocket-Protocol')
        self.active_connections.remove(websocket)
        self.number_of_connections -= 1
        self.user_tokens.remove(token)
        await websocket.close()

    async def send_personal_message(self, message: str):
        """ Отправляем сообщение юзерам по сокету """
        for connection in self.active_connections:
            print(message)
            await connection.send_json(message)
