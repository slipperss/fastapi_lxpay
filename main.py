from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from debug_toolbar.middleware import DebugToolbarMiddleware

from starlette.middleware.sessions import SessionMiddleware

from tortoise.contrib.fastapi import register_tortoise

from src.apps.chat.socket import asgi_app#, asgi_app1
from src.config import settings
from src.apps import routers

app = FastAPI(
    title="LXPay",
    version="0.0.1",
    debug=settings.DEBUG,
)

if settings.DEBUG is True:
    app.add_middleware(DebugToolbarMiddleware)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=False,
    add_exception_handlers=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.mount('/ws', asgi_app)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(routers.api_router, prefix=settings.API_V1_STR)
