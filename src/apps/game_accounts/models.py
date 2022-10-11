from tortoise import models, fields

from datetime import datetime


class GameAccount(models.Model):
    """ Модель аккаунта на продажу """
    id = fields.UUIDField(pk=True, index=True)
    title = fields.CharField(max_length=255, null=False, index=True)
    description = fields.TextField()
    seller: fields.ForeignKeyRelation = fields.ForeignKeyField(
        'models.User',
        on_delete=fields.RESTRICT,
        related_name='seller'
    )
    game = fields.ForeignKeyRelation = fields.ForeignKeyField(
        'models.Game',
        on_delete=fields.RESTRICT,
        related_name='game'
    )
    price = fields.FloatField(default=0.00)

    created_date = fields.DatetimeField(default=datetime.utcnow)
    is_published = fields.BooleanField(default=True)

    class Meta:
        table = 'game_account'
