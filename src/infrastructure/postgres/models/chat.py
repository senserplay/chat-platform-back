from sqlalchemy import Column, Integer, Boolean, ForeignKey, UUID, String
from sqlalchemy.orm import relationship
from .mixin import TimestampMixin
import uuid

from ..client import Base


class Chat(Base, TimestampMixin):
    __tablename__ = 'chats'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_open = Column(Boolean, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="owned_chats")
    users = relationship("ChatUser", back_populates="chat", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")