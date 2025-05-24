from uuid import UUID

from sqlalchemy.orm import Session

from src.infrastructure.postgres.client import SessionLocal
from src.application.schemas.user import (
    UserCreate,
    UserUpdate,
    UserSchema,
)
from src.infrastructure.postgres.repositories.chat import chats_repository
from src.infrastructure.postgres.repositories.user import users_repository
from src.infrastructure.redis.storage.redis_storage import RedisStorage


class UsersStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="users")

    def add_user(self, user: UserSchema, ttl=3600):
        user_data = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "created_at": str(user.created_at),
            "updated_at": str(user.updated_at) if user.updated_at else user.updated_at
        }
        self.hash_set(str(user.id), user_data, ttl)

    def create_user(self, session: Session, user_data: UserCreate) -> UserSchema:
        new_user = users_repository.create_user(session, user_data)
        self.add_user(new_user)
        return new_user

    def get_user(self, user_id: int) -> UserSchema:
        if not self.hash_exists(str(user_id)):
            with SessionLocal() as session:
                user = users_repository.get_user(session, user_id)
                self.add_user(user)
        user = self.hash_get(str(user_id))
        return user

    def delete_user(self, session: Session, user_id: int):
        users_repository.delete_user(session, user_id)
        self.hash_delete(str(user_id))

    def update_user(
            self, session: Session, user_data: UserUpdate, user_id: int
    ) -> UserSchema:
        user = users_repository.update_user(session, user_data, user_id)
        self.add_user(user)
        return user


users_storage = UsersStorage()

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


class ChatsStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="chats")

    def add_chat(self, chat: ChatSchema, ttl=3600):
        chat_data = {
            "uuid": chat.uuid,
            "title": chat.title,
            "owner_id": chat.owner_id,
            "is_open": chat.is_open,
            "created_at": str(chat.created_at),
            "updated_at": str(chat.updated_at) if chat.updated_at else chat.updated_at
        }
        self.hash_set(str(chat.uuid), chat_data, ttl)

    def get_chat(self, chat_uuid: UUID) -> ChatSchema:
        if not self.hash_exists(str(chat_uuid)):
            with SessionLocal() as session:
                chat = chats_repository.get_chat(session, chat_uuid)
                self.add_chat(chat)
        chat_data = self.hash_get(str(chat_uuid))
        chat = ChatSchema(
            uuid=chat_data['uuid'],
            session_id=chat_data['title'],
            link=int(chat_data['owner_id']),
            status=bool(chat_data['is_open']),
            created_at=chat_data['created_at'],
            updated_at=chat_data['updated_at']
        )
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
