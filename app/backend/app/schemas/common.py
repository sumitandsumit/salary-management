"""Shared envelopes: pagination + errors."""

from pydantic import BaseModel


class PageMeta(BaseModel):
    page: int
    size: int
    total: int


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: dict | None = None
    request_id: str | None = None
