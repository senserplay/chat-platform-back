import uuid
from datetime import datetime

from src.application.schemas.base_model import BaseModelMixin


# Базовая схема для создания сообщения
class MessageCreate(BaseModelMixin):
    chat_uuid: uuid
    text: str

    class Config:
        arbitrary_types_allowed = True


# Полная схема для вывода информации о сообщении
class MessageSchema(BaseModelMixin):
    id: int
    user_id: int
    chat_uuid: uuid
    text: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
