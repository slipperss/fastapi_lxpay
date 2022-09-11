from tortoise import models, fields


class Game(models.Model):
    """ Модель игр """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    category: fields.ForeignKeyRelation = fields.ForeignKeyField(
        'models.Category',
        on_delete=fields.CASCADE,
        related_name='category'
    )
