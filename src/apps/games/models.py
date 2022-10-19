from tortoise import models, fields


class Game(models.Model):
    """ Модель игр """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False, unique=True)
    category: fields.ForeignKeyRelation = fields.ForeignKeyField(
        'models.Category',
        on_delete=fields.RESTRICT,
        related_name='category'
    )
    image = fields.CharField(
        max_length=255,
        default='https://res.cloudinary.com/dgcdfglif/image/upload/v1664625373/profile_avatar/fmwbdgbpdrbbskv2pifq.jpg'
    )
