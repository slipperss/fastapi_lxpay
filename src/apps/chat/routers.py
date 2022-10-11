import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates

from starlette.responses import HTMLResponse

from .schemas import MessageOut, ChatOut, ChatIn
from .services import ChatService
from ..auth.services import get_current_verified_active_user
from ..user.models import User


chat_router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@chat_router.get('/my-chats/')
async def get_all_user_chats(current_user: User = Depends(get_current_verified_active_user)):
    chats = await ChatService.get_all_user_chats(current_user.id)
    return chats


@chat_router.post('/create/', response_model=ChatOut)
async def create_chat(
        new_chat: ChatIn,
        current_user: User = Depends(get_current_verified_active_user)
):
    if new_chat.members[0].user_id == new_chat.members[1].user_id:
        raise HTTPException(status_code=405, detail="There can't be two identical users in a chat")
    obj = await ChatService.chat_create(new_chat)
    return obj


@chat_router.get('/history/{chat_id}', response_model=list[MessageOut])
async def get_chat_history(
        chat_id: uuid.UUID,
        current_user: User = Depends(get_current_verified_active_user)
):
    messages = await ChatService.get_all_messages_in_chat(chat_id)
    return messages


@chat_router.get('/test/', response_class=HTMLResponse)
async def test_chat(request: Request):
    return templates.TemplateResponse('socketio.html', {'request': request})
