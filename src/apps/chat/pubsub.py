import redis

from src.apps.auth.services import get_current_user


async def get_message_custom(pubsub, ignore_subscribe_messages: bool = False, timeout: float = 0.0):
    """
    A copy of the get_message method in aioredis
    but small bug -> parse_response parameter block=False was changed to True
    """
    response = await pubsub.parse_response(block=True, timeout=timeout)
    if response:
        return pubsub.handle_message(response, ignore_subscribe_messages)
    return None


async def send_message_to_socket(sio, message, room):
    """ Отправляем сообщение пользователям по сокету """
    if message['channel'] != b'socketio' and message is not None:
        print('msg', message)
        #message = eval(message['data'])
        await sio.emit(event='message', data=message['data'], room=room, namespace='/chat/')
    return


async def listener(sio, chat, pubsub):
    """ Прослушиваем канал и ловим в нем сообщения """
    print('LISTENER', chat)
    while True:
        try:
            message = await get_message_custom(pubsub, ignore_subscribe_messages=True)
            #await sio.emit(event='message', data=message['data'], room=chat, namespace='/chat/')
            await send_message_to_socket(sio, message, chat)
        except redis.exceptions.ResponseError:
            raise redis.exceptions.ResponseError


def parse_message(message, session_data):
    """ Парсим сообщения для отправки в канал """
    pubsub_data = {
        'id': str(message.id),
        'msg': message.msg,
        'user__id': str(session_data['user_id']),
        'user__username': session_data['username'],
        'created_date': str(message.created_date)
    }
    return pubsub_data


async def send_message_to_channel(redis_conn, session_data, parsed_message):
    """ Отправляем сообщения в pubsub канал """
    await redis_conn.publish(session_data['chat'], str(parsed_message))


async def get_request_data(environ):
    token = environ.get('HTTP_TOKEN')
    current_user = await get_current_user(token)
    chat = environ.get('HTTP_CHAT')
    return {
        'token': token,
        'user_id': current_user.id,
        'username': current_user.username,
        'chat': chat
    }
