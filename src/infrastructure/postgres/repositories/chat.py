from typing import List

from sqlalchemy.orm import Session

from src.infrastructure.postgres.models.chat import Chat
from src.application.schemas.chat import (
    ChatSchema,
    ChatUpdate,
    ChatCreate,
)


class ChatNotFoundError(Exception):
    """Исключение, вызываемое, если чат не найден"""

    def __str__(self):
        return "Чат не найден"


class AccessDeniedError(Exception):
    """Исключение, вызываемое, если нет прав на совершение действия"""

    def __str__(self):
        return "Вы не можете выполнить данную операцию"


class ChatsRepository:
    def get_chat(self, session: Session, chat_uuid) -> ChatSchema:
        chat = session.query(Chat).filter_by(uuid=chat_uuid).first()
        if not chat:
            raise ChatNotFoundError
        return ChatSchema.model_validate(chat)

    def create_chat(self, session: Session, chat_data: ChatCreate, owner_id: int) -> ChatSchema:
        new_chat = Chat(**chat_data.model_dump(), owner_id=owner_id)
        session.add(new_chat)
        session.commit()
        session.refresh(new_chat)

        return ChatSchema.model_validate(new_chat)

    def get_user_owned_chats(self, session: Session, user_id: int) -> List[ChatSchema]:
        user_owned_chats = session.query(Chat).filter_by(owner_id=user_id).all()
        return [ChatSchema.model_validate(chat) for chat in user_owned_chats]

    def delete_chat(self, session: Session, chat_uuid: int, user_id: int):
        chat = session.query(Chat).filter_by(uuid=chat_uuid).first()
        if not chat:
            raise ChatNotFoundError
        if chat.owner_id != user_id:
            raise AccessDeniedError
        session.delete(chat)
        session.commit()

    def update_chat(
            self, session: Session, chat_data: ChatUpdate, user_id: int
    ) -> ChatSchema:
        chat = session.query(Chat).filter_by(uuid=chat_data.uuid).first()
        if not chat:
            raise ChatNotFoundError
        if chat.owner_id != user_id:
            raise AccessDeniedError
        if chat_data.is_open is not None:
            chat.is_open = chat_data.is_open
        if chat_data.title is not None:
            chat.title = chat_data.title
        session.commit()
        session.refresh(chat)
        return ChatSchema.model_validate(chat)


chats_repository = ChatsRepository()
