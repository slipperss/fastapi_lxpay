import os

from dotenv import load_dotenv

from passlib.context import CryptContext

from src.apps.auth.security import CustomOAuth2PasswordBearer

load_dotenv()

PROJECT_NAME = "LXPay"

DEBUG = os.environ.get('DEBUG')

SECRET_KEY = os.environ.get('SECRET_KEY')

GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

SERVER_HOST = os.environ.get("SERVER_HOST")

SERVER_PORT = os.environ.get('SERVER_PORT')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_V1_STR = "/api"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

OAUTH2_SCHEME = CustomOAuth2PasswordBearer(tokenUrl="/api/auth/login/")


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Token 60 minutes * 24 hours * 7 days = 7 days

BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

DATABASE_URL = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("POSTGRES_HOST")}:5432/' \
               f'{os.environ.get("POSTGRES_DB")}'

USERS_OPEN_REGISTRATION = True

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
PASSWORD_RESET_JWT_SUBJECT = 'reset_token'
EMAIL_TEMPLATES_DIR = "src/templates/build"


# SMTP_TLS = os.environ.get("SMTP_TLS")
# SMTP_PORT = os.environ.get("SMTP_PORT")
# SMTP_HOST = os.environ.get("SMTP_HOST")
# SMTP_USER = os.environ.get("SMTP_USER")
# SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
# EMAILS_FROM_EMAIL = os.environ.get("EMAILS_FROM_EMAIL")

#EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

APPS_MODELS = [
    "src.apps.user.models",
    "src.apps.auth.models",
    "src.apps.chat.models",
    "src.apps.categories.models",
    "src.apps.games.models",
    "src.apps.game_accounts.models",
    "aerich.models",
]

TORTOISE_ORM = {  # https://github.com/tortoise/aerich

    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        }
    },
}
