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
    description: str
    seller_id: uuid.UUID
    game_id: int
    created_date: datetime
    is_published: bool
