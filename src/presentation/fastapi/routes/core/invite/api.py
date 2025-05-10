from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession

from src.application.schemas.chat import (
    ChatSchema,

)
from src.application.schemas.chat_user import ChatUserUpdate
from src.application.schemas.user import UserSchema
from src.core.config import env_settings
from src.infrastructure.postgres.client import get_db_session
from src.infrastructure.postgres.repositories.invitations import (
    invitations_repository,
    InvitationNotFoundError,
    InvitationSchema,
    InvitationCreate,
)
from src.infrastructure.postgres.repositories.chat import chats_repository
from src.infrastructure.postgres.repositories.chat_user import chat_users_repository
from src.presentation.fastapi.middlewares import get_current_user

from src.services.email import EmailSender

ROUTER = APIRouter(prefix="/invite")


@ROUTER.post(
    "",
    response_model=InvitationSchema,
    summary="Создание нового приглашения",
)
async def create_invitation(
        request: InvitationCreate, user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session)
) -> ChatSchema:
    user_owned_chats = chats_repository.get_user_owned_chats(db_session, user.id)
    if request.chat_uuid not in [chat.uuid for chat in user_owned_chats]:
        raise HTTPException(
            status_code=403, detail="Вы не являетесь создателем данного чата"
        )

    new_invitation = invitations_repository.create_invitation(db_session, request)
    subject = "Здравствуйте, на связи ChatPlatform!"
    html_content = f"""
                <h1>Вас пригласили в чат!</h1>
                <p>Для присоединения к чату, перейдите по ссылке.</p>
                <a href="{env_settings.BASE_URL}/invite/accept/{new_invitation.token} ">Присоединиться к чату</a>
            """
    EmailSender.send_email(request.email, subject=subject, html_content=html_content)
    return new_invitation


@ROUTER.post(
    "/accept/{token}",
    response_model=InvitationSchema,
    summary="Принять приглашение",
)
async def accept_invitation(token: UUID, user: UserSchema = Depends(get_current_user),
                            db_session: DBSession = Depends(get_db_session)) -> ChatSchema:
    try:
        invitation = invitations_repository.get_invitation(db_session, token)
    except InvitationNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=str(e)
        )

    if invitation.is_accepted:
        raise HTTPException(
            status_code=409, detail="Данное приглашение уже принято"
        )
    if invitation.email != user.email:
        raise HTTPException(
            status_code=403, detail="Приглашение было создано на другой email"
        )
    chat_users_repository.add_user_to_chat(db_session, ChatUserUpdate(user_id=user.id, chat_uuid=invitation.chat_uuid))
    return invitations_repository.accept_invitation(db_session, token)
