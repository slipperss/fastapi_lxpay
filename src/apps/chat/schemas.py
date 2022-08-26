from datetime import datetime
from pydantic import BaseModel
import uuid


class Message(BaseModel):
    user_id: str
    msg: str
    timestamp = str(datetime.now())


class UserInChat(BaseModel):
    user_id: uuid.UUID


class ChatCreate(BaseModel):
    second_member_id: UserInChat


class Chat(BaseModel):
    id: str
    messages: list[Message]
    members: list[str]
    session_start = str(datetime.now())

