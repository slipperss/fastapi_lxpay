from tortoise import models, fields


class Verification(models.Model):
    """ Модель для подтверждения регистрации пользователя по почте """
    link = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='verification', on_delete=fields.CASCADE)
