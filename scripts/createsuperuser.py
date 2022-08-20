import os
import sys

from src.apps.user.models import User
from src.apps.user.schemas import UserIn
from src.apps.user.services import UserService

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tortoise import Tortoise, run_async
from src.config import settings


async def main():
    """ Создание супер юзера
    """
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APPS_MODELS},
    )
    print("Create superuser")
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    is_user_exist = User.get(username=username, email=email, password=password)
    if is_user_exist:
        print("Error, user existing")
    super_user_scheme = UserIn(username=username, email=email, password=password)
    super_user = await UserService.create_superuser(super_user_scheme)
    if super_user:
        print("Success")


if __name__ == '__main__':
    run_async(main())