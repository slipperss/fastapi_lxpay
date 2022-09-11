from fastapi import APIRouter

from src.apps.games.schemas import GameOut, GameIn
from src.apps.games.services import GameService

game_router = APIRouter()


@game_router.post('/', response_model=GameOut)
async def create_game(new_game: GameIn):
    created_game = await GameService.create(new_game)
    return created_game


@game_router.get('/all/', response_model=list[GameOut])
async def get_all_games():
    games = await GameService.all()
    return games


@game_router.put('/{game_id}/', response_model=GameOut)
async def update_game(to_update: GameIn, game_id: int):
    updated_game = await GameService.update_and_get(to_update, id=game_id)
    return updated_game


@game_router.delete('/{game_id}/')
async def delete_game(game_id: int):
    response = await GameService.delete(id=game_id)
    if response:
        return {'detail': response}
