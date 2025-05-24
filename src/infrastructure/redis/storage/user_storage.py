from sqlalchemy.orm import Session

from src.infrastructure.postgres.client import SessionLocal
from src.application.schemas.user import (
    UserCreate,
    UserUpdate,
    UserSchema,
)
from src.infrastructure.postgres.repositories.user import users_repository
from src.infrastructure.redis.storage.redis_storage import RedisStorage


class UsersStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="users")

    def add_user(self, user: UserSchema, ttl=3600):
        user_data = user.model_dump(mode='json')
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
        user_data = self.hash_get(str(user_id))
        user = UserSchema(**user_data)
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
