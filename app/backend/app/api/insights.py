"""Analytics + rates routes."""

from datetime import date
from decimal import Decimal

from app.core.deps import get_db, require_hr
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.meta_repo import AuditRepository, RateRepository
from app.schemas.analytics import (
    AnalyticsSummary,
    RateRead,
    RateRefresh,
    RateUpdate,
)
from app.services.analytics_service import AnalyticsService
from app.services.fx_service import StaticFxService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["insights"])

FALLBACK_RATES = {
    "USD": Decimal("1"),
    "INR": Decimal("0.012"),
    "EUR": Decimal("1.08"),
    "GBP": Decimal("1.27"),
    "JPY": Decimal("0.007"),
}


def _fx_and_day(db: Session):
    rows = RateRepository(db).all()
    if rows:
        rates = {r.currency_code: Decimal(r.rate_to_usd) for r in rows}
        day = max(r.effective_date for r in rows)
        return StaticFxService(rates, day), day
    return StaticFxService(dict(FALLBACK_RATES), date.today()), date.today()


@router.get("/analytics/summary", response_model=AnalyticsSummary)
def analytics_summary(
    search: str = "", dept: str = "", country: str = "", db: Session = Depends(get_db)
):
    fx, day = _fx_and_day(db)
    svc = AnalyticsService(EmployeeRepository(db), fx, day)
    return svc.summary(search=search, dept=dept, country=country)


@router.get("/rates", response_model=list[RateRead])
def list_rates(db: Session = Depends(get_db)):
    return RateRepository(db).all()


@router.post("/rates/refresh", response_model=list[RateRead])
def refresh_rates(
    body: RateRefresh, db: Session = Depends(get_db), _actor: dict = Depends(require_hr)
):
    repo = RateRepository(db)
    for code, rate in body.rates.items():
        repo.upsert(code, Decimal(rate), body.effective_date)
    db.commit()
    return repo.all()


@router.put("/rates/{code}", response_model=RateRead)
def update_rate(
    code: str,
    body: RateUpdate,
    db: Session = Depends(get_db),
    actor: dict = Depends(require_hr),
):
    """Edit a single currency rate. Creation stays in POST /rates/refresh."""
    if len(code) != 3 or not code.isalpha():
        raise HTTPException(422, "currency code must be 3 letters (ISO-4217)")
    repo = RateRepository(db)
    row = repo.get(code)
    if row is None:
        raise HTTPException(404, f"unknown currency: {code.upper()}")
    old = {"rate_to_usd": str(row.rate_to_usd), "effective_date": str(row.effective_date)}
    updated = repo.upsert(code, Decimal(body.rate_to_usd), body.effective_date)
    AuditRepository(db).record(
        actor["id"],
        "rate_update",
        "exchange_rate",
        updated.currency_code,
        old,
        {"rate_to_usd": str(updated.rate_to_usd), "effective_date": str(updated.effective_date)},
        body.reason,
    )
    db.commit()
    return updated
