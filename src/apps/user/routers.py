import uuid

from fastapi import APIRouter, Depends

from src.apps.auth.services import get_current_verified_active_user
from src.apps.user import models
from src.apps.user.services import UserService
from src.apps.user.schemas import UserOut, UserUpdate

user_router = APIRouter()


@user_router.get('/me/', response_model=UserOut)
async def read_users_me(current_user: models.User = Depends(get_current_verified_active_user)):
    return current_user


@user_router.get('/{user_id}/', response_model=UserOut)
async def get_user_by_id(user_id: uuid.UUID):
    user = await UserService.get(id=user_id)
    return user


@user_router.put('/update/', response_model=UserOut)
async def update_user(
        to_update: UserUpdate,
        current_user: models.User = Depends(get_current_verified_active_user)
):
    updated_user = await UserService.update_and_get(to_update, id=current_user.id)
    return updated_user


@user_router.delete('/delete/{user_id}/')
async def delete_user(user_id: uuid.UUID):
    response = await UserService.delete(id=user_id)
    if response:
        return {'detail': response}
