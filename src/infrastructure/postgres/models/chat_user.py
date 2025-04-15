from sqlalchemy import Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship
from .mixin import TimestampMixin
from ..client import Base


class ChatUser(Base, TimestampMixin):
    __tablename__ = 'chat_users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_uuid = Column(UUID(as_uuid=True), ForeignKey('chats.uuid'), nullable=False)

    # Relationships
    user = relationship("User", back_populates="chats")
    chat = relationship("Chat", back_populates="users")
