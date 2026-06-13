"""Portfolio routes."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.portfolio import HoldingCreate, HoldingRead, HoldingUpdate, PortfolioCreate, PortfolioRead, PortfolioUpdate
from app.services.portfolio_service import PortfolioService

router = APIRouter()


@router.post("", response_model=PortfolioRead, status_code=201)
async def create_portfolio(payload: PortfolioCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Create a portfolio."""
    return await PortfolioService(db).create(user, payload)


@router.get("", response_model=list[PortfolioRead])
async def list_portfolios(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """List portfolios."""
    return await PortfolioService(db).list(user)


@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def get_portfolio(portfolio_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get a portfolio."""
    return await PortfolioService(db).get(user, portfolio_id)


@router.put("/{portfolio_id}", response_model=PortfolioRead)
async def update_portfolio(portfolio_id: str, payload: PortfolioUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Update a portfolio."""
    return await PortfolioService(db).update(user, portfolio_id, payload)


@router.delete("/{portfolio_id}", status_code=204)
async def delete_portfolio(portfolio_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Delete a portfolio."""
    await PortfolioService(db).delete(user, portfolio_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{portfolio_id}/holding", response_model=HoldingRead, status_code=201)
async def add_holding(portfolio_id: str, payload: HoldingCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Add a holding."""
    return await PortfolioService(db).add_holding(user, portfolio_id, payload)


@router.put("/holding/{holding_id}", response_model=HoldingRead)
async def update_holding(holding_id: str, payload: HoldingUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Update a holding."""
    return await PortfolioService(db).update_holding(user, holding_id, payload)


@router.delete("/holding/{holding_id}", status_code=204)
async def delete_holding(holding_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Delete a holding."""
    await PortfolioService(db).delete_holding(user, holding_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
