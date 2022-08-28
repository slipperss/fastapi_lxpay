import uuid

from tortoise.expressions import Q, F, Subquery

from src.apps.chat import models
from src.apps.chat import schemas
from src.apps.user.models import User
from src.base.service_base import BaseService


class ChatService(BaseService):
    model = models.Chat
    create_schema = schemas.ChatIn
    get_schema = schemas.ChatOut

    @classmethod
    async def get_chat_by_id(cls, chat_id: uuid.UUID):
        chat = await models.Chat.get(id=chat_id)
        return chat

    @classmethod
    async def check_existing_user_in_chat(cls, chat: models.Chat, user: User):
        for member in await chat.members:
            if user.id == member.id:
                return True
        return False

    @classmethod
    async def check_chat_by_members(cls, members):
        sub1 = Subquery(models.Chat.filter(members=members[0].id).only('id'))
        sub2 = Subquery(models.Chat.filter(members=members[1].id).only('id'))
        chat = await cls.model.filter(Q(id__in=sub1) &
                                      Q(id__in=sub2))
        return chat

    @classmethod
    async def get_all_user_chats(cls, user: User):
        chats = await models.Chat.filter(members=user.id)
        return chats

    @classmethod
    async def chat_create(cls, new_chat: create_schema):
        members = []
        for member in new_chat.members:
            user = await User.get(id=member.user_id)
            members.append(user)

        chat = await cls.check_chat_by_members(members)
        if not chat:
            chat = await models.Chat.create()
            await chat.members.add(*members)
            return chat, new_chat.members
        else:
            return chat[0], new_chat.members

    @classmethod
    async def message_create(cls, msg: str, user_id: uuid.UUID, chat_id: uuid.UUID):
        message = await models.Message.create(msg=msg, user_id=user_id, chat_id=chat_id)
        return message

    @classmethod
    async def get_all_messages_in_chat(cls, chat_id: uuid.UUID):
        messages = await models.Message.filter(chat_id=chat_id).only('msg', 'created_date')\
                                                               .select_related('user')\
                                                               .order_by('created_date')
        return messages
