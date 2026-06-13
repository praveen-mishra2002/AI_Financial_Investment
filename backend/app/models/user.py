"""User model."""

from enum import StrEnum

from sqlalchemy import Boolean, Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class UserRole(StrEnum):
    """Supported user roles."""

    ADMIN = "ADMIN"
    INVESTOR = "INVESTOR"


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Application user."""

    __tablename__ = "users"
    __table_args__ = (Index("ix_users_email", "email", unique=True),)

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.INVESTOR)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
