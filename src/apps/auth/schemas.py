import uuid

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
    link: uuid.UUID


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
    token: str
