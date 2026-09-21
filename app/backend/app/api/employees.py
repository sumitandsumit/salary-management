"""Employee routes. Thin: parse HTTP, call service, map errors."""

from app.core.config import settings
from app.core.deps import get_db, require_hr
from app.repositories.employee_repo import EmployeeRepository
from app.repositories.meta_repo import AuditRepository
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeIncrement,
    EmployeeRead,
    EmployeeUpdate,
)
from app.services.employee_service import (
    DuplicateEmail,
    EmployeeNotFound,
    EmployeeService,
)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/employees", tags=["employees"])


def _service(db: Session, actor: dict) -> EmployeeService:
    return EmployeeService(
        EmployeeRepository(db), AuditRepository(db), actor=actor["id"]
    )


@router.get("", response_model=dict)
def list_employees(
    search: str = "",
    dept: str = "",
    country: str = "",
    status: str = "",
    min_salary: float | None = None,
    max_salary: float | None = None,
    sort: str = "",
    page: int = Query(1, ge=1),
    size: int = Query(settings.page_size_default, ge=1),
    db: Session = Depends(get_db),
):
    size = min(size, settings.page_size_max)
    repo = EmployeeRepository(db)
    stmt = repo.base_query(search, dept, country, status, min_salary, max_salary)
    stmt = repo.apply_sort(stmt, sort)
    rows, total = repo.list_page(stmt, page, size)
    return {
        "data": [EmployeeRead.model_validate(r).model_dump() for r in rows],
        "meta": {"page": page, "size": size, "total": total},
    }


@router.post("", response_model=EmployeeRead, status_code=201)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    actor: dict = Depends(require_hr),
):
    try:
        emp = _service(db, actor).create(payload)
        db.commit()
        return emp
    except DuplicateEmail as exc:
        raise HTTPException(409, f"email already exists: {exc}") from exc


@router.get("/{emp_id}", response_model=EmployeeRead)
def get_employee(emp_id: str, db: Session = Depends(get_db)):
    emp = EmployeeRepository(db).get(emp_id)
    if emp is None:
        raise HTTPException(404, "employee not found")
    return emp


@router.patch("/{emp_id}", response_model=EmployeeRead)
def update_employee(
    emp_id: str,
    patch: EmployeeUpdate,
    db: Session = Depends(get_db),
    actor: dict = Depends(require_hr),
):
    try:
        emp = _service(db, actor).update(emp_id, patch)
        db.commit()
        return emp
    except EmployeeNotFound as exc:
        raise HTTPException(404, "employee not found") from exc


@router.post("/{emp_id}/increment", response_model=EmployeeRead)
def increment_salary(
    emp_id: str,
    body: EmployeeIncrement,
    db: Session = Depends(get_db),
    actor: dict = Depends(require_hr),
):
    try:
        emp = _service(db, actor).increment(emp_id, body.percent, body.reason)
        db.commit()
        return emp
    except EmployeeNotFound as exc:
        raise HTTPException(404, "employee not found") from exc


@router.post("/{emp_id}/deactivate", response_model=EmployeeRead)
def deactivate(
    emp_id: str, db: Session = Depends(get_db), actor: dict = Depends(require_hr)
):
    try:
        emp = _service(db, actor).deactivate(emp_id)
        db.commit()
        return emp
    except EmployeeNotFound as exc:
        raise HTTPException(404, "employee not found") from exc
