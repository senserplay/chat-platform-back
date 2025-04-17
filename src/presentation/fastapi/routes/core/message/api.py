from typing import List

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession

from src.application.schemas.user import UserSchema
from src.infrastructure.postgres.client import get_db_session
from src.infrastructure.postgres.repositories.message import (
    messages_repository,
    MessageNotFoundError, AccessDeniedError,
)
from src.presentation.fastapi.middlewares import get_current_user
from src.application.schemas.message import MessageSchema, MessageCreate

ROUTER = APIRouter(prefix="/message")


@ROUTER.post(
    "",
    response_model=MessageCreate,
    summary="Отправить сообщение",
)
async def send_message(
        request: MessageCreate, user: UserSchema = Depends(get_current_user), db_session: DBSession = Depends(get_db_session)
) -> MessageSchema:
    return messages_repository.create_message(db_session, request, user.id)


@ROUTER.get(
    "/chat/{chat_uuid}",
    response_model=List[MessageSchema],
    summary="Получить сообщения чата",
)
async def get_chat_messages(chat_uuid: uuid, db_session: DBSession = Depends(get_db_session)) -> List[MessageSchema]:
    return messages_repository.get_chat_messages(db_session, chat_uuid)


@ROUTER.delete(
    "/{message_id}",
    summary="Удалить сообщение",
)
async def delete_message(
        message_id: int,
        user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session),
):
    try:
        messages_repository.delete_message(db_session, message_id, user.id)
        return {"status": "ok"}
    except MessageNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=str(e)
        )
    except AccessDeniedError as e:
        raise HTTPException(
            status_code=403, detail=str(e)
        )