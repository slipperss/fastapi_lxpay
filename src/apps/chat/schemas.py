import uuid

from datetime import datetime

from pydantic import BaseModel

from tortoise.contrib.pydantic import pydantic_model_creator

from src.apps.chat.models import Chat

ChatBase = pydantic_model_creator(
    Chat,
    name="ChatOut",
)


class ChatUserIn(BaseModel):
    user_id: uuid.UUID


class ChatUserOut(BaseModel):
    id: uuid.UUID
    username: str
    avatar: str


class UserInMessage(BaseModel):
    user_id: uuid.UUID
    username: str


class ChatIn(BaseModel):
    members: list[ChatUserIn]

    class Config:
        schema_extra = {
            "example": {
                "members": [
                    {
                        "user_id": "b05a1187-c994-4541-90ec-244eb54ad54d"
                    },
                    {
                        "user_id": "65ff93a5-9c4e-48c8-ac55-93d480583c67"
                    }
                ]
            }
        }


class ChatOut(BaseModel):
    id: uuid.UUID
    created_date: datetime


class MessageOut(BaseModel):
    id: uuid.UUID
    msg: str
    created_date: datetime
    user__id: uuid.UUID
    user__username: str
