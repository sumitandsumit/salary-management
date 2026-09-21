"""FX conversion. Static table v1; live provider is a future swap."""

from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Protocol

TWOPLACES = Decimal("0.01")


class UnknownCurrencyError(KeyError):
    pass


class FxService(Protocol):
    def to_usd(self, amount: Decimal, currency: str) -> Decimal: ...
    def rate_date(self) -> date | None: ...


class StaticFxService:
    """Convert with versioned rates dict. Deterministic + testable."""

    def __init__(self, rates: dict[str, Decimal], day: date | None = None):
        self._rates = {k.upper(): v for k, v in rates.items()}
        self._day = day

    def to_usd(self, amount: Decimal, currency: str) -> Decimal:
        rate = self._rates.get(currency.upper())
        if rate is None:
            raise UnknownCurrencyError(currency)
        return (Decimal(amount) * rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)

    def rate_date(self) -> date | None:
        return self._day

    # TODO(fx-live): class LiveFxProvider(FxService) fetching nightly
    # from a provider into fx_history; same interface, no caller change.
