"""Recommendation and analysis schemas."""

from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.models.recommendation import RecommendationAction


class StockCandidate(BaseModel):
    """Stock candidate input for recommendation generation."""

    ticker: str = Field(min_length=1, max_length=24)
    company_name: str | None = None
    sector: str | None = None

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        """Normalize ticker symbols."""
        return value.strip().upper()


class RecommendationRequest(BaseModel):
    """Recommendation generation request."""

    investment_amount: Decimal = Field(gt=0)
    candidates: list[StockCandidate] = Field(min_length=1)


class Explanation(BaseModel):
    """Explainability payload."""

    summary: str
    key_strengths: list[str]
    key_risks: list[str]
    confidence_commentary: str


class RecommendationRead(BaseModel):
    """Recommendation response item."""

    id: str | None = None
    ticker: str
    company_name: str | None = None
    sector: str | None = None
    action: RecommendationAction
    final_score: Decimal
    confidence: Decimal
    allocation_amount: Decimal | None = None
    reason_codes: list[str]
    explanation: Explanation
    metrics_snapshot: dict

    model_config = {"from_attributes": True}


class RecommendationRunRead(BaseModel):
    """Recommendation run response."""

    id: str
    recommendations: list[RecommendationRead]


class PortfolioAnalysisRequest(BaseModel):
    """Portfolio analysis request."""

    portfolio_id: str


class HoldingAnalysisRead(BaseModel):
    """Holding analysis response item."""

    ticker: str
    action: RecommendationAction
    score: Decimal
    rationale: str


class PortfolioAnalysisRead(BaseModel):
    """Portfolio analysis response."""

    id: str | None = None
    risk_score: Decimal
    warnings: list[str]
    recommendations: list[str]
    holdings: list[HoldingAnalysisRead]


class StockRead(BaseModel):
    """Market data response."""

    ticker: str
    metrics: dict
