from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from src.application.schemas.message import MessageSchema
from src.infrastructure.postgres.client import SessionLocal
from src.application.schemas.user import (
    UserCreate,
    UserUpdate,
    UserSchema,
)
from src.infrastructure.postgres.repositories.chat import chats_repository
from src.infrastructure.postgres.repositories.message import messages_repository
from src.infrastructure.postgres.repositories.user import users_repository
from src.infrastructure.redis.storage.redis_storage import RedisStorage


class MessagesStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="messages")

    def add_message(self, message: MessageSchema, ttl=3600):
        message_data = message.model_dump(mode='json')
        self.list_push(str(message.chat_uuid), message_data, ttl)

    def create_message(self, session: Session, message_data: MessageSchema) -> MessageSchema:
        new_message = messages_repository.create_message(session, message_data)
        self.add_message(new_message)
        return new_message

    def get_chat_messages(self, chat_uuid: UUID) -> List[MessageSchema]:
        if not self.exists(str(chat_uuid)):
            with SessionLocal() as session:
                chat_messages = messages_repository.get_chat_messages(session, chat_uuid)
                for message in chat_messages:
                    self.add_message(message)
        chat_messages = self.list_get(str(chat_uuid))
        for i in range(len(chat_messages)):
            chat_messages[i] = MessageSchema(**chat_messages[i])
        return chat_messages

    def delete_message(self, session: Session, message_id: int, user_id: int):
        message = messages_repository.get_message(session, message_id)
        messages_repository.delete_message(session, message_id, user_id)
        self.delete_key(str(message.chat_uuid))
        self.get_chat_messages(message.chat_uuid)


messages_storage = MessagesStorage()
