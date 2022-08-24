from pydantic import BaseModel, EmailStr, Field

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

# UserUpdate = pydantic_model_creator(
#     User,
#     name='UserUpdate',
#     exclude_readonly=True,
#     exclude=('email_verified', 'last_activity', 'join_date', 'password', 'email', 'is_superuser', 'is_active')
# )

# class UserUpdate(BaseModel):
#     username: str | None = Field(default=None)
#     avatar: str | None = Field(default=None)

class UpdateAvatar(BaseModel):
    avatar: str

class UpdateUsername(BaseModel):
    username: str


class GoogleUserCreate(BaseModel):
    username: str
    email: EmailStr
    avatar: str
    token: str
