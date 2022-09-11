# from tortoise import models, fields
#
# from datetime import datetime
#
#
# class Account(models.Model):
#     """ Модель аккаунта на продажу """
#     id = fields.UUIDField(pk=True)
#     title = fields.CharField(max_length=255, null=False, index=True)
#     description = fields.TextField()
#     seller: fields.ForeignKeyRelation = fields.ForeignKeyField(
#         'models.User',
#         on_delete=fields.CASCADE,
#         related_name='seller'
#     )
#     game = fields.ForeignKeyRelation = fields.ForeignKeyField(
#         'models.Games',
#         on_delete=fields.CASCADE,
#         related_name='game'
#     )
#     created_date = fields.DatetimeField(default=datetime.utcnow)
#
#
