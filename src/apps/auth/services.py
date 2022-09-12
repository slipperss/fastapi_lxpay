from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from starlette.background import BackgroundTasks

from google.auth.transport import requests
from google.oauth2 import id_token

from jose import jwt, JWTError

from passlib.exc import InvalidTokenError

from tortoise.expressions import Q

from .models import Verification
from .schemas import TokenData, VerificationOut
from .security import verify_password
from .send_email import send_new_account_email
from ..user.schemas import UserIn, GoogleUserCreate
from ..user.services import UserService
from ..user import models
from ...config import settings
from ...config.settings import GOOGLE_CLIENT_ID


def create_access_token(data: dict):
    """ Генерация jwt access токена """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str):
    """ Проверка авторизирован ли юзер """
    user = await UserService.get(email=email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(settings.OAUTH2_SCHEME)):
    """ Получить обьект текущего пользователя """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await UserService.get(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """ Получить обьект текущего верифицированного и активного пользователя """
    if not current_user.is_active:
        raise HTTPException(status_code=405, detail="Inactive user")
    return current_user


async def get_current_verified_active_user(current_user: models.User = Depends(get_current_active_user)):
    """ Получить обьект текущего верифицированного и активного пользователя """
    if not current_user.email_verified:
        raise HTTPException(status_code=405, detail="Email not verified")
    return current_user


async def get_current_verified_active_superuser(current_user: models.User = Depends(get_current_verified_active_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You don't have administrator rights")
    return current_user


async def registration_user(new_user: UserIn, task: BackgroundTasks) -> bool:
    """ Регистрация пользователя """
    existing = await models.User.get(Q(username=new_user.username) | Q(email=new_user.email)).exists()
    if existing:
        return True
    else:
        user = await UserService.create_user(new_user)
        verify = await Verification.create(user_id=user.id)
        task.add_task(
            send_new_account_email, new_user.email, new_user.username, verify.link
        )
    return False


async def verify_registration_user(uuid: VerificationOut) -> bool:
    """ Подтверждение email пользователя """
    verify = await Verification.get(link=uuid).prefetch_related("user")
    print(verify.link, verify.user.id)
    if verify:
        await models.User.filter(id=verify.user.id).update(email_verified=True)
        await Verification.get(link=uuid).delete()
        return True
    else:
        return False


def generate_password_reset_token(email: str):
    """ Генерация токена для дальнейшего изменения пароля """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    expires = datetime.utcnow() + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "sub": settings.PASSWORD_RESET_JWT_SUBJECT, "email": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str):
    """ Проверка на валидность токена для изменения пароля """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded_token["sub"] == settings.PASSWORD_RESET_JWT_SUBJECT
        return decoded_token["email"]
    except InvalidTokenError:
        return False


async def google_auth(user: GoogleUserCreate) -> tuple:
    """ Авторизация через google """
    try:
        id_info = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await UserService.get_or_create_google_user(id_info)
    data = {"sub": user.email}
    access_token = create_access_token(data=data)
    return access_token