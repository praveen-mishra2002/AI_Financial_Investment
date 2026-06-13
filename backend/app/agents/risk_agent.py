"""Portfolio risk analysis agent."""

from decimal import Decimal

from app.agents.types import HoldingInput


class RiskAgent:
    """Analyze concentration, sector exposure, and diversification."""

    def analyze(self, holdings: list[HoldingInput]) -> dict:
        """Return portfolio risk score, warnings, and recommendations."""
        if not holdings:
            return {"risk_score": 100.0, "warnings": ["Portfolio has no holdings"], "recommendations": ["Add holdings"]}
        total_value = sum((holding["value"] for holding in holdings), Decimal("0"))
        if total_value <= 0:
            return {"risk_score": 100.0, "warnings": ["Portfolio value is zero"], "recommendations": ["Check holdings"]}

        ticker_weights = {holding["ticker"]: float(holding["value"] / total_value) for holding in holdings}
        sector_weights: dict[str, float] = {}
        for holding in holdings:
            sector = holding.get("sector") or "Unknown"
            sector_weights[sector] = sector_weights.get(sector, 0.0) + float(holding["value"] / total_value)

        max_position = max(ticker_weights.values())
        max_sector = max(sector_weights.values())
        diversification_penalty = max(0, 10 - len(holdings)) * 3
        concentration_penalty = max(0.0, (max_position - 0.20) * 120)
        sector_penalty = max(0.0, (max_sector - 0.35) * 90)
        risk_score = min(100.0, concentration_penalty + sector_penalty + diversification_penalty)

        warnings: list[str] = []
        recommendations: list[str] = []
        if max_position > 0.20:
            warnings.append("Single-stock concentration exceeds 20%")
            recommendations.append("Reduce oversized positions or add diversified holdings")
        if max_sector > 0.35:
            warnings.append("Sector exposure exceeds 35%")
            recommendations.append("Add exposure to underrepresented sectors")
        if len(holdings) < 10:
            warnings.append("Portfolio has fewer than 10 holdings")
            recommendations.append("Improve diversification across 10-20 quality stocks")

        return {
            "risk_score": round(risk_score, 2),
            "warnings": warnings,
            "recommendations": recommendations,
            "ticker_weights": ticker_weights,
            "sector_weights": sector_weights,
        }
