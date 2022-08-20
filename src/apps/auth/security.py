from src.config import settings


def get_hashed_password(password):
    return settings.PWD_CONTEXT.hash(password)


def verify_password(plain_password, hashed_password):
    return settings.PWD_CONTEXT.verify(plain_password, hashed_password)
