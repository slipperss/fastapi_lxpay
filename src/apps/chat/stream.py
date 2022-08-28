
class StreamConsumer:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def consume_stream(self, count: int, block: int,  stream_channel: str):
        response = await self.redis_client.xread(streams={stream_channel:  '0-0'}, count=count, block=block)
        if not response:
            return False
        return response

    async def delete_message(self, stream_channel, message_id):
        await self.redis_client.xdel(stream_channel, message_id)
        print(f'Message {message_id} deleted from {stream_channel}')
