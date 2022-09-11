from tortoise import models, fields


class Category(models.Model):
    """ Модель категорий игр """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)

