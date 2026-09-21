"""Employee ORM. Money as NUMERIC; soft-delete via status."""

import uuid
from datetime import date, datetime

from app.core.database import Base
from sqlalchemy import Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    department: Mapped[str] = mapped_column(String(80), index=True)
    job_title: Mapped[str] = mapped_column(String(80))
    country: Mapped[str] = mapped_column(String(2), index=True)
    currency: Mapped[str] = mapped_column(String(3))
    base_salary: Mapped[float] = mapped_column(Numeric(14, 2), index=True)
    bonus: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    joining_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(16), default=STATUS_ACTIVE, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # TODO(history): add salary_history table + hook here; audit_logs
    # already captures old/new so history can be backfilled.
