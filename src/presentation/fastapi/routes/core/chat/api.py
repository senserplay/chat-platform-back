from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession

from src.application.schemas.chat import (
    ChatSchema,
    ChatCreate,
    ChatUpdate,
)
from src.application.schemas.chat_user import ChatUserSchema, ChatUserUpdate
from src.application.schemas.user import UserSchema
from src.infrastructure.postgres.client import get_db_session
from src.infrastructure.postgres.repositories.chat import (
    chats_repository,
    ChatNotFoundError,
    AccessDeniedError,
)
from src.infrastructure.postgres.repositories.chat_user import chat_users_repository
from src.infrastructure.redis.storage.chat_storage import chats_storage
from src.presentation.fastapi.middlewares import get_current_user

ROUTER = APIRouter(prefix="/chat")


@ROUTER.post(
    "",
    response_model=ChatSchema,
    summary="Создание нового чата",
)
async def create_chat(
        request: ChatCreate, user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session)
) -> ChatSchema:
    new_chat = chats_storage.create_chat(db_session, request, user.id)
    chat_users_repository.add_user_to_chat(db_session, ChatUserUpdate(user_id=user.id, chat_uuid=new_chat.uuid))
    return new_chat


@ROUTER.get(
    "/{chat_uuid}",
    response_model=ChatSchema,
    summary="Получить чат",
)
async def get_chat(chat_uuid: UUID) -> ChatSchema:
    try:
        return chats_storage.get_chat(chat_uuid)
    except ChatNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@ROUTER.patch(
    "",
    response_model=ChatSchema,
    summary="Обновить чат"
)
async def update_chat(request: ChatUpdate,
                      user: UserSchema = Depends(get_current_user),
                      db_session: DBSession = Depends(get_db_session)
                      ) -> ChatSchema:
    try:
        return chats_storage.update_chat(db_session, request, user.id)
    except ChatNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDeniedError as e:
        raise HTTPException(status_code=404, detail=str(e))


@ROUTER.delete(
    "/{chat_uuid}",
    summary="Удалить чат"
)
async def delete_chat(chat_uuid: UUID,
                      user: UserSchema = Depends(get_current_user),
                      db_session: DBSession = Depends(get_db_session)):
    try:
        chats_storage.delete_chat(db_session, chat_uuid, user.id)
        return {"status": "ok"}
    except ChatNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))


@ROUTER.get(
    "/users/{chat_uuid}",
    response_model=List[UserSchema],
    summary="Поучить пользователей чата"
)
async def get_chat_users(chat_uuid: UUID, db_session: DBSession = Depends(get_db_session)):
    users_list = chat_users_repository.get_chat_users(db_session, chat_uuid)
    return users_list
