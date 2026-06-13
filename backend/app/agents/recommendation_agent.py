"""Deterministic recommendation agent."""

from app.models.recommendation import RecommendationAction


class RecommendationAgent:
    """Combine scores and produce final investment actions."""

    def decide(self, fundamental: dict, sentiment: dict, risk_score: float = 0.0) -> dict:
        """Return final score, action, confidence, and reason codes."""
        fundamental_score = float(fundamental["score"])
        sentiment_score = float(sentiment["score"])
        quality_score = float(fundamental["components"]["quality"])
        risk_adjustment = max(0.0, 100.0 - risk_score)
        final_score = (
            fundamental_score * 0.40
            + sentiment_score * 0.10
            + quality_score * 0.35
            + risk_adjustment * 0.15
        )
        action = self._action(final_score)
        confidence = min(98.0, max(40.0, 55.0 + abs(final_score - 50.0) * 0.75))
        return {
            "final_score": round(final_score, 2),
            "action": action,
            "confidence": round(confidence, 2),
            "reason_codes": self._reason_codes(fundamental_score, sentiment_score, risk_score),
        }

    @staticmethod
    def _action(score: float) -> RecommendationAction:
        """Map score to action."""
        if score >= 85:
            return RecommendationAction.STRONG_BUY
        if score >= 70:
            return RecommendationAction.BUY
        if score >= 55:
            return RecommendationAction.WATCH
        if score >= 40:
            return RecommendationAction.HOLD
        return RecommendationAction.SELL

    @staticmethod
    def _reason_codes(fundamental_score: float, sentiment_score: float, risk_score: float) -> list[str]:
        """Build reason codes."""
        reasons: list[str] = []
        reasons.append("FUNDAMENTALS_STRONG" if fundamental_score >= 70 else "FUNDAMENTALS_WEAK")
        if sentiment_score >= 60:
            reasons.append("SENTIMENT_POSITIVE")
        elif sentiment_score <= 40:
            reasons.append("SENTIMENT_NEGATIVE")
        if risk_score >= 60:
            reasons.append("RISK_ELEVATED")
        return reasons
