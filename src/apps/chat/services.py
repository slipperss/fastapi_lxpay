import uuid

from tortoise.expressions import Q, Subquery, F

from src.apps.chat import models
from src.apps.chat.schemas import ChatIn
from src.apps.user.models import User


class ChatService:
    @classmethod
    async def get_chat_by_id(cls, chat_id: uuid.UUID):
        """ Получаем чат по его id """
        chat = await models.Chat.get(id=chat_id)
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
    async def get_all_user_chats(cls, user: User):
        """ Получаем все чаты юзера """
        chats = await models.Chat.filter(members=user.id).prefetch_related('members')
        chats_with_members = []
        for chat in chats:
            chats_with_members.append(
                {
                    'id': chat.id,
                    'сreated_date': chat.created_date,
                    'members': await chat.members.all().values('id', 'username', 'avatar'),
                    'last_message': await models.Message.filter(chat_id=chat.id)
                                                        .order_by('-created_date')
                                                        .limit(1)
                                                        .values('user__username', 'msg', 'created_date')
                }
            )
        return chats_with_members

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
    async def get_all_messages_in_chat(cls, chat_id: uuid.UUID):
        """ Получаем всю историю сообщений в чате """
        messages = await models.Message.filter(chat_id=chat_id).select_related('user') \
                                                               .order_by('created_date')\
                                                               .values('id',
                                                                       'msg',
                                                                       'created_date',
                                                                       'user__id',
                                                                       'user__username',
                                                                       #'user__avatar',
                                                                       )
        return messages
