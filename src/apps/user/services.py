from . import schemas, models
from ..auth.security import get_hashed_password
from ...base.service_base import BaseService


class UserService(BaseService):
    model = models.User

    @classmethod
    async def create_user(cls, new_user: schemas.UserIn) -> models.User:
        new_user.password = get_hashed_password(new_user.password)
        user = await cls.model.create(**new_user.dict(exclude_none=True, exclude_unset=True))
        return user

    @classmethod
    async def get_or_create_google_user(cls, new_user) -> models.User:
        user = await cls.get(email=new_user['email'])
        if not user:
            user = await cls.model.create(
                email=new_user['email'],
                username=new_user['name'],
                email_verified=new_user['email_verified'],
                avatar=new_user['picture'],
                #password=hashed_random_pass
            )
        return user

    @classmethod
    async def change_password(cls, obj: models.User, new_password: str):
        hashed_password = get_hashed_password(new_password)
        obj.password = hashed_password
        await obj.save()
