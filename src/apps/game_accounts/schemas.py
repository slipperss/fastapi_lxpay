import uuid

from datetime import datetime

from pydantic import BaseModel


class GameAccountIn(BaseModel):
    title: str
    description: str
    game_id: int
    is_published: bool
    price: float | None = None


class GameAccountUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    game_id: int | None = None
    is_published: bool | None = None
    price: float | None = None


class GameAccountOut(BaseModel):
    id: uuid.UUID
    title: str
    seller_id: uuid.UUID
    seller__username: str
    seller__avatar: str
    game__name: str
    price: float
    created_date: datetime
    is_published: bool


class GameAccountDetailOut(GameAccountOut):
    description: str
