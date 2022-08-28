import os

from dotenv import dotenv_values

from passlib.context import CryptContext

from src.apps.auth.security import CustomOAuth2PasswordBearer


CONFIG_CREDENTIALS = dict(dotenv_values(".env"))

PROJECT_NAME = "LXPay"

SECRET_KEY = CONFIG_CREDENTIALS['SECRET_KEY']

GOOGLE_CLIENT_SECRET = CONFIG_CREDENTIALS['GOOGLE_CLIENT_SECRET']

GOOGLE_CLIENT_ID = CONFIG_CREDENTIALS['GOOGLE_CLIENT_ID']

SERVER_HOST = CONFIG_CREDENTIALS["SERVER_HOST"]

SERVER_PORT = CONFIG_CREDENTIALS['SERVER_PORT']

#SERVER_HOST = os.environ.get("SERVER_HOST")

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
]

DATABASE_URL = f'postgres://{CONFIG_CREDENTIALS["POSTGRES_USER"]}:' \
               f'{CONFIG_CREDENTIALS["POSTGRES_PASSWORD"]}@' \
               f'{CONFIG_CREDENTIALS["POSTGRES_HOST"]}:5432/' \
               f'{CONFIG_CREDENTIALS["POSTGRES_DB"]}'

# DATABASE_URL = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
#                f'{os.environ.get("POSTGRES_PASSWORD")}@' \
#                f'{os.environ.get("POSTGRES_HOST")}:5432/' \
#                f'{os.environ.get("POSTGRES_DB")}'

USERS_OPEN_REGISTRATION = True

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
PASSWORD_RESET_JWT_SUBJECT = 'reset_token'
EMAIL_TEMPLATES_DIR = "src/templates/build"

# Email
SMTP_TLS = CONFIG_CREDENTIALS["SMTP_TLS"]
SMTP_PORT = CONFIG_CREDENTIALS["SMTP_PORT"]
SMTP_HOST = CONFIG_CREDENTIALS["SMTP_HOST"]
SMTP_USER = CONFIG_CREDENTIALS["SMTP_USER"]
SMTP_PASSWORD = CONFIG_CREDENTIALS["SMTP_PASSWORD"]
EMAILS_FROM_EMAIL = CONFIG_CREDENTIALS["EMAILS_FROM_EMAIL"]

# SMTP_TLS = os.environ.get("SMTP_TLS")
# SMTP_PORT = os.environ.get("SMTP_PORT")
# SMTP_HOST = os.environ.get("SMTP_HOST")
# SMTP_USER = os.environ.get("SMTP_USER")
# SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
# EMAILS_FROM_EMAIL = os.environ.get("EMAILS_FROM_EMAIL")

EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

APPS_MODELS = [
    "src.apps.user.models",
    "src.apps.auth.models",
    "src.apps.chat.models",
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
