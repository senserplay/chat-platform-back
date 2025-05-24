import uuid
from datetime import datetime
from typing import Optional

from src.application.schemas.base_model import BaseModelMixin


# Базовая схема для создания чата
class ChatCreate(BaseModelMixin):
    title: str


# Полная схема для вывода информации о чате
class ChatSchema(BaseModelMixin):
    uuid: uuid.UUID
    title: str
    owner_id: int
    is_open: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v),
        }


# Схема для обновления чата
class ChatUpdate(BaseModelMixin):
    uuid: uuid.UUID
    title: Optional[str] = None
    is_open: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True



