from . import models
from ...base.service_base import BaseService


class GameService(BaseService):
    model = models.Game

    @classmethod
    async def all(cls):
        return await cls.model.all().order_by('name').values('id', 'name', 'category_id', 'category__name')
