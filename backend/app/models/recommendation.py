"""Recommendation, analysis, cache, and audit models."""

from decimal import Decimal
from enum import StrEnum

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class RecommendationAction(StrEnum):
    """Supported recommendation actions."""

    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    WATCH = "Watch"
    HOLD = "Hold"
    SELL = "Sell"


class RecommendationRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Auditable recommendation workflow execution."""

    __tablename__ = "recommendation_runs"
    __table_args__ = (Index("ix_recommendation_runs_user_id", "user_id"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    investment_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    input_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    agent_outputs: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    model_version: Mapped[str] = mapped_column(String(60), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(60), nullable=False, default="explainability-v1")

    recommendations = relationship("Recommendation", back_populates="run", cascade="all, delete-orphan")


class Recommendation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Single stock recommendation."""

    __tablename__ = "recommendations"
    __table_args__ = (Index("ix_recommendations_run_id", "run_id"), Index("ix_recommendations_ticker", "ticker"))

    run_id: Mapped[str] = mapped_column(ForeignKey("recommendation_runs.id", ondelete="CASCADE"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(24), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(160))
    sector: Mapped[str | None] = mapped_column(String(100))
    action: Mapped[RecommendationAction] = mapped_column(Enum(RecommendationAction), nullable=False)
    final_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    confidence: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    allocation_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    reason_codes: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    explanation: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    metrics_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    run = relationship("RecommendationRun", back_populates="recommendations")


class MarketCache(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Cached market data by ticker."""

    __tablename__ = "market_cache"
    __table_args__ = (Index("ix_market_cache_ticker", "ticker", unique=True),)

    ticker: Mapped[str] = mapped_column(String(24), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    expires_at = mapped_column(DateTime(timezone=True), nullable=False)


class SentimentCache(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Cached sentiment analysis by ticker."""

    __tablename__ = "sentiment_cache"
    __table_args__ = (Index("ix_sentiment_cache_ticker", "ticker", unique=True),)

    ticker: Mapped[str] = mapped_column(String(24), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    expires_at = mapped_column(DateTime(timezone=True), nullable=False)


class PortfolioAnalysisRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Portfolio analysis execution."""

    __tablename__ = "portfolio_analysis_runs"
    __table_args__ = (Index("ix_portfolio_analysis_runs_portfolio_id", "portfolio_id"),)

    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    risk_score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    warnings: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    recommendations: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    results = relationship("PortfolioAnalysisResult", back_populates="run", cascade="all, delete-orphan")


class PortfolioAnalysisResult(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Buy/Hold/Sell decision for a holding."""

    __tablename__ = "portfolio_analysis_results"
    __table_args__ = (Index("ix_portfolio_analysis_results_run_id", "run_id"),)

    run_id: Mapped[str] = mapped_column(ForeignKey("portfolio_analysis_runs.id", ondelete="CASCADE"), nullable=False)
    holding_id: Mapped[str] = mapped_column(ForeignKey("holdings.id", ondelete="CASCADE"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(24), nullable=False)
    action: Mapped[RecommendationAction] = mapped_column(Enum(RecommendationAction), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)

    run = relationship("PortfolioAnalysisRun", back_populates="results")


class AuditLog(UUIDPrimaryKeyMixin, Base):
    """Immutable audit event."""

    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_user_id", "user_id"), Index("ix_audit_logs_event_type", "event_type"))

    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
