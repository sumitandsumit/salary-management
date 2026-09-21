"""Employee business rules. Repos injected (DIP); no HTTP here."""

from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from app.models.employee import STATUS_ACTIVE, STATUS_INACTIVE, Employee
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.meta_repo import AuditRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate

TWOPLACES = Decimal("0.01")


class EmployeeNotFound(KeyError):
    pass


class DuplicateEmail(ValueError):
    pass


def _to_dict(emp: Employee) -> dict:
    return {
        "id": emp.id,
        "email": emp.email,
        "base_salary": str(emp.base_salary),
        "bonus": str(emp.bonus),
        "status": emp.status,
    }


class EmployeeService:
    def __init__(
        self,
        employees: EmployeeRepository,
        audits: AuditRepository,
        actor: str = "hr_manager",
    ):
        self.employees = employees
        self.audits = audits
        self.actor = actor

    def create(self, payload: EmployeeCreate) -> Employee:
        if self.employees.get_by_email(payload.email):
            raise DuplicateEmail(payload.email)
        emp = Employee(**payload.model_dump())
        emp.country = emp.country.upper()
        emp.currency = emp.currency.upper()
        self.employees.add(emp)
        self.audits.record(
            self.actor, "create", "employee", emp.id, None, _to_dict(emp), None
        )
        return emp

    def update(
        self, emp_id: str, patch: EmployeeUpdate, reason: str | None = None
    ) -> Employee:
        emp = self.employees.get(emp_id)
        if emp is None:
            raise EmployeeNotFound(emp_id)
        old = _to_dict(emp)
        for field, value in patch.model_dump(exclude_unset=True).items():
            if value is None:
                continue
            if field in ("country", "currency"):
                value = str(value).upper()
            setattr(emp, field, value)
        self.audits.record(
            self.actor, "update", "employee", emp.id, old, _to_dict(emp), reason
        )
        return emp

    def increment(self, emp_id: str, percent: float, reason: str) -> Employee:
        emp = self.employees.get(emp_id)
        if emp is None:
            raise EmployeeNotFound(emp_id)
        old = _to_dict(emp)
        factor = Decimal(str(percent)) / Decimal("100")
        new_salary = (Decimal(emp.base_salary) * (1 + factor)).quantize(
            TWOPLACES, rounding=ROUND_HALF_UP
        )
        emp.base_salary = new_salary
        self.audits.record(
            self.actor, "increment", "employee", emp.id, old, _to_dict(emp), reason
        )
        return emp

    def deactivate(self, emp_id: str, reason: str | None = None) -> Employee:
        emp = self.employees.get(emp_id)
        if emp is None:
            raise EmployeeNotFound(emp_id)
        old = _to_dict(emp)
        emp.status = STATUS_INACTIVE
        self.audits.record(
            self.actor, "deactivate", "employee", emp.id, old, _to_dict(emp), reason
        )
        return emp

    # TODO(bulk-csv): add increment_many(rows) with single transaction +
    # per-row audit; validate all before writing (all-or-nothing).
