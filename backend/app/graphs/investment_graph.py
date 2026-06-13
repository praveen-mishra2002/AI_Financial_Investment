"""LangGraph-compatible investment recommendation workflow."""

from typing import Any, TypedDict

try:
    from langgraph.graph import END, StateGraph
except Exception:  # pragma: no cover
    END = "END"
    StateGraph = None

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.fundamental_agent import FundamentalAgent
from app.agents.market_agent import MarketAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.explainability_agent import ExplainabilityAgent
from app.agents.types import Candidate


class InvestmentState(TypedDict, total=False):
    """Workflow state."""

    candidate: Candidate
    market: dict
    fundamental: dict
    sentiment: dict
    risk_score: float
    decision: dict
    explanation: dict
    errors: list[str]


class InvestmentGraph:
    """Supervisor graph orchestrating investment agents."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.market_agent = MarketAgent(db)
        self.fundamental_agent = FundamentalAgent()
        self.sentiment_agent = SentimentAgent(db)
        self.recommendation_agent = RecommendationAgent()
        self.explainability_agent = ExplainabilityAgent()
        self.graph = self._build_graph()

    async def run(self, candidate: Candidate, risk_score: float = 0.0) -> InvestmentState:
        """Execute the workflow for one candidate."""
        initial: InvestmentState = {"candidate": candidate, "risk_score": risk_score, "errors": []}
        if self.graph is None:
            return await self._run_linear(initial)
        return await self.graph.ainvoke(initial)

    def _build_graph(self) -> Any:
        """Build a LangGraph state graph when available."""
        if StateGraph is None:
            return None
        graph = StateGraph(InvestmentState)
        graph.add_node("market", self._market_node)
        graph.add_node("fundamental", self._fundamental_node)
        graph.add_node("sentiment", self._sentiment_node)
        graph.add_node("recommendation", self._recommendation_node)
        graph.add_node("explanation", self._explanation_node)
        graph.set_entry_point("market")
        graph.add_edge("market", "fundamental")
        graph.add_edge("fundamental", "sentiment")
        graph.add_edge("sentiment", "recommendation")
        graph.add_edge("recommendation", "explanation")
        graph.add_edge("explanation", END)
        return graph.compile()

    async def _run_linear(self, state: InvestmentState) -> InvestmentState:
        """Fallback execution path if LangGraph is not installed."""
        for node in [self._market_node, self._fundamental_node, self._sentiment_node, self._recommendation_node, self._explanation_node]:
            state.update(await node(state))
        return state

    async def _market_node(self, state: InvestmentState) -> InvestmentState:
        return {"market": await self.market_agent.fetch(state["candidate"])}

    async def _fundamental_node(self, state: InvestmentState) -> InvestmentState:
        return {"fundamental": self.fundamental_agent.score(state["market"])}

    async def _sentiment_node(self, state: InvestmentState) -> InvestmentState:
        return {"sentiment": await self.sentiment_agent.analyze(state["candidate"]["ticker"])}

    async def _recommendation_node(self, state: InvestmentState) -> InvestmentState:
        return {"decision": self.recommendation_agent.decide(state["fundamental"], state["sentiment"], state.get("risk_score", 0.0))}

    async def _explanation_node(self, state: InvestmentState) -> InvestmentState:
        scores = {"fundamental": state["fundamental"], "sentiment": state["sentiment"], "risk_score": state.get("risk_score", 0.0)}
        return {"explanation": await self.explainability_agent.explain(state["candidate"]["ticker"], state["market"], scores, state["decision"])}
