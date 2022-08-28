import uuid

from datetime import datetime

from pydantic import BaseModel, Field

from tortoise.contrib.pydantic import pydantic_model_creator

from src.apps.chat.models import Chat, Message
from src.apps.user.models import User

ChatOut = pydantic_model_creator(
    Chat,
    name="ChatOut",
)


class UserInChat(BaseModel):
    user_id: uuid.UUID


class UserInMessage(BaseModel):
    user_id: uuid.UUID
    username: str


class ChatIn(BaseModel):
    members: list[UserInChat]


class MessageOut(BaseModel):
    id: uuid.UUID
    msg: str
    #user_id: uuid.UUID
    created_date: datetime

