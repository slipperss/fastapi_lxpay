import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.apps.auth.services import get_current_verified_active_user
from src.apps.user import models
from src.apps.user.services import UserService
from src.apps.user.schemas import UserOut, UserIn, UpdateUsername, UpdateAvatar

user_router = APIRouter()


@user_router.get("/me/", response_model=UserOut, tags=['user'])
async def read_users_me(current_user: models.User = Depends(get_current_verified_active_user)):
    return current_user


@user_router.put("/update-username/", response_model=UserOut)
async def username_update_user(
        new_username: UpdateUsername,
        current_user: models.User = Depends(get_current_verified_active_user)
):
    updated_user = await UserService.update_user(new_username, current_user)
    return updated_user


@user_router.put("/update-avatar/", response_model=UserOut)
async def avatar_update_user(
        new_avatar: UpdateAvatar,
        current_user: models.User = Depends(get_current_verified_active_user)
):
    updated_user = await UserService.update_user(new_avatar, current_user)
    return updated_user

@user_router.post('/superuser/', response_model=UserOut)
async def create_superuser(new_superuser: UserIn):
    superuser = await UserService.create_superuser(new_superuser)
    return superuser


@user_router.delete('/delete/{user_id}/')
async def delete_user(user_id: uuid.UUID):
    response = await UserService.delete_user(user_id)
    if response:
        return {'detail': 'User deleted'}
    raise HTTPException(status_code=404, detail='Not found')