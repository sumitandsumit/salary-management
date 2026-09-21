"""Register ORM tables for Base.metadata.create_all."""

from app.models.audit_log import AuditLog  # noqa: F401
from app.models.employee import Employee  # noqa: F401
from app.models.exchange_rate import ExchangeRate  # noqa: F401
