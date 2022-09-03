from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from tortoise.contrib.fastapi import register_tortoise

from src.config import settings
from src.apps import routers

app = FastAPI(
    title="LXPay",
    version="0.0.1",
)

app.mount('/static', StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


register_tortoise(
    app,
    db_url=settings.DATABASE_URL,  # settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},  # settings.APPS_MODELS
    generate_schemas=False,
    add_exception_handlers=True,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.get('/healthcheck/', tags=['healthcheck'])
async def healthcheck():
    return {'Hello': 'World'}


@app.get('/')
async def google_auth_page(request: Request):
    return templates.TemplateResponse("google_auth.html", {"request": request})


app.include_router(routers.api_router, prefix=settings.API_V1_STR)


#
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=80, debug=True)