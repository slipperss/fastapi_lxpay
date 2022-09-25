import os

from dotenv import load_dotenv

import aioredis

load_dotenv()


async def create_connection():
    host = os.environ.get('REDIS_HOST')
    password = os.environ.get('REDIS_PASSWORD')
    user = os.environ.get('REDIS_USER')
    connection_url = f"redis://{user}:{password}@{host}"

    """ Создаем подключение к redis """
    connection = aioredis.from_url(
        connection_url, db=0)

    return connection
