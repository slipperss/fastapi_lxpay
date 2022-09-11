from pydantic import BaseModel


class GameIn(BaseModel):
    name: str
    category_id: int | None = None


class GameOut(BaseModel):
    id: int
    name: str
    category_id: int