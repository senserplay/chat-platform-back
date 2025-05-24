from uuid import UUID

from sqlalchemy.orm import Session

from src.application.schemas.chat import (
    ChatSchema,
    ChatUpdate,
    ChatCreate,
)
from src.infrastructure.postgres.client import SessionLocal
from src.infrastructure.postgres.repositories.chat import chats_repository
from src.infrastructure.redis.storage.redis_storage import RedisStorage


class ChatsStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="chats")

    def add_chat(self, chat: ChatSchema, ttl=3600):
        chat_data = chat.model_dump(mode='json')
        self.hash_set(str(chat.uuid), chat_data, ttl)

    def get_chat(self, chat_uuid: UUID) -> ChatSchema:
        if not self.hash_exists(str(chat_uuid)):
            with SessionLocal() as session:
                chat = chats_repository.get_chat(session, chat_uuid)
                self.add_chat(chat)
        chat_data = self.hash_get(str(chat_uuid))
        chat = ChatSchema(**chat_data)
        return chat

    def create_chat(self, session: Session, chat_data: ChatCreate, owner_id: int) -> ChatSchema:
        new_chat = chats_repository.create_chat(session, chat_data, owner_id)
        self.add_chat(new_chat)
        return new_chat

    def delete_chat(self, session: Session, chat_uuid: UUID, user_id: int):
        chats_repository.delete_chat(session, chat_uuid, user_id)
        self.hash_delete(str(chat_uuid))

    def update_chat(
            self, session: Session, chat_data: ChatUpdate, user_id: int
    ) -> ChatSchema:
        chat = chats_repository.update_chat(session, chat_data, user_id)
        self.add_chat(chat)
        return chat


chats_storage = ChatsStorage()
