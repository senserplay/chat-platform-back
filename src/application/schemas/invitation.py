import uuid
from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from src.application.schemas.base_model import BaseModelMixin


# Базовая схема для создания чата
class InvitationCreate(BaseModelMixin):
    email: EmailStr
    chat_uuid: uuid.UUID


# Полная схема для вывода информации о чате
class InvitationSchema(BaseModelMixin):
    token: uuid.UUID
    email: EmailStr
    chat_uuid: uuid.UUID
    is_accepted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
