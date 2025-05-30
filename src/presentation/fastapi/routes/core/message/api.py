from typing import List

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession

from src.application.schemas.user import UserSchema
from src.infrastructure.postgres.client import get_db_session
from src.infrastructure.postgres.repositories.chat_user import chat_users_repository
from src.infrastructure.postgres.repositories.message import (
    MessageNotFoundError, AccessDeniedError,
)
from src.infrastructure.redis.storage.message_storage import messages_storage
from src.presentation.fastapi.middlewares import get_current_user
from src.application.schemas.message import MessageSchema, MessageCreate, MessageWithUsernameSchema
from src.presentation.fastapi.websockets.message.ws import notify_user
from src.infrastructure.redis.storage.user_storage import users_storage

ROUTER = APIRouter(prefix="/message")


@ROUTER.post(
    "",
    response_model=MessageCreate,
    summary="Отправить сообщение",
)
async def send_message(
        request: MessageCreate, user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session)
) -> MessageSchema:
    message = messages_storage.create_message(db_session, request, user.id)
    message_with_username = MessageWithUsernameSchema(username=user.username, message=message)
    for user in chat_users_repository.get_chat_users(db_session, request.chat_uuid):
        await notify_user(user.id, message.chat_uuid, message_with_username)
    return message


@ROUTER.get(
    "/chat/{chat_uuid}",
    response_model=List[MessageWithUsernameSchema],
    summary="Получить сообщения чата",
)
async def get_chat_messages(chat_uuid: UUID) -> List[MessageWithUsernameSchema]:
    messages = messages_storage.get_chat_messages(chat_uuid)
    messages_with_username = []
    for message in messages:
        user = users_storage.get_user(message.user_id)
        messages_with_username.append(MessageWithUsernameSchema(username=user.username, message=message))
    return messages_with_username


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
        messages_storage.delete_message(db_session, message_id, user.id)
        return {"status": "ok"}
    except MessageNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=str(e)
        )
    except AccessDeniedError as e:
        raise HTTPException(
            status_code=403, detail=str(e)
        )
