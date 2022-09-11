from typing import TypeVar, Type

from fastapi import HTTPException
from tortoise import models

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseService:
    model: Type[ModelType]

    @classmethod
    async def create(cls, schema, *args, **kwargs):
        obj = await cls.model.create(**schema.dict(exclude_unset=True, exclude_none=True), **kwargs)
        return obj

    @classmethod
    async def update_and_get(cls, schema, **kwargs):
        res = await cls.model.filter(**kwargs).update(**schema.dict(exclude_unset=True, exclude_none=True))
        if not res:
            raise HTTPException(status_code=404, detail='Object doest not exist')
        obj = await cls.model.get(**kwargs)
        return obj

    @classmethod
    async def delete(cls, **kwargs):
        obj = await cls.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(status_code=404, detail='Object does not exist')
        return True

    @classmethod
    async def all(cls):
        return await cls.model.all()

    @classmethod
    async def filter(cls, **kwargs):
        return await cls.model.filter(**kwargs)

    @classmethod
    async def get(cls, **kwargs):
        return await cls.model.get(**kwargs)

    @classmethod
    async def get_obj_or_none(cls, **kwargs):
        return await cls.model.get_or_none(**kwargs)