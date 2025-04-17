from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from src.application.schemas.base_model import BaseModelMixin


# Базовая схема для создания пользователя
class UserCreate(BaseModelMixin):
    username: str
    password: str
    email: EmailStr


# Полная схема для вывода информации о пользователе
class UserSchema(BaseModelMixin):
    id: int
    username: str
    password: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None


# Схема для обновления пользователя
class UserUpdate(BaseModelMixin):
    username: str
    password: str


class UserLogin(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserToken(BaseModel):
    token: str
