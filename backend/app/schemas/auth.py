"""Authentication schemas."""

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    """Registration payload."""

    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    """User response."""

    id: str
    email: EmailStr
    full_name: str
    role: UserRole

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Login payload."""

    email: EmailStr
    password: str


class TokenPair(BaseModel):
    """Access and refresh JWT response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead
