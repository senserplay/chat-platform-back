from sqlalchemy import Column, TIMESTAMP, func
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """
    Миксин для добавления полей created_at и updated_at.
    """
    @declared_attr
    def created_at(cls):
        return Column(TIMESTAMP, nullable=False, server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
