from fastapi import APIRouter

from src.apps.auth.routers import auth_router
from src.apps.categories.routers import category_router
from src.apps.chat.routers import chat_router
from src.apps.games.routers import game_router
from src.apps.user.routers import user_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_router.include_router(user_router, prefix='/user', tags=['user'])
api_router.include_router(chat_router, prefix='/chat', tags=['chat'])
api_router.include_router(category_router, prefix='/category', tags=['category'])
api_router.include_router(game_router, prefix='/game', tags=['game'])
