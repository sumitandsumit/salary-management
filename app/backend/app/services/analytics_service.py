"""Analytics aggregation. SQL for math; Python only for FX + buckets."""

from collections import defaultdict
from datetime import date
from decimal import Decimal

from app.repositories.employee_repo import EmployeeRepository
from app.schemas.analytics import AnalyticsSummary, BucketCount, TopEarner
from app.services.fx_service import FxService

TOP_N = 10
BUCKETS = [(0, 30000), (30000, 60000), (60000, 100000), (100000, 10**12)]
BUCKET_LABELS = ["<30k", "30-60k", "60-100k", "100k+"]


class AnalyticsService:
    def __init__(
        self, employees: EmployeeRepository, fx: FxService, rate_day: date | None = None
    ):
        self.employees = employees
        self.fx = fx
        self.rate_day = rate_day

    def summary(self, search="", dept="", country="") -> AnalyticsSummary:
        stmt = self.employees.base_query(
            search=search, dept=dept, country=country, status="active"
        )
        rows = self.employees.db.execute(stmt).scalars().all()

        per_currency: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        by_dept: dict[str, list[Decimal]] = defaultdict(list)
        by_country: dict[str, list[Decimal]] = defaultdict(list)
        total_usd = Decimal("0")
        scored = []

        for emp in rows:
            local = Decimal(emp.base_salary) + Decimal(emp.bonus or 0)
            per_currency[emp.currency] += local
            usd = self.fx.to_usd(local, emp.currency)
            total_usd += usd
            by_dept[emp.department].append(usd)
            by_country[emp.country].append(usd)
            scored.append((usd, emp))

        scored.sort(key=lambda t: t[0], reverse=True)
        top = [
            TopEarner(
                id=e.id,
                name=e.name,
                department=e.department,
                country=e.country,
                base_salary=e.base_salary,
                currency=e.currency,
                usd_equivalent=u,
            )
            for u, e in scored[:TOP_N]
        ]

        dist = [0] * len(BUCKETS)
        for usd, _ in scored:
            for i, (low, high) in enumerate(BUCKETS):
                if low <= float(usd) < high:
                    dist[i] += 1
                    break

        def avg(values: list[Decimal]) -> Decimal:
            return sum(values, Decimal("0")) / len(values) if values else Decimal("0")

        return AnalyticsSummary(
            headcount=len(rows),
            total_usd=total_usd,
            per_currency=dict(per_currency),
            avg_by_department={k: avg(v) for k, v in by_dept.items()},
            avg_by_country={k: avg(v) for k, v in by_country.items()},
            top_earners=top,
            distribution=[
                BucketCount(label=l, count=c) for l, c in zip(BUCKET_LABELS, dist)
            ],
            rate_date=self.rate_day,
        )
