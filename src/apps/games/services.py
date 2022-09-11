from . import models
from ...base.service_base import BaseService


class GameService(BaseService):
    model = models.Game
