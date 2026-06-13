"""Explainability agent."""

import json

from openai import AsyncOpenAI

from app.core.config import settings


class ExplainabilityAgent:
    """Generate narratives for deterministic recommendations."""

    prompt_version = "explainability-v1"

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def explain(self, ticker: str, metrics: dict, scores: dict, decision: dict) -> dict:
        """Return explanation. The decision is an immutable input."""
        if self.client is None:
            return self._fallback(ticker, scores, decision)
        prompt = (
            "Explain this deterministic equity recommendation in JSON. Do not change the action. "
            "Fields: summary, key_strengths, key_risks, confidence_commentary. "
            f"Ticker: {ticker}. Metrics: {metrics}. Scores: {scores}. Decision: {decision}."
        )
        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            parsed = json.loads(response.choices[0].message.content or "{}")
            return {
                "summary": str(parsed.get("summary", "")),
                "key_strengths": list(parsed.get("key_strengths", [])),
                "key_risks": list(parsed.get("key_risks", [])),
                "confidence_commentary": str(parsed.get("confidence_commentary", "")),
            }
        except Exception:
            return self._fallback(ticker, scores, decision)

    @staticmethod
    def _fallback(ticker: str, scores: dict, decision: dict) -> dict:
        """Deterministic explanation when LLM is unavailable."""
        return {
            "summary": f"{ticker} is rated {decision['action']} with a final score of {decision['final_score']}.",
            "key_strengths": [f"Fundamental score: {scores['fundamental']['score']}"],
            "key_risks": ["Review valuation, concentration, and latest corporate disclosures before investing."],
            "confidence_commentary": f"Confidence is {decision['confidence']} based on score distance and data completeness.",
        }
