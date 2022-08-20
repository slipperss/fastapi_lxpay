from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from src.apps.auth.services import get_current_verified_active_user
from src.apps.user import models
from src.apps.user.services import UserService
from src.apps.user.schemas import UserOut, UserUpdate, UserIn

user_router = APIRouter()


@user_router.get("/me/", response_model=UserOut, tags=['user'])
async def read_users_me(current_user: models.User = Depends(get_current_verified_active_user)):
    return current_user


@user_router.put("/update/", response_model=UserOut)
async def partial_update_user(
        to_update: UserUpdate,
        current_user: models.User = Depends(get_current_verified_active_user)
):
    updated_user = await UserService.update_user(to_update, current_user)
    return updated_user

@user_router.post('/superuser/', response_model=UserOut)
async def create_superuser(new_superuser: UserIn):
    superuser = await UserService.create_superuser(new_superuser)
    return superuser
