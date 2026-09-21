"""Analytics + rates routes."""

from datetime import date
from decimal import Decimal

from app.core.deps import get_db, require_hr
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.meta_repo import RateRepository
from app.schemas.analytics import AnalyticsSummary, RateRead, RateRefresh
from app.services.analytics_service import AnalyticsService
from app.services.fx_service import StaticFxService
from fastapi import APIRouter, Depends
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
