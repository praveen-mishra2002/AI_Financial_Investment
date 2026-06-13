"""User repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Database access for users."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""
        return await self.db.scalar(select(User).where(User.email == email.lower()))

    async def get(self, user_id: str) -> User | None:
        """Return a user by id."""
        return await self.db.get(User, user_id)

    async def add(self, user: User) -> User:
        """Persist a user."""
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
