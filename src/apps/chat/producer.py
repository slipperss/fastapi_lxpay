import uuid

from src.apps.chat.models import Message


class Producer:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    @staticmethod
    def create_stream_data(chat_id: uuid.UUID, message: Message, user_id: uuid.UUID):
        stream_data = {
            str(chat_id): str({
                'id': str(message.id),
                'msg': str(message.msg),
                'user': str(user_id),
                'created_date': str(message.created_date)
            })
        }
        return stream_data

    async def add_to_stream(self, stream_channel: str, data: dict) -> str:
        msg_id = await self.redis_client.xadd(name=stream_channel, id="*", fields=data)
        print(f"Message {msg_id} added to {stream_channel} stream")
        return msg_id
