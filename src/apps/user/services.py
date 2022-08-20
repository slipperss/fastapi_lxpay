import uuid

from fastapi import HTTPException
from tortoise.expressions import Q

from . import schemas, models
from ..auth.security import get_hashed_password
from ...base.service_base import BaseService


class UserService(BaseService):
    model = models.User
    create_schema = schemas.UserIn
    update_schema = schemas.UserUpdate
    get_schema = schemas.UserOut

    @classmethod
    async def create_user(cls, new_user: schemas.UserIn) -> models.User:
        new_user.password = get_hashed_password(new_user.password)
        user = await cls.model.create(**new_user.dict())
        return user

    @classmethod
    async def create_google_user(cls, new_user: schemas.GoogleUserCreate) -> models.User:
        random_pass = uuid.UUID()
        new_user.password = get_hashed_password(random_pass)
        user = await cls.model.create(**new_user.dict().pop('token'))
        return user

    @classmethod
    async def change_password(cls, obj: models.User, new_password: str):
        hashed_password = get_hashed_password(new_password)
        obj.password = hashed_password
        await obj.save()

    @classmethod
    async def get_user_by_email(cls, email) -> models.User:
        user = await cls.model.get(email=email)
        return user

    @classmethod
    async def update_user(cls, update_schema, user):
        is_updated = await cls.model.filter(id=user.id).update(**update_schema.dict())
        if is_updated:
            updated_user = await cls.model.get(id=user.id)
            return updated_user

    @classmethod
    async def create_superuser(cls, new_superuser: create_schema):
        user = await UserService.create_user(new_superuser)
        user.is_superuser = True
        await user.save()
        return user


    # @classmethod
    # async def create_superuser(cls, schema: create_schema):
    #     hashed_password = get_hashed_password(schema.password)
    #     schema.password = hashed_password
    #     return await create_user(schema, )
