from tortoise import models, fields


class Game(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)

