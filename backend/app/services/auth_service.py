"""Authentication service."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User
from app.repositories.users import UserRepository
from app.schemas.auth import LoginRequest, TokenPair, UserCreate


class AuthService:
    """Register and authenticate users."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.users = UserRepository(db)

    async def register(self, payload: UserCreate) -> User:
        """Register a new user."""
        existing = await self.users.get_by_email(payload.email)
        if existing is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        user = User(
            email=payload.email.lower(),
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        await self.users.add(user)
        await self.db.commit()
        return user

    async def login(self, payload: LoginRequest) -> TokenPair:
        """Authenticate and return token pair."""
        user = await self.users.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return TokenPair(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            user=user,
        )
