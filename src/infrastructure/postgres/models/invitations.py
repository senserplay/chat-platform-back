from sqlalchemy import Column, Integer, Boolean, ForeignKey, UUID, String
from sqlalchemy.orm import relationship
from .mixin import TimestampMixin
import uuid

from ..client import Base


class Invitation(Base, TimestampMixin):
    __tablename__ = 'invitations'

    token = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    chat_uuid = Column(UUID(as_uuid=True), ForeignKey('chats.uuid'), nullable=False)
    email = Column(String, nullable=False)
    is_accepted = Column(Boolean, nullable=False)

    chat = relationship("Chat", back_populates="chat_invitations")
