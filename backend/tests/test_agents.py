"""Agent unit tests."""

from decimal import Decimal

from app.agents.fundamental_agent import FundamentalAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.risk_agent import RiskAgent
from app.models.recommendation import RecommendationAction


def test_fundamental_agent_scores_strong_business() -> None:
    """High quality metrics should receive a strong score."""
    metrics = {
        "roe": 0.22,
        "revenue_growth": 0.18,
        "operating_margin": 0.24,
        "debt_to_equity": 15,
        "free_cash_flow": 1_000_000,
        "pe_ratio": 25,
    }
    result = FundamentalAgent().score(metrics)
    assert result["score"] >= 80
    assert result["components"]["quality"] >= 80


def test_risk_agent_flags_concentration() -> None:
    """Concentrated portfolios should produce warnings."""
    result = RiskAgent().analyze(
        [
            {"ticker": "AAA", "sector": "IT", "value": Decimal("800")},
            {"ticker": "BBB", "sector": "IT", "value": Decimal("200")},
        ]
    )
    assert result["risk_score"] > 50
    assert result["warnings"]


def test_recommendation_thresholds() -> None:
    """Recommendation agent should apply documented thresholds."""
    decision = RecommendationAgent().decide(
        {"score": 90, "components": {"quality": 90}},
        {"score": 75},
        risk_score=5,
    )
    assert decision["action"] == RecommendationAction.STRONG_BUY
