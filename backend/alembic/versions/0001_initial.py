"""Initial schema."""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_role = sa.Enum("ADMIN", "INVESTOR", name="userrole")
recommendation_action = sa.Enum("STRONG_BUY", "BUY", "WATCH", "HOLD", "SELL", name="recommendationaction")


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "portfolios",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_portfolios_user_id", "portfolios", ["user_id"])
    op.create_table(
        "holdings",
        sa.Column("portfolio_id", sa.String(length=36), nullable=False),
        sa.Column("ticker", sa.String(length=24), nullable=False),
        sa.Column("company_name", sa.String(length=160), nullable=True),
        sa.Column("sector", sa.String(length=100), nullable=True),
        sa.Column("quantity", sa.Numeric(18, 4), nullable=False),
        sa.Column("average_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("portfolio_id", "ticker", name="uq_holding_portfolio_ticker"),
    )
    op.create_index("ix_holdings_portfolio_id", "holdings", ["portfolio_id"])
    op.create_table(
        "recommendation_runs",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("investment_amount", sa.Numeric(18, 2), nullable=True),
        sa.Column("input_payload", sa.JSON(), nullable=False),
        sa.Column("agent_outputs", sa.JSON(), nullable=False),
        sa.Column("model_version", sa.String(length=60), nullable=False),
        sa.Column("prompt_version", sa.String(length=60), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendation_runs_user_id", "recommendation_runs", ["user_id"])
    op.create_table(
        "recommendations",
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("ticker", sa.String(length=24), nullable=False),
        sa.Column("company_name", sa.String(length=160), nullable=True),
        sa.Column("sector", sa.String(length=100), nullable=True),
        sa.Column("action", recommendation_action, nullable=False),
        sa.Column("final_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("confidence", sa.Numeric(5, 2), nullable=False),
        sa.Column("allocation_amount", sa.Numeric(18, 2), nullable=True),
        sa.Column("reason_codes", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.JSON(), nullable=False),
        sa.Column("metrics_snapshot", sa.JSON(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], ["recommendation_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendations_run_id", "recommendations", ["run_id"])
    op.create_index("ix_recommendations_ticker", "recommendations", ["ticker"])
    op.create_table("market_cache", sa.Column("ticker", sa.String(24), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False), sa.Column("id", sa.String(36), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_market_cache_ticker", "market_cache", ["ticker"], unique=True)
    op.create_table("sentiment_cache", sa.Column("ticker", sa.String(24), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False), sa.Column("id", sa.String(36), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_sentiment_cache_ticker", "sentiment_cache", ["ticker"], unique=True)
    op.create_table("portfolio_analysis_runs", sa.Column("portfolio_id", sa.String(36), nullable=False), sa.Column("risk_score", sa.Numeric(5, 2), nullable=False), sa.Column("warnings", sa.JSON(), nullable=False), sa.Column("recommendations", sa.JSON(), nullable=False), sa.Column("id", sa.String(36), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_portfolio_analysis_runs_portfolio_id", "portfolio_analysis_runs", ["portfolio_id"])
    op.create_table("portfolio_analysis_results", sa.Column("run_id", sa.String(36), nullable=False), sa.Column("holding_id", sa.String(36), nullable=False), sa.Column("ticker", sa.String(24), nullable=False), sa.Column("action", recommendation_action, nullable=False), sa.Column("score", sa.Numeric(5, 2), nullable=False), sa.Column("rationale", sa.Text(), nullable=False), sa.Column("id", sa.String(36), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.ForeignKeyConstraint(["holding_id"], ["holdings.id"], ondelete="CASCADE"), sa.ForeignKeyConstraint(["run_id"], ["portfolio_analysis_runs.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_portfolio_analysis_results_run_id", "portfolio_analysis_results", ["run_id"])
    op.create_table("audit_logs", sa.Column("user_id", sa.String(36), nullable=True), sa.Column("event_type", sa.String(80), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False), sa.Column("id", sa.String(36), nullable=False), sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_event_type", "audit_logs", ["event_type"])


def downgrade() -> None:
    """Revert migration."""
    for table in ["audit_logs", "portfolio_analysis_results", "portfolio_analysis_runs", "sentiment_cache", "market_cache", "recommendations", "recommendation_runs", "holdings", "portfolios", "users"]:
        op.drop_table(table)
