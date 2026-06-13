"""Sentiment analysis agent."""

import json

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


class SentimentAgent:
    """Analyze news sentiment. Returns neutral sentiment when OpenAI is unavailable."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def analyze(self, ticker: str, context: str | None = None) -> dict:
        """Return a 0-100 sentiment score and factors."""
        if self.client is None:
            return {
                "score": 50.0,
                "positive_factors": ["No live sentiment source configured"],
                "negative_factors": [],
                "summary": "Neutral sentiment applied because OpenAI is not configured.",
            }
        prompt = (
            "Analyze equity news sentiment for the Indian stock. Return JSON with score 0-100, "
            "positive_factors, negative_factors, and summary. Ticker: "
            f"{ticker}. Context: {context or 'No additional context'}"
        )
        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            return {
                "score": float(parsed.get("score", 50)),
                "positive_factors": list(parsed.get("positive_factors", [])),
                "negative_factors": list(parsed.get("negative_factors", [])),
                "summary": str(parsed.get("summary", "")),
            }
        except Exception:
            return {
                "score": 50.0,
                "positive_factors": [],
                "negative_factors": ["Sentiment service unavailable"],
                "summary": "Neutral sentiment applied due to external service failure.",
            }
