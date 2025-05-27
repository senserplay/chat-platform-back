import uuid
from src.application.schemas.base_model import BaseModelMixin


# Базовая схема для добавления пользователя в чат
class ChatUserUpdate(BaseModelMixin):
    user_id: int
    chat_uuid: uuid.UUID

    class Config:
        arbitrary_types_allowed = True


# Полная схема для вывода информации о пользователе чата
class ChatUserSchema(BaseModelMixin):
    id: int
    user_id: int
    chat_uuid: uuid.UUID

    class Config:
        arbitrary_types_allowed = True
