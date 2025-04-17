import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from src.application.schemas.base_model import BaseModelMixin


# Базовая схема для создания чата
class ChatCreate(BaseModelMixin):
    owner_id: int


# Полная схема для вывода информации о чате
class ChatSchema(BaseModelMixin):
    uuid: uuid
    owner_id: int
    is_open: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


# Схема для обновления чата
class ChatUpdate(BaseModelMixin):
    uuid: uuid
    is_open: bool



