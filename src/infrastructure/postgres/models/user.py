from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .mixin import TimestampMixin
from ..client import Base


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)

    # Relationships
    owned_chats = relationship("Chat", back_populates="owner", cascade="all, delete-orphan")
    chats = relationship("ChatUser", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
