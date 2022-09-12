from fastapi import APIRouter, Depends

from src.apps.auth.services import get_current_verified_active_superuser
from src.apps.categories.schemas import CategoryOut, CategoryIn
from src.apps.categories.services import CategoryService
from src.apps.user import models

category_router = APIRouter()


@category_router.post('/', response_model=CategoryOut)
async def create_category(
    new_category: CategoryIn,
    current_superuser: models.User = Depends(get_current_verified_active_superuser)
):
    created_category = await CategoryService.create(new_category)
    return created_category


@category_router.get('/all/', response_model=list[CategoryOut])
async def get_all_categories():
    categories = await CategoryService.all()
    return categories


@category_router.put('/{category_id}/', response_model=CategoryOut)
async def update_category(
    to_update: CategoryIn,
    category_id: int,
    current_superuser: models.User = Depends(get_current_verified_active_superuser)
):
    updated_category = await CategoryService.update_and_get(to_update, id=category_id)
    return updated_category


@category_router.delete('/{category_id}/')
async def delete_category(
    category_id: int,
    current_superuser: models.User = Depends(get_current_verified_active_superuser)
):
    response = await CategoryService.delete(id=category_id)
    if response:
        return {'detail': response}
