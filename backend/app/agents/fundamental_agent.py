"""Fundamental analysis scoring agent."""

from app.agents.types import MarketMetrics


class FundamentalAgent:
    """Compute a deterministic 0-100 fundamental score."""

    weights = {
        "roe": 0.20,
        "revenue_growth": 0.20,
        "operating_margin": 0.15,
        "debt_to_equity": 0.15,
        "free_cash_flow": 0.10,
        "pe_ratio": 0.10,
        "quality": 0.10,
    }

    def score(self, metrics: MarketMetrics) -> dict:
        """Score fundamentals using the approved methodology."""
        components = {
            "roe": self._higher_better(metrics.get("roe"), 0.05, 0.25),
            "revenue_growth": self._higher_better(metrics.get("revenue_growth"), 0.00, 0.20),
            "operating_margin": self._higher_better(metrics.get("operating_margin"), 0.05, 0.25),
            "debt_to_equity": self._lower_better(metrics.get("debt_to_equity"), 200.0, 20.0),
            "free_cash_flow": 100.0 if (metrics.get("free_cash_flow") or 0) > 0 else 35.0,
            "pe_ratio": self._pe_score(metrics.get("pe_ratio")),
        }
        components["quality"] = (
            components["roe"] * 0.35
            + components["operating_margin"] * 0.30
            + components["debt_to_equity"] * 0.20
            + components["free_cash_flow"] * 0.15
        )
        total = sum(components[key] * weight for key, weight in self.weights.items())
        return {"score": round(total, 2), "components": {key: round(value, 2) for key, value in components.items()}}

    @staticmethod
    def _higher_better(value: float | None, floor: float, ceiling: float) -> float:
        """Scale a metric where higher is better."""
        if value is None:
            return 50.0
        return max(0.0, min(100.0, ((value - floor) / (ceiling - floor)) * 100.0))

    @staticmethod
    def _lower_better(value: float | None, floor: float, ceiling: float) -> float:
        """Scale a metric where lower is better."""
        if value is None:
            return 50.0
        return max(0.0, min(100.0, ((floor - value) / (floor - ceiling)) * 100.0))

    @staticmethod
    def _pe_score(value: float | None) -> float:
        """Score PE ratio with a valuation sweet spot."""
        if value is None or value <= 0:
            return 50.0
        if value <= 15:
            return 90.0
        if value <= 30:
            return 100.0 - ((value - 15) / 15) * 20
        if value <= 60:
            return 70.0 - ((value - 30) / 30) * 50
        return 20.0
