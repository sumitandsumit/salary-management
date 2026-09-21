"""Employee queries only. No business rules here (see services)."""

from app.models.employee import Employee
from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session

ALLOWED_SORTS = {"name", "base_salary", "joining_date", "created_at"}


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def base_query(
        self,
        search="",
        dept="",
        country="",
        status="",
        min_salary=None,
        max_salary=None,
    ):
        stmt = select(Employee)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                or_(Employee.name.ilike(like), Employee.email.ilike(like))
            )
        if dept:
            stmt = stmt.where(Employee.department == dept)
        if country:
            stmt = stmt.where(Employee.country == country)
        if status:
            stmt = stmt.where(Employee.status == status)
        if min_salary is not None:
            stmt = stmt.where(Employee.base_salary >= min_salary)
        if max_salary is not None:
            stmt = stmt.where(Employee.base_salary <= max_salary)
        return stmt

    def apply_sort(self, stmt, sort=""):
        if not sort:
            return stmt.order_by(asc(Employee.name))
        field, _, direction = sort.partition(":")
        if field not in ALLOWED_SORTS:
            return stmt.order_by(asc(Employee.name))
        col = getattr(Employee, field)
        return stmt.order_by(desc(col) if direction == "desc" else asc(col))

    def list_page(self, stmt, page: int, size: int):
        total = len(self.db.execute(stmt).scalars().all())
        rows = (
            self.db.execute(stmt.offset((page - 1) * size).limit(size)).scalars().all()
        )
        return rows, total

    def get(self, employee_id: str) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        stmt = select(Employee).where(Employee.email == email)
        return self.db.execute(stmt).scalars().first()

    def add(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        return employee
