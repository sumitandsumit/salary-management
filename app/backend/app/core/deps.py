"""FastAPI dependencies. Auth intentionally minimal (see docs)."""

from collections.abc import Iterator

from app.core.database import SessionLocal
from sqlalchemy.orm import Session

HR_ACTOR = "hr_manager"


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_hr() -> dict:
    """Return fixed HR actor. TODO(auth): replace with JWT/OIDC."""
    return {"id": HR_ACTOR, "role": HR_ACTOR}
