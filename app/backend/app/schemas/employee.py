"""Employee request/response schemas. Decimal money, strict ISO codes."""

from datetime import date, datetime
from decimal import Decimal

from app.models.employee import STATUS_ACTIVE
from pydantic import BaseModel, ConfigDict, Field

CURRENCY_LEN = 3
COUNTRY_LEN = 2
MAX_PERCENT = 100
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=5, max_length=160, pattern=EMAIL_PATTERN)
    department: str = Field(min_length=1, max_length=80)
    job_title: str = Field(min_length=1, max_length=80)
    country: str = Field(min_length=COUNTRY_LEN, max_length=COUNTRY_LEN)
    currency: str = Field(min_length=CURRENCY_LEN, max_length=CURRENCY_LEN)
    base_salary: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    bonus: Decimal = Field(default=Decimal("0"), ge=0, max_digits=14, decimal_places=2)
    joining_date: date
    status: str = STATUS_ACTIVE


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=120)
    department: str | None = Field(default=None, max_length=80)
    job_title: str | None = Field(default=None, max_length=80)
    country: str | None = Field(default=None, max_length=COUNTRY_LEN)
    currency: str | None = Field(default=None, max_length=CURRENCY_LEN)
    base_salary: Decimal | None = Field(
        default=None, gt=0, max_digits=14, decimal_places=2
    )
    bonus: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=2)
    status: str | None = None


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    department: str
    job_title: str
    country: str
    currency: str
    base_salary: Decimal
    bonus: Decimal
    joining_date: date
    status: str
    created_at: datetime
    updated_at: datetime


class EmployeeIncrement(BaseModel):
    percent: float = Field(gt=0, le=MAX_PERCENT)
    reason: str = Field(min_length=3, max_length=500)
