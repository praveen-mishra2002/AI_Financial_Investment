"""Declarative base and reusable model mixins."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


class UUIDPrimaryKeyMixin:
    """String UUID primary key mixin."""

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))


class TimestampMixin:
    """Created and updated timestamp mixin."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
