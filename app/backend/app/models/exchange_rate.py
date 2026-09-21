"""Versioned FX rates. Salaries stay in local currency (see docs)."""

from datetime import date

from app.core.database import Base
from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    currency_code: Mapped[str] = mapped_column(String(3), primary_key=True)
    rate_to_usd: Mapped[float] = mapped_column(Numeric(18, 6))
    effective_date: Mapped[date] = mapped_column(Date)
    source: Mapped[str] = mapped_column(String(32), default="seed")

    # TODO(fx-live): add fx_history table + nightly provider job here.
