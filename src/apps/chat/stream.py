
class StreamConsumer:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def consume_stream(self, count: int, block: int,  stream_channel: str):
        """ Подписываемся на канал с сообщениями и отслеживаем новые """
        response = await self.redis_client.xread(streams={stream_channel:  '0-0'}, count=count, block=block)
        if not response:
            return False
        return response

    async def delete_message(self, stream_channel, message_id):
        """ Удаляем сообщения из канала """
        await self.redis_client.xdel(stream_channel, message_id)
        print(f'Message {message_id} deleted from {stream_channel}')

    @staticmethod
    async def parse_message_from_stream(response_message, chat_id):
        response_chat_token = [k.decode('utf-8') for k, v in response_message[1].items()][0]
        channel_msg_id = response_message[0].decode('utf-8')
        if str(chat_id) == response_chat_token:
            response_message = [v.decode('utf-8') for k, v in response_message[1].items()][0]
            dict_message = eval(response_message)
            return dict_message, channel_msg_id