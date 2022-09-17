from fastapi import APIRouter, Depends

from src.apps.auth.services import get_current_verified_active_superuser
from src.apps.games.schemas import GameOut, GameIn
from src.apps.games.services import GameService
from src.apps.user import models

game_router = APIRouter()


@game_router.post('/', response_model=GameOut)
async def create_game(
    new_game: GameIn,
    current_superuser: models.User = Depends(get_current_verified_active_superuser)
):
    created_game = await GameService.create(new_game)
    return created_game


@game_router.get('/all/')#, response_model=list[GameOut])
async def get_all_games():
    games = await GameService.all()
    #values=('id', 'name', 'category_id', 'category__name'))
    return games


@game_router.put('/{game_id}/', response_model=GameOut)
async def update_game(
    to_update: GameIn,
    game_id: int,
    current_superuser: models.User = Depends(get_current_verified_active_superuser)
):
    updated_game = await GameService.update_and_get(to_update, id=game_id)
    return updated_game


@game_router.delete('/{game_id}/')
async def delete_game(
    game_id: int,
    current_superuser: models.User = Depends(get_current_verified_active_superuser)
):
    response = await GameService.delete(id=game_id)
    if response:
        return {'detail': response}
