from fastapi import APIRouter

from src.apps.auth.routers import auth_router
from src.apps.chat.routers import chat_router
from src.apps.user.routers import user_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=["auth"])
api_router.include_router(user_router, prefix='/user', tags=["user"])
api_router.include_router(chat_router, prefix='/chat', tags=['chat'])
