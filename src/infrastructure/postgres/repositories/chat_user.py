from typing import List

import uuid
from sqlalchemy.orm import Session

from src.application.schemas.chat import ChatSchema
from src.application.schemas.user import UserSchema
from src.infrastructure.postgres.models.chat_user import ChatUser
from src.application.schemas.chat_user import (
    ChatUserSchema,
    ChatUserUpdate,
)

from src.infrastructure.redis.storage.chat_storage import chats_storage
from src.infrastructure.redis.storage.user_storage import users_storage


class UserAlreadyExistsError(Exception):
    """Исключение, вызываемое, если пользователь уже существует"""

    def __str__(self):
        return "Пользователь уже присутствует в чате"


class UserNotFoundError(Exception):
    """Исключение, вызываемое, если пользователь не найден"""

    def __str__(self):
        return "Пользователь не найден"


class ChatUsersRepository:
    def add_user_to_chat(self, session: Session, chat_user_data: ChatUserUpdate) -> ChatUserSchema:
        chat_user = session.query(ChatUser).filter_by(chat_uuid=chat_user_data.chat_uuid,
                                                      user_id=chat_user_data.user_id).first()
        if chat_user:
            raise UserAlreadyExistsError()

        new_chat_user = ChatUser(**chat_user_data.model_dump())
        session.add(new_chat_user)
        session.commit()
        session.refresh(new_chat_user)

        return ChatUserSchema.model_validate(new_chat_user)

    def get_user_chats(self, session: Session, user_id: int) -> List[ChatSchema]:
        user_chats = session.query(ChatUser).filter_by(user_id=user_id).all()
        return [chats_storage.get_chat(user_chat.chat_uuid) for user_chat in user_chats]

    def get_chat_users(self, session: Session, chat_uuid: uuid.UUID) -> List[UserSchema]:
        chat_users = session.query(ChatUser).filter_by(chat_uuid=chat_uuid).all()
        return [users_storage.get_user(chat_user.user_id) for chat_user in chat_users]

    def delete_user_from_chat(self, session: Session, chat_user_data: ChatUserUpdate):
        chat_user = session.query(ChatUser).filter_by(user_id=chat_user_data.user_id).filter_by(
            chat_uuid=chat_user_data.chat_uuid).first()
        if not chat_user:
            raise UserNotFoundError
        session.delete(chat_user)
        session.commit()


chat_users_repository = ChatUsersRepository()
