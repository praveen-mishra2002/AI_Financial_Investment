"""Agent input and output types."""

from decimal import Decimal
from typing import TypedDict


class MarketMetrics(TypedDict, total=False):
    """Normalized market and fundamental metrics."""

    ticker: str
    company_name: str | None
    sector: str | None
    market_cap: float | None
    pe_ratio: float | None
    pb_ratio: float | None
    revenue_growth: float | None
    operating_margin: float | None
    debt_to_equity: float | None
    free_cash_flow: float | None
    roe: float | None


class Candidate(TypedDict, total=False):
    """Recommendation candidate."""

    ticker: str
    company_name: str | None
    sector: str | None


class HoldingInput(TypedDict):
    """Portfolio risk holding input."""

    ticker: str
    sector: str | None
    value: Decimal
