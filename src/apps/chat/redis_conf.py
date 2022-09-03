import os

from dotenv import load_dotenv

import aioredis


load_dotenv()


class Redis:
    def __init__(self):
        """initialize  connection """
        self.REDIS_HOST = os.environ.get('REDIS_HOST')
        self.REDIS_HOST_WITHOUT_PORT = os.environ.get('REDIS_HOST_WITHOUT_PORT')
        self.REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
        self.REDIS_USER = os.environ.get('REDIS_USER')
        self.REDIS_PORT = os.environ.get('REDIS_PORT')
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}"
        self.connection = None
        self.redisJson = None

    async def create_connection(self):
        """ Создаем подключение к redis """
        self.connection = aioredis.from_url(
            self.connection_url, db=0)

        return self.connection
