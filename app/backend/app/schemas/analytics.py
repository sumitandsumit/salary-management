"""Analytics + rates schemas."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BucketCount(BaseModel):
    label: str
    count: int


class TopEarner(BaseModel):
    id: str
    name: str
    department: str
    country: str
    base_salary: Decimal
    currency: str
    usd_equivalent: Decimal


class AnalyticsSummary(BaseModel):
    headcount: int
    total_usd: Decimal
    per_currency: dict[str, Decimal]
    avg_by_department: dict[str, Decimal]
    avg_by_country: dict[str, Decimal]
    top_earners: list[TopEarner]
    distribution: list[BucketCount]
    rate_date: date | None = None


class RateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    currency_code: str
    rate_to_usd: Decimal
    effective_date: date


class RateRefresh(BaseModel):
    rates: dict[str, Decimal] = Field(description="code -> rate_to_usd")
    effective_date: date


class RateUpdate(BaseModel):
    rate_to_usd: Decimal = Field(gt=0, max_digits=18, decimal_places=6)
    effective_date: date
    reason: str | None = Field(default=None, max_length=500)
