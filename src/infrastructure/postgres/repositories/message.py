from typing import List

import uuid
from sqlalchemy.orm import Session

from src.infrastructure.postgres.models.message import Message
from src.application.schemas.message import (
    MessageSchema,
    MessageCreate,
)


class MessageNotFoundError(Exception):
    """Исключение, вызываемое, если сообщение не найден"""

    def __str__(self):
        return "Сообщение не найден"


class AccessDeniedError(Exception):
    """Исключение, вызываемое, если нет прав на совершение действия"""

    def __str__(self):
        return "Вы не можете выполнить данную операцию"


class MessagesRepository:
    def create_message(self, session: Session, message_data: MessageCreate, user_id: int) -> MessageSchema:
        new_message = Message(**message_data.model_dump(), user_id=user_id)
        session.add(new_message)
        session.commit()
        session.refresh(new_message)

        return MessageSchema.model_validate(new_message)

    def get_chat_messages(self, session: Session, chat_uuid: uuid) -> List[MessageSchema]:
        chat_messages = session.query(Message).filter_by(chat_uuid=chat_uuid).all()
        return [MessageSchema.model_validate(chat_message) for chat_message in chat_messages]

    def delete_message(self, session: Session, message_id: int, user_id: int):
        message = session.query(Message).filter_by(id=message_id).first()
        if not message:
            raise MessageNotFoundError
        if message.user_id != user_id:
            raise AccessDeniedError
        session.delete(message)
        session.commit()


messages_repository = MessagesRepository()
