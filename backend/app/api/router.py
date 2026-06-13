"""API router aggregation."""

from fastapi import APIRouter

from app.api.routes import auth, portfolio, recommendations, stocks

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(recommendations.router, prefix="", tags=["Recommendations"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])


@api_router.get("/health", tags=["Health"])
async def api_health() -> dict[str, str]:
    """Return API health."""
    return {"status": "ok"}
