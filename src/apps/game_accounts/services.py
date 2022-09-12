from .import models
from ...base.service_base import BaseService


class GameAccountService(BaseService):
    model = models.GameAccount
