from fastapi import HTTPException

from .import models
from ...base.service_base import BaseService


class GameAccountService(BaseService):
    model = models.GameAccount

    expected_fields = (
        'id',
        'title',
        'description',
        'seller_id',
        'seller__username',
        'seller__avatar',
        'seller__is_online',
        'game__name',
        'price',
        'created_date',
        'is_published'
    )

    @classmethod
    async def get(cls, **kwargs):
        return await cls.model.get(**kwargs).values(*cls.expected_fields)

    @classmethod
    async def filter(cls, limit: int = 0, offset: int = 0, **kwargs):
        return await cls.model.filter(**kwargs)\
                              .order_by('-price')\
                              .offset(offset)\
                              .limit(limit)\
                              .values(*cls.expected_fields)

    @classmethod
    async def create_and_get(cls, schema, *args, **kwargs):
        res = await cls.model.create(**schema.dict(exclude_unset=True, exclude_none=True), **kwargs)
        if not res:
            raise HTTPException(status_code=404, detail='Object doest not exist')
        obj = await cls.model.get(id=res.id).values(*cls.expected_fields)
        return obj

    @classmethod
    async def update_and_get(cls, schema, **kwargs):
        res = await cls.model.filter(**kwargs).update(**schema.dict(exclude_unset=True, exclude_none=True))
        if not res:
            raise HTTPException(status_code=404, detail='Object doest not exist')
        obj = await cls.model.get(id=kwargs.get('id')).values(*cls.expected_fields)
        return obj
