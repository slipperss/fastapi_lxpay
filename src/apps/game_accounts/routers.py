import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.apps.game_accounts.schemas import GameAccountIn, GameAccountOut, GameAccountUpdate, GameAccountDetailOut
from src.apps.game_accounts.services import GameAccountService
from src.apps.auth.services import get_current_verified_active_user
from src.apps.user import models

game_account_router = APIRouter()


@game_account_router.get('/all/{game_id}/', response_model=list[GameAccountOut])
async def get_all_user_accounts_by_game(game_id: int):
    game_accounts = await GameAccountService.filter(game_id=game_id, is_published=True)
    return game_accounts


@game_account_router.get('/{game_account_id}/', response_model=GameAccountDetailOut)
async def get_all_user_accounts_by_id(game_account_id: uuid.UUID):
    game_account = await GameAccountService.get(id=game_account_id, is_published=True)
    return game_account


@game_account_router.post('/', response_model=GameAccountDetailOut)
async def create_user_game_account_for_sale(
    new_account: GameAccountIn,
    current_user: models.User = Depends(get_current_verified_active_user)
):
    created_game_account = await GameAccountService.create_and_get(new_account, seller_id=current_user.id)
    return created_game_account


@game_account_router.get('/my', response_model=list[GameAccountOut])
async def get_all_user_game_accounts_for_sale(
    current_user: models.User = Depends(get_current_verified_active_user)
):
    game_accounts = await GameAccountService.filter(seller_id=current_user.id)
    return game_accounts


@game_account_router.put('/{game_account_id}/', response_model=GameAccountDetailOut)
async def update_user_game_account_for_sale(
    to_update: GameAccountUpdate,
    game_account_id: uuid.UUID,
    current_user: models.User = Depends(get_current_verified_active_user)
):
    updated_game_account = await GameAccountService.update_and_get(to_update, id=game_account_id)
    return updated_game_account


@game_account_router.delete('/{game_account_id}/')
async def delete_user_game_account_for_sale(
    game_account_id: uuid.UUID,
    current_user: models.User = Depends(get_current_verified_active_user)
):
    response = await GameAccountService.delete(id=game_account_id)
    if response:
        return {'detail': response}
