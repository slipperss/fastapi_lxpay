from tortoise import models, fields

from datetime import datetime

from src.apps.user.models import User


class Chat(models.Model):
    """ Модель чата """
    id = fields.UUIDField(pk=True, index=True)
    created_date = fields.DatetimeField(default=datetime.utcnow)
    members: fields.ManyToManyRelation[User] = fields.ManyToManyField(
        'models.User',
        through='chat_user',
        related_name='members',
        on_delete=fields.NO_ACTION
    )


class Message(models.Model):
    """ Модель сообщений """
    id = fields.UUIDField(pk=True)
    msg = fields.CharField(null=False, max_length=10000)
    user: fields.ForeignKeyRelation = fields.ForeignKeyField(
        'models.User',
        on_delete=fields.CASCADE,
        related_name='user'
    )
    chat: fields.ForeignKeyRelation = fields.ForeignKeyField(
        'models.Chat',
        on_delete=fields.CASCADE,
        related_name='chat'
    )
    created_date = fields.DatetimeField(default=datetime.utcnow)
