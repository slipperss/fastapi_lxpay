from . import models
from ...base.service_base import BaseService


class CategoryService(BaseService):
    model = models.Category
