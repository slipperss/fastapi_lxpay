from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.websockets import WebSocket

from src.config import settings


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)


def get_hashed_password(password):
    return settings.PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return settings.PWD_CONTEXT.verify(plain_password, hashed_password)

