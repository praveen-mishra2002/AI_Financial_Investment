"""Portfolio schemas."""

from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class HoldingBase(BaseModel):
    """Shared holding fields."""

    ticker: str = Field(min_length=1, max_length=24)
    company_name: str | None = None
    sector: str | None = None
    quantity: Decimal = Field(gt=0)
    average_price: Decimal = Field(gt=0)

    @field_validator("ticker")
    @classmethod
    def normalize_ticker(cls, value: str) -> str:
        """Normalize ticker symbols for NSE lookups."""
        return value.strip().upper()


class HoldingCreate(HoldingBase):
    """Create holding request."""


class HoldingUpdate(BaseModel):
    """Update holding request."""

    company_name: str | None = None
    sector: str | None = None
    quantity: Decimal | None = Field(default=None, gt=0)
    average_price: Decimal | None = Field(default=None, gt=0)


class HoldingRead(HoldingBase):
    """Holding response."""

    id: str
    portfolio_id: str

    model_config = {"from_attributes": True}


class PortfolioCreate(BaseModel):
    """Create portfolio request."""

    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)


class PortfolioUpdate(BaseModel):
    """Update portfolio request."""

    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=500)


class PortfolioRead(BaseModel):
    """Portfolio response."""

    id: str
    name: str
    description: str | None
    holdings: list[HoldingRead] = []

    model_config = {"from_attributes": True}
