import uuid
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

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v),
        }


# Схема для обновления пользователя
class UserUpdate(BaseModelMixin):
    username: Optional[str] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserToken(BaseModel):
    token: str
