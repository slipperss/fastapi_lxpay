import datetime
import uuid

from tortoise.expressions import Q, Subquery

from src.apps.auth.services import get_current_user
from src.apps.chat import models
from src.apps.chat.schemas import ChatIn
from src.apps.user.models import User


class ChatService:
    @classmethod
    async def get_chat_by_id(cls, chat_id: uuid.UUID):
        """ Получаем чат по его id """
        chat = await models.Chat.get_or_none(id=chat_id)
        return chat

    @classmethod
    async def check_existing_user_in_chat(cls, chat: models.Chat, user_id: uuid.UUID):
        """ Проверяем существование пользователя в чате """
        for member in await chat.members:
            if user_id == member.id:
                return True
        return False

    @classmethod
    async def check_chat_by_members(cls, members):
        """ Проверяем существование чата с помощью 2-х его участников """
        sub1 = Subquery(models.Chat.filter(members=members[0].id).only('id'))
        sub2 = Subquery(models.Chat.filter(members=members[1].id).only('id'))
        chat = await models.Chat.filter(Q(id__in=sub1) &
                                      Q(id__in=sub2))
        return chat

    @classmethod
    async def get_all_user_chats(cls, user_id: uuid.UUID):
        """ Получаем все чаты юзера """
        print('(my_chats) -> Beginning queries ...')
        now = datetime.datetime.now()
        chats = await models.Chat.filter(members=user_id).prefetch_related('members').order_by('created_date')
        edited_chats = []
        for chat in chats:
            members = await chat.members.all().values('id', 'username', 'avatar')
            for member in members:
                if member['id'] != user_id:
                    unread_msgs = await models.Message.filter(
                        chat_id=chat.id,
                        is_read=False,
                        user_id=member['id']
                    ).count()

            edited_chats.append({
                'id': chat.id,
                'сreated_date': chat.created_date,
                'members': members,
                'last_message': await models.Message.get_or_none(chat_id=chat.id)
                                                    .order_by('-created_date')
                                                    .limit(1)
                                                    .values('user__username', 'msg', 'created_date') or None,
                'unread_messages': unread_msgs
            })
        diff = (datetime.datetime.now() - now)
        print(f'(my_chats) -> Queries finished in {diff.seconds} seconds')

        # Sorting chats
        # for i in range(len(edited_chats)):
        #     latest = i
        #     for j in range(i + 1, len(edited_chats)):
        #         if edited_chats[j]['last_message'] and edited_chats[latest]['last_message']:
        #             latest_msg = edited_chats[latest]['last_message']['created_date']
        #             next_msg = edited_chats[j]['last_message']['created_date']
        #             if next_msg > latest_msg:
        #                 latest = j
        #         elif edited_chats[j]['last_message']:
        #             latest = j
        #         elif edited_chats[latest]['last_message']:
        #             continue
        #     edited_chats[i], edited_chats[latest] = edited_chats[latest], edited_chats[i]
        return edited_chats

    @classmethod
    async def chat_create(cls, new_chat: ChatIn):
        """ Создаем чат и юзеров к нему """
        members = []
        for member in new_chat.members:
            user = await User.get(id=member.user_id)
            members.append(user)

        chat = await cls.check_chat_by_members(members)
        if not chat:
            chat = await models.Chat.create()
            await chat.members.add(*members)
            return chat
        else:
            return chat[0]

    @classmethod
    async def message_create(cls, msg: str, user_id: uuid.UUID, chat_id: uuid.UUID):
        """ Создаем сообщение """
        message = await models.Message.create(msg=msg, user_id=user_id, chat_id=chat_id)
        return message

    @classmethod
    async def read_user_messages_in_chat(cls, chat: models.Chat, user_id: uuid.UUID):
        for member in await chat.members:
            if member.id != user_id:
                await models.Message.filter(chat_id=chat.id, user_id=member.id).update(is_read=True)

    @classmethod
    async def get_all_messages_in_chat(cls, chat_id: uuid.UUID):
        """ Получаем всю историю сообщений в чате """
        messages = await models.Message.filter(chat_id=chat_id).select_related('user') \
                                                               .order_by('created_date')\
                                                               .values('id',
                                                                       'msg',
                                                                       'created_date',
                                                                       'user__id',
                                                                       'user__username',
                                                                       'is_read'
                                                                       )
        return messages

    @classmethod
    async def get_all_unread_user_messages(cls, user: User):
        print('(unread_messages) -> Beginning queries ...')
        now = datetime.datetime.now()
        chats = await models.Chat.filter(members=user.id).prefetch_related('members')
        count_unread_msgs = 0
        for chat in chats:
            members = await chat.members.all()
            for member in members:
                if member.id != user.id:
                    count_unread_msgs += await models.Message.filter(
                        user=member.id,
                        chat=chat.id,
                        is_read=False
                    ).count()
        diff = (datetime.datetime.now() - now)
        print(f'(unread_messages) -> Queries finished in {diff.seconds} seconds')
        return count_unread_msgs

    @staticmethod
    def parse_message(message, user_id: uuid.UUID, username: str):
        """ Парсим сообщения для отправки по сокету """
        pubsub_data = {
            'id': str(message.id),
            'msg': message.msg,
            'user__id': str(user_id),
            'user__username': username,
            'is_read': message.is_read,
            'created_date': str(message.created_date)
        }
        return pubsub_data

    @staticmethod
    async def get_request_user(environ):
        token = environ.get('HTTP_TOKEN')
        current_user = await get_current_user(token)
        return {
            'id': current_user.id,
            'username': current_user.username,
        }
