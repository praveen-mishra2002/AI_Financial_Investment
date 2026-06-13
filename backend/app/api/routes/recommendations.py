"""Recommendation and analysis routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.recommendation import (
    PortfolioAnalysisRead,
    PortfolioAnalysisRequest,
    RecommendationRequest,
    RecommendationRunRead,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/recommendations", response_model=RecommendationRunRead)
async def generate_recommendations(
    payload: RecommendationRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RecommendationRunRead:
    """Generate stock recommendations."""
    return await RecommendationService(db).generate(user, payload)


@router.post("/portfolio/analyze", response_model=PortfolioAnalysisRead)
async def analyze_portfolio(
    payload: PortfolioAnalysisRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PortfolioAnalysisRead:
    """Analyze portfolio holdings."""
    return await RecommendationService(db).analyze_portfolio(user, payload.portfolio_id)
