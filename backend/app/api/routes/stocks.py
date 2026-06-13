"""Stock routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.market_agent import MarketAgent
from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.recommendation import StockRead

router = APIRouter()


@router.get("/{ticker}", response_model=StockRead)
async def get_stock(ticker: str, _: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> StockRead:
    """Fetch normalized stock metrics."""
    metrics = await MarketAgent(db).fetch({"ticker": ticker.upper()})
    return StockRead(ticker=ticker.upper(), metrics=metrics)
