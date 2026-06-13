"""Audit repository."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.recommendation import AuditLog


class AuditRepository:
    """Database access for audit events."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def record(self, user_id: str | None, event_type: str, payload: dict) -> AuditLog:
        """Record an audit event."""
        event = AuditLog(user_id=user_id, event_type=event_type, payload=payload)
        self.db.add(event)
        await self.db.flush()
        return event
