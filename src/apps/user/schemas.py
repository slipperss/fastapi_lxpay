from pydantic import BaseModel, EmailStr

from tortoise.contrib.pydantic import pydantic_model_creator

from src.apps.user.models import User


UserIn = pydantic_model_creator(
    User,
    name='UserIn',
    exclude_readonly=True,
    exclude=('email_verified', 'last_activity', 'join_date', 'is_active', 'avatar', 'is_superuser')
)

UserOut = pydantic_model_creator(
    User,
    name="UserOut",
    exclude=("password", )
)


class UserUpdate(BaseModel):
    username: str | None = None
    avatar: str | None = None


class GoogleUserCreate(BaseModel):
    token: str
