"""Audit + rate persistence helpers."""

from datetime import date
from decimal import Decimal

from app.models.audit_log import AuditLog
from app.models.exchange_rate import ExchangeRate
from sqlalchemy import select
from sqlalchemy.orm import Session


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def record(
        self,
        actor: str,
        action: str,
        entity: str,
        entity_id: str,
        old: dict | None,
        new: dict | None,
        reason: str | None = None,
    ) -> AuditLog:
        row = AuditLog(
            actor=actor,
            action=action,
            entity=entity,
            entity_id=entity_id,
            old_data=old,
            new_data=new,
            reason=reason,
        )
        self.db.add(row)
        self.db.flush()
        return row


class RateRepository:
    def __init__(self, db: Session):
        self.db = db

    def all(self) -> list[ExchangeRate]:
        stmt = select(ExchangeRate)
        return list(self.db.execute(stmt).scalars().all())

    def upsert(
        self, code: str, rate: Decimal, day: date, source: str = "admin"
    ) -> ExchangeRate:
        row = self.db.get(ExchangeRate, code.upper())
        if row is None:
            row = ExchangeRate(
                currency_code=code.upper(),
                rate_to_usd=rate,
                effective_date=day,
                source=source,
            )
            self.db.add(row)
        else:
            row.rate_to_usd = rate
            row.effective_date = day
            row.source = source
        self.db.flush()
        return row
