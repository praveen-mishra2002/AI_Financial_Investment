"""Password hashing and JWT helpers."""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash."""
    return password_context.verify(password, hashed_password)


def create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    """Create a signed JWT."""
    expires_at = datetime.now(UTC) + expires_delta
    payload: dict[str, Any] = {"sub": subject, "exp": expires_at, "type": token_type}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    """Create an access token."""
    return create_token(subject, timedelta(minutes=settings.access_token_expire_minutes), "access")


def create_refresh_token(subject: str) -> str:
    """Create a refresh token."""
    return create_token(subject, timedelta(days=settings.refresh_token_expire_days), "refresh")


def decode_token(token: str, expected_type: str = "access") -> str:
    """Decode a JWT and return its subject."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
    if payload.get("type") != expected_type or not payload.get("sub"):
        raise ValueError("Invalid token type")
    return str(payload["sub"])
