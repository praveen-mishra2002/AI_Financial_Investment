"""Recommendation and portfolio analysis services."""

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.risk_agent import RiskAgent
from app.core.config import settings
from app.graphs.investment_graph import InvestmentGraph
from app.models.portfolio import Holding
from app.models.recommendation import PortfolioAnalysisResult, PortfolioAnalysisRun, Recommendation, RecommendationRun
from app.models.user import User
from app.repositories.audit import AuditRepository
from app.repositories.portfolios import PortfolioRepository
from app.schemas.recommendation import (
    HoldingAnalysisRead,
    PortfolioAnalysisRead,
    RecommendationRead,
    RecommendationRequest,
    RecommendationRunRead,
)


class RecommendationService:
    """Investment recommendation workflows."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.audit = AuditRepository(db)
        self.portfolios = PortfolioRepository(db)
        self.risk_agent = RiskAgent()

    async def generate(self, user: User, payload: RecommendationRequest) -> RecommendationRunRead:
        """Generate and persist recommendations."""
        graph = InvestmentGraph(self.db)
        amount = payload.investment_amount
        states = []
        for candidate in payload.candidates:
            states.append(await graph.run(candidate.model_dump(), risk_score=0.0))

        buy_like = [state for state in states if state["decision"]["action"].value in {"Strong Buy", "Buy", "Watch"}]
        allocation_count = max(1, len(buy_like))
        run = RecommendationRun(
            user_id=user.id,
            investment_amount=amount,
            input_payload=payload.model_dump(mode="json"),
            agent_outputs={state["candidate"]["ticker"]: self._state_for_audit(state) for state in states},
            model_version=settings.openai_model,
        )
        self.db.add(run)
        await self.db.flush()

        response_items: list[RecommendationRead] = []
        for state in states:
            decision = state["decision"]
            allocation = amount / Decimal(allocation_count) if state in buy_like else Decimal("0")
            entity = Recommendation(
                run_id=run.id,
                ticker=state["candidate"]["ticker"],
                company_name=state["market"].get("company_name"),
                sector=state["market"].get("sector"),
                action=decision["action"],
                final_score=Decimal(str(decision["final_score"])),
                confidence=Decimal(str(decision["confidence"])),
                allocation_amount=allocation,
                reason_codes=decision["reason_codes"],
                explanation=state["explanation"],
                metrics_snapshot=state["market"],
            )
            self.db.add(entity)
            await self.db.flush()
            response_items.append(RecommendationRead.model_validate(entity))

        await self.audit.record(user.id, "recommendation.generated", {"run_id": run.id, "count": len(response_items)})
        await self.db.commit()
        return RecommendationRunRead(id=run.id, recommendations=response_items)

    async def analyze_portfolio(self, user: User, portfolio_id: str) -> PortfolioAnalysisRead:
        """Analyze current holdings and persist results."""
        portfolio = await self.portfolios.get_for_user(portfolio_id, user.id)
        if portfolio is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

        holding_inputs = [
            {"ticker": h.ticker, "sector": h.sector, "value": h.quantity * h.average_price}
            for h in portfolio.holdings
        ]
        risk = self.risk_agent.analyze(holding_inputs)
        run = PortfolioAnalysisRun(
            portfolio_id=portfolio.id,
            risk_score=Decimal(str(risk["risk_score"])),
            warnings=risk["warnings"],
            recommendations=risk["recommendations"],
        )
        self.db.add(run)
        await self.db.flush()

        results: list[HoldingAnalysisRead] = []
        for holding in portfolio.holdings:
            score = self._holding_score(holding, risk["risk_score"])
            action = InvestmentGraph().recommendation_agent._action(score)
            rationale = f"{holding.ticker} receives {action.value} based on portfolio risk and position review."
            entity = PortfolioAnalysisResult(
                run_id=run.id,
                holding_id=holding.id,
                ticker=holding.ticker,
                action=action,
                score=Decimal(str(round(score, 2))),
                rationale=rationale,
            )
            self.db.add(entity)
            results.append(HoldingAnalysisRead(ticker=holding.ticker, action=action, score=entity.score, rationale=rationale))

        await self.audit.record(user.id, "portfolio.analyzed", {"portfolio_id": portfolio.id, "run_id": run.id})
        await self.db.commit()
        return PortfolioAnalysisRead(
            id=run.id,
            risk_score=run.risk_score,
            warnings=run.warnings,
            recommendations=run.recommendations,
            holdings=results,
        )

    @staticmethod
    def _holding_score(holding: Holding, risk_score: float) -> float:
        """Simple deterministic holding score for portfolio analysis."""
        value = float(holding.quantity * holding.average_price)
        base = 65.0 if value > 0 else 35.0
        return max(0.0, min(100.0, base - risk_score * 0.25))

    @staticmethod
    def _state_for_audit(state: dict) -> dict:
        """Build a compact audit-safe state snapshot."""
        return {
            "market": state.get("market"),
            "fundamental": state.get("fundamental"),
            "sentiment": state.get("sentiment"),
            "decision": {
                **state.get("decision", {}),
                "action": state.get("decision", {}).get("action").value if state.get("decision", {}).get("action") else None,
            },
            "explanation": state.get("explanation"),
        }
