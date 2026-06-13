"""Portfolio repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.portfolio import Holding, Portfolio


class PortfolioRepository:
    """Database access for portfolios and holdings."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, portfolio: Portfolio) -> Portfolio:
        """Create a portfolio."""
        self.db.add(portfolio)
        await self.db.flush()
        await self.db.refresh(portfolio, ["holdings"])
        return portfolio

    async def get_for_user(self, portfolio_id: str, user_id: str) -> Portfolio | None:
        """Return a portfolio owned by a user."""
        stmt = (
            select(Portfolio)
            .options(selectinload(Portfolio.holdings))
            .where(Portfolio.id == portfolio_id, Portfolio.user_id == user_id)
        )
        return await self.db.scalar(stmt)

    async def list_for_user(self, user_id: str) -> list[Portfolio]:
        """List portfolios owned by a user."""
        result = await self.db.scalars(
            select(Portfolio).options(selectinload(Portfolio.holdings)).where(Portfolio.user_id == user_id)
        )
        return list(result)

    async def get_holding_for_user(self, holding_id: str, user_id: str) -> Holding | None:
        """Return a holding through portfolio ownership."""
        stmt = select(Holding).join(Portfolio).where(Holding.id == holding_id, Portfolio.user_id == user_id)
        return await self.db.scalar(stmt)

    async def add_holding(self, holding: Holding) -> Holding:
        """Create a holding."""
        self.db.add(holding)
        await self.db.flush()
        await self.db.refresh(holding)
        return holding

    async def delete(self, entity: Portfolio | Holding) -> None:
        """Delete an entity."""
        await self.db.delete(entity)
        await self.db.flush()
