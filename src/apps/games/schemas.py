from pydantic import BaseModel


class GameIn(BaseModel):
    name: str | None = None
    category_id: int | None = None
    image: str | None = None


class GameOut(BaseModel):
    id: int
    name: str
    category_id: int
    image: str
