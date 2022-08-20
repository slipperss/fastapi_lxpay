import uuid
from uuid import UUID

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class VerificationCreate(BaseModel):
    """ Схема для проверки email при регистрации
    """
    user_id: int


class VerificationOut(BaseModel):
    """ Схема для проверки email при регистрации
    """
    link: UUID


class Msg(BaseModel):
    """ Схема для сообщение
    """
    msg: str


class EmailRecover(BaseModel):
    email: str


class ResetPassword(BaseModel):
    #token: str
    new_password = str


class GoogleToken(BaseModel):
    user_id: uuid.UUID
    token: str
