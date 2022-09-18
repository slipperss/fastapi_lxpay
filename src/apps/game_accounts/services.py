from .import models
from ...base.service_base import BaseService


class GameAccountService(BaseService):
    model = models.GameAccount


    @classmethod
    async def get(cls, **kwargs):
        return await cls.model.get(**kwargs).values(
                                                    'id',
                                                    'title',
                                                    'description',
                                                    'seller_id',
                                                    'seller__username',
                                                    'game__name',
                                                    'created_date',
                                                    )

    @classmethod
    async def filter(cls, **kwargs):
        return await cls.model.filter(**kwargs).values(
                                                       'id',
                                                       'title',
                                                       'seller_id',
                                                       'seller__username',
                                                       'game__name',
                                                       'created_date',
                                                       )
