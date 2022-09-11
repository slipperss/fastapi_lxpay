from fastapi import APIRouter

from src.apps.categories.schemas import CategoryOut, CategoryIn
from src.apps.categories.services import CategoryService


category_router = APIRouter()


@category_router.post('/', response_model=CategoryOut)
async def create_category(new_category: CategoryIn):
    created_category = await CategoryService.create(new_category)
    return created_category


@category_router.get('/all/', response_model=list[CategoryOut])
async def get_all_categories():
    categories = await CategoryService.all()
    return categories


@category_router.put('/{category_id}/', response_model=CategoryOut)
async def update_category(to_update: CategoryIn, category_id: int):
    updated_category = await CategoryService.update_and_get(to_update, id=category_id)
    return updated_category


@category_router.delete('/{category_id}/')
async def delete_category(category_id: int):
    response = await CategoryService.delete(id=category_id)
    if response:
        return {'detail': response}
