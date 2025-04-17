from sqlalchemy.orm import Session

from src.infrastructure.postgres.models.user import User
from src.application.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserSchema,
)
from src.core.auth_service import auth_service


class UserAlreadyExistsError(Exception):
    """Исключение, вызываемое, если пользователь уже существует"""

    def __str__(self):
        return "Пользователь с указанными данными уже существует"


class UserNotFoundError(Exception):
    """Исключение, вызываемое, если пользователь не найден"""

    def __str__(self):
        return "Пользователь не найден"


class IncorrectPasswordError(Exception):
    """Исключение, вызываемое, если введен неверный пароль"""

    def __str__(self):
        return "Неверный пароль"


class UsersRepository:
    def create_user(self, session: Session, user_data: UserCreate) -> UserSchema:
        user = session.query(User).filter_by(email=user_data.email).first()
        if user:
            raise UserAlreadyExistsError()
        user_data.password = auth_service.hash_password(user_data.password)

        new_user = User(**user_data.model_dump())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return UserSchema.model_validate(new_user)

    def get_user(self, session: Session, user_id: int) -> UserSchema:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundError()
        return UserSchema.model_validate(user)

    def get_token(self, session: Session, user_data: UserLogin) -> str:
        user = session.query(User).filter_by(email=user_data.email).first()
        if not user:
            raise UserNotFoundError()
        else:
            if not auth_service.verify_password(
                    user_data.password, user.password
            ):
                raise IncorrectPasswordError()
            else:
                token = auth_service.create_access_token(user.id)
                return token

    def delete_user(self, session: Session, user_id: int):
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundError
        session.delete(user)
        session.commit()

    def update_user(
            self, session: Session, user_data: UserUpdate, user_id: int
    ) -> UserSchema:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundError
        if user_data.username:
            user.username = user_data.username
        if user_data.password:
            hashed_password = auth_service.hash_password(user_data.password)
            user.password = hashed_password
        session.commit()
        session.refresh(user)
        return UserSchema.model_validate(user)


users_repository = UsersRepository()
