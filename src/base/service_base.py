from typing import TypeVar, Type, Optional

from fastapi import HTTPException
from pydantic import BaseModel
from tortoise import models


ModelType = TypeVar("ModelType", bound=models.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class BaseService:
    model: Type[ModelType]
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    query_schema: QuerySchemaType
    get_schema: GetSchemaType

    # def __init__(self, model: Type[ModelType]):
    #     self.model = model
    @classmethod
    async def create(cls, schema, *args, **kwargs) -> Optional[CreateSchemaType]:
        obj = await cls.model.create(**schema.dict(exclude_unset=True), **kwargs)
        return await cls.get_schema.from_tortoise_orm(obj)

    @classmethod
    async def update(cls, schema, **kwargs) -> Optional[UpdateSchemaType]:
        await cls.model.filter(**kwargs).update(**schema.dict(exclude_unset=True))
        return await cls.get_schema.from_queryset_single(cls.model.get(**kwargs))

    @classmethod
    async def delete(cls, **kwargs):
        obj = await cls.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(status_code=404, detail='Object does not exist')

    @classmethod
    async def all(cls) -> Optional[GetSchemaType]:
        return await cls.get_schema.from_queryset(cls.model.all())

    @classmethod
    async def filter(cls, **kwargs) -> Optional[GetSchemaType]:
        return await cls.get_schema.from_queryset(cls.model.filter(**kwargs))

    @classmethod
    async def get(cls, **kwargs) -> Optional[GetSchemaType]:
        return await cls.get_schema.from_queryset_single(cls.model.get(**kwargs))

    @classmethod
    async def get_obj(cls, **kwargs) -> Optional[ModelType]:
        return await cls.model.get_or_none(**kwargs)
