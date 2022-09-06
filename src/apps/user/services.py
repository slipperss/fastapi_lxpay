import uuid

from . import schemas, models
from ..auth.security import get_hashed_password
from ...base.service_base import BaseService


class UserService(BaseService):
    model = models.User
    create_schema = schemas.UserIn
    get_schema = schemas.UserOut

    @classmethod
    async def create_user(cls, new_user: schemas.UserIn) -> models.User:
        new_user.password = get_hashed_password(new_user.password)
        user = await cls.model.create(**new_user.dict())
        return user

    @classmethod
    async def get_or_create_google_user(cls, new_user) -> models.User:
        user = await cls.get_user_by_email(email=new_user['email'])
        if not user:
            #random_pass = uuid.uuid4()
            #hashed_random_pass = get_hashed_password(random_pass)
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

    @classmethod
    async def get_user_by_email(cls, email) -> models.User:
        try:
            user = await cls.model.get(email=email)
            return user
        except Exception:
            pass

    @classmethod
    async def get_user_by_id(cls, id):
        user = await cls.model.get(id=id)
        return user

    @classmethod
    async def update_user(cls, update_schema, user):
        is_updated = await cls.model.filter(id=user.id).update(**update_schema.dict())
        if is_updated:
            updated_user = await cls.model.get(id=user.id)
            return updated_user

    @classmethod
    async def delete_user(cls, user_id: uuid.UUID):
        obj = await cls.model.get(id=user_id)
        await obj.delete()
        if obj:
            return True
        return False

    @classmethod
    async def create_superuser(cls, new_superuser: create_schema):
        user = await UserService.create_user(new_superuser)
        user.is_superuser = True
        await user.save()
        return user


    # @classmethod
    # async def create_superuser(cls, schema: create_schema):
    #     hashed_password = get_hashed_password(schema.password)
    #     schema.password = hashed_password
    #     return await create_user(schema, )
