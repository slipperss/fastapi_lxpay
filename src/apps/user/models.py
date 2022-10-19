from tortoise import models, fields

from datetime import datetime


class User(models.Model):
    id = fields.UUIDField(pk=True, index=True)
    username = fields.CharField(max_length=20, null=False, unique=True, index=True)
    email = fields.CharField(max_length=200, null=False, unique=True, index=True)
    password = fields.CharField(max_length=100, default='')
    email_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow)
    last_activity = fields.DatetimeField(default=datetime.utcnow)
    is_online = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    avatar = fields.CharField(max_length=250, default='')
