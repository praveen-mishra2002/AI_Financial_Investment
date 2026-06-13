"""Portfolio and holding models."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Portfolio(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User investment portfolio."""

    __tablename__ = "portfolios"
    __table_args__ = (Index("ix_portfolios_user_id", "user_id"),)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500))

    user = relationship("User", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")


class Holding(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Single stock holding inside a portfolio."""

    __tablename__ = "holdings"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "ticker", name="uq_holding_portfolio_ticker"),
        Index("ix_holdings_portfolio_id", "portfolio_id"),
    )

    portfolio_id: Mapped[str] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(24), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(160))
    sector: Mapped[str | None] = mapped_column(String(100))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    average_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")
