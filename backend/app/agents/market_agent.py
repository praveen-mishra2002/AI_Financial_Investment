"""Market data acquisition agent."""

from datetime import UTC, datetime, timedelta
from typing import Any

import structlog
import yfinance as yf
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_exponential

from app.agents.types import Candidate, MarketMetrics
from app.models.recommendation import MarketCache

logger = structlog.get_logger(__name__)


class MarketAgent:
    """Fetch and normalize equity metrics from Yahoo Finance with database caching."""

    def __init__(self, db: AsyncSession | None = None, cache_ttl_hours: int = 12) -> None:
        self.db = db
        self.cache_ttl = timedelta(hours=cache_ttl_hours)

    async def fetch(self, candidate: Candidate) -> MarketMetrics:
        """Fetch normalized market metrics for a candidate."""
        ticker = self._format_ticker(candidate["ticker"])
        cached = await self._get_cache(ticker)
        if cached is not None:
            return cached
        metrics = await self._fetch_yahoo(ticker, candidate)
        await self._set_cache(ticker, metrics)
        return metrics

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4))
    async def _fetch_yahoo(self, ticker: str, candidate: Candidate) -> MarketMetrics:
        """Retrieve metrics from Yahoo Finance."""
        logger.info("market_agent.fetch", ticker=ticker)
        try:
            info: dict[str, Any] = yf.Ticker(ticker).info
        except Exception as exc:
            logger.warning("market_agent.yahoo_failed", ticker=ticker, error=str(exc))
            info = {}
        return {
            "ticker": candidate["ticker"],
            "company_name": candidate.get("company_name") or info.get("longName"),
            "sector": candidate.get("sector") or info.get("sector"),
            "market_cap": self._float(info.get("marketCap")),
            "pe_ratio": self._float(info.get("trailingPE")),
            "pb_ratio": self._float(info.get("priceToBook")),
            "revenue_growth": self._float(info.get("revenueGrowth")),
            "operating_margin": self._float(info.get("operatingMargins")),
            "debt_to_equity": self._float(info.get("debtToEquity")),
            "free_cash_flow": self._float(info.get("freeCashflow")),
            "roe": self._float(info.get("returnOnEquity")),
        }

    async def _get_cache(self, ticker: str) -> MarketMetrics | None:
        """Return non-expired cached metrics if available."""
        if self.db is None:
            return None
        cached = await self.db.scalar(select(MarketCache).where(MarketCache.ticker == ticker))
        if cached and cached.expires_at > datetime.now(UTC):
            return cached.payload
        return None

    async def _set_cache(self, ticker: str, metrics: MarketMetrics) -> None:
        """Store metrics in cache."""
        if self.db is None:
            return
        cached = await self.db.scalar(select(MarketCache).where(MarketCache.ticker == ticker))
        if cached is None:
            cached = MarketCache(ticker=ticker, payload=metrics, expires_at=datetime.now(UTC) + self.cache_ttl)
            self.db.add(cached)
        else:
            cached.payload = metrics
            cached.expires_at = datetime.now(UTC) + self.cache_ttl
        await self.db.flush()

    @staticmethod
    def _format_ticker(ticker: str) -> str:
        """Convert a plain NSE ticker to Yahoo Finance format."""
        normalized = ticker.strip().upper()
        return normalized if "." in normalized else f"{normalized}.NS"

    @staticmethod
    def _float(value: Any) -> float | None:
        """Safely coerce numeric values."""
        try:
            return None if value is None else float(value)
        except (TypeError, ValueError):
            return None
