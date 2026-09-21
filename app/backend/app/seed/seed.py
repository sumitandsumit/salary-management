"""Deterministic 10k seed. Faker seed=42; bulk batches of 1000."""

import argparse
import random
from datetime import date
from decimal import Decimal

from faker import Faker
from sqlalchemy import func, select

from app.core.database import SessionLocal, init_db
from app.models.employee import STATUS_ACTIVE, STATUS_INACTIVE, Employee
from app.models.exchange_rate import ExchangeRate

SEED = 42
BATCH = 1000
RATE_DAY = date(2026, 1, 1)

BASE_RATES = {"USD": Decimal("1"), "INR": Decimal("0.012"),
              "EUR": Decimal("1.08"), "GBP": Decimal("1.27"),
              "JPY": Decimal("0.007")}

COUNTRY_CURRENCY = [("IN", "INR"), ("US", "USD"), ("DE", "EUR"),
                    ("GB", "GBP"), ("JP", "JPY")]
DEPARTMENTS = ["Engineering", "HR", "Sales", "Finance", "Operations",
               "Marketing"]
TITLES = ["SDE I", "SDE II", "SDE III", "Manager", "Analyst", "Lead",
          "Specialist"]
SALARY_BANDS = {"INR": (400000, 3000000), "USD": (60000, 200000),
                "EUR": (55000, 180000), "GBP": (50000, 170000),
                "JPY": (4000000, 12000000)}


def seed_rates(db) -> int:
    count = 0
    for code, rate in BASE_RATES.items():
        if db.get(ExchangeRate, code) is None:
            db.add(ExchangeRate(currency_code=code, rate_to_usd=rate,
                                effective_date=RATE_DAY, source="seed"))
            count += 1
    db.commit()
    return count


def _make_employee(fake: Faker, i: int) -> Employee:
    rng = random.Random(SEED + i)
    country, currency = rng.choice(COUNTRY_CURRENCY)
    low, high = SALARY_BANDS[currency]
    base = Decimal(rng.randint(low, high))
    bonus = (base * Decimal(rng.randint(0, 20)) / Decimal(100)
             ).quantize(Decimal("1"))
    status = STATUS_ACTIVE if rng.random() < 0.95 else STATUS_INACTIVE
    name = fake.name()
    local = name.lower().replace(" ", ".").replace("'", "")
    return Employee(
        name=name,
        email=f"{local}.{i}@acme.local",
        department=rng.choice(DEPARTMENTS),
        job_title=rng.choice(TITLES),
        country=country,
        currency=currency,
        base_salary=base,
        bonus=bonus,
        joining_date=date(rng.randint(2015, 2026), rng.randint(1, 12),
                          rng.randint(1, 28)),
        status=status,
    )


def seed_employees(count: int, fresh: bool = False) -> int:
    init_db()
    db = SessionLocal()
    try:
        existing = db.execute(select(func.count()).select_from(Employee)
                              ).scalar() or 0
        if existing and not fresh:
            print(f"seed: {existing} employees present, skipping")
            return existing
        if fresh and existing:
            db.query(Employee).delete()
            db.commit()
        fake = Faker()
        Faker.seed(SEED)
        random.seed(SEED)
        batch: list[Employee] = []
        for i in range(count):
            batch.append(_make_employee(fake, i))
            if len(batch) >= BATCH:
                db.bulk_save_objects(batch)
                db.commit()
                batch.clear()
        if batch:
            db.bulk_save_objects(batch)
            db.commit()
        total = db.execute(select(func.count()).select_from(Employee)
                           ).scalar() or 0
        print(f"seed: wrote {total} employees (seed={SEED})")
        return total
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed salary DB")
    parser.add_argument("--count", type=int, default=10000)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    db = SessionLocal()
    init_db()
    try:
        added = seed_rates(db)
        print(f"seed: {added} rates upserted")
    finally:
        db.close()
    seed_employees(args.count, fresh=args.fresh)


if __name__ == "__main__":
    main()
