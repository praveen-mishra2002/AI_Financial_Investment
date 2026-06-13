"""Portfolio service."""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portfolio import Holding, Portfolio
from app.models.user import User
from app.repositories.audit import AuditRepository
from app.repositories.portfolios import PortfolioRepository
from app.schemas.portfolio import HoldingCreate, HoldingUpdate, PortfolioCreate, PortfolioUpdate


class PortfolioService:
    """Portfolio workflows."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.portfolios = PortfolioRepository(db)
        self.audit = AuditRepository(db)

    async def create(self, user: User, payload: PortfolioCreate) -> Portfolio:
        """Create a portfolio."""
        portfolio = await self.portfolios.create(Portfolio(user_id=user.id, **payload.model_dump()))
        await self.audit.record(user.id, "portfolio.created", {"portfolio_id": portfolio.id})
        await self.db.commit()
        return portfolio

    async def get(self, user: User, portfolio_id: str) -> Portfolio:
        """Get a portfolio."""
        portfolio = await self.portfolios.get_for_user(portfolio_id, user.id)
        if portfolio is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
        return portfolio

    async def list(self, user: User) -> list[Portfolio]:
        """List portfolios."""
        return await self.portfolios.list_for_user(user.id)

    async def update(self, user: User, portfolio_id: str, payload: PortfolioUpdate) -> Portfolio:
        """Update a portfolio."""
        portfolio = await self.get(user, portfolio_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(portfolio, field, value)
        await self.audit.record(user.id, "portfolio.updated", {"portfolio_id": portfolio.id})
        await self.db.commit()
        await self.db.refresh(portfolio, ["holdings"])
        return portfolio

    async def delete(self, user: User, portfolio_id: str) -> None:
        """Delete a portfolio."""
        portfolio = await self.get(user, portfolio_id)
        await self.portfolios.delete(portfolio)
        await self.audit.record(user.id, "portfolio.deleted", {"portfolio_id": portfolio_id})
        await self.db.commit()

    async def add_holding(self, user: User, portfolio_id: str, payload: HoldingCreate) -> Holding:
        """Add a holding to a portfolio."""
        await self.get(user, portfolio_id)
        holding = await self.portfolios.add_holding(Holding(portfolio_id=portfolio_id, **payload.model_dump()))
        await self.audit.record(user.id, "holding.created", {"portfolio_id": portfolio_id, "holding_id": holding.id})
        await self.db.commit()
        return holding

    async def update_holding(self, user: User, holding_id: str, payload: HoldingUpdate) -> Holding:
        """Update a holding."""
        holding = await self.portfolios.get_holding_for_user(holding_id, user.id)
        if holding is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(holding, field, value)
        await self.audit.record(user.id, "holding.updated", {"holding_id": holding_id})
        await self.db.commit()
        await self.db.refresh(holding)
        return holding

    async def delete_holding(self, user: User, holding_id: str) -> None:
        """Delete a holding."""
        holding = await self.portfolios.get_holding_for_user(holding_id, user.id)
        if holding is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holding not found")
        await self.portfolios.delete(holding)
        await self.audit.record(user.id, "holding.deleted", {"holding_id": holding_id})
        await self.db.commit()
