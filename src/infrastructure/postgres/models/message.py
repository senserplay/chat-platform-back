from sqlalchemy import Column, Integer, Text, ForeignKey, UUID
from sqlalchemy.orm import relationship
from .mixin import TimestampMixin
from ..client import Base


class Message(Base, TimestampMixin):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_uuid = Column(UUID(as_uuid=True), ForeignKey('chats.uuid'), nullable=False)
    text = Column(Text, nullable=False)

    # Relationships
    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")