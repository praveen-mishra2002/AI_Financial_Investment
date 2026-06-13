"""Authentication routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth import LoginRequest, TokenPair, UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    """Register a user."""
    return await AuthService(db).register(payload)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenPair:
    """Login a user."""
    return await AuthService(db).login(payload)
