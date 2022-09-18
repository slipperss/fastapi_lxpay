import uuid

from datetime import datetime

from pydantic import BaseModel


class GameAccountIn(BaseModel):
    title: str
    description: str
    game_id: int
    is_published: bool


class GameAccountUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    game_id: int | None = None
    is_published: bool | None = None


class GameAccountOut(BaseModel):
    id: uuid.UUID
    title: str
    seller_id: uuid.UUID
    seller__username: str
    game__name: str
    created_date: datetime


class GameAccountDetailOut(GameAccountOut):
    description: str
