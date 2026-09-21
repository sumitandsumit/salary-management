"""Structured logging + request-id middleware."""

import logging
import sys
import uuid

from app.core.config import settings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class _DefaultRequestId(logging.Filter):
    """Ensure request_id exists on every record (e.g. httpx, startup)."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s "
        "request_id=%(request_id)s %(message)s",
        stream=sys.stdout,
        force=True,
    )
    logging.getLogger().addFilter(_DefaultRequestId())


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Echo/assign request id; attaches to log record + response."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get(settings.request_id_header)
        if not request_id:
            request_id = uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[settings.request_id_header] = request_id
        return response


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
