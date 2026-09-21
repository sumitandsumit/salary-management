"""Deterministic dev seed. Full 10k seed lands in step 5 (commit)."""

from datetime import date
from decimal import Decimal

from app.models.employee import Employee
from app.models.exchange_rate import ExchangeRate

SEED_MARK = "dev-seed-v1"

BASE_RATES = {
    "USD": (Decimal("1"), date(2026, 1, 1)),
    "INR": (Decimal("0.012"), date(2026, 1, 1)),
    "EUR": (Decimal("1.08"), date(2026, 1, 1)),
    "GBP": (Decimal("1.27"), date(2026, 1, 1)),
    "JPY": (Decimal("0.007"), date(2026, 1, 1)),
}


def seed_rates(db) -> int:
    count = 0
    for code, (rate, day) in BASE_RATES.items():
        if db.get(ExchangeRate, code) is None:
            db.add(
                ExchangeRate(
                    currency_code=code,
                    rate_to_usd=rate,
                    effective_date=day,
                    source="seed",
                )
            )
            count += 1
    db.commit()
    return count


def seed_minimal(db) -> Employee:
    """One employee for local smoke. TODO(seed-10k): Faker bulk 10k."""
    emp = Employee(
        name="Asha HR",
        email="asha.hr@acme.local",
        department="HR",
        job_title="HR Manager",
        country="IN",
        currency="INR",
        base_salary=Decimal("900000"),
        bonus=Decimal("50000"),
        joining_date=date(2022, 6, 1),
    )
    db.add(emp)
    db.commit()
    return emp
