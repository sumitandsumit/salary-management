"""App factory. Routers + middleware + error envelope."""

from contextlib import asynccontextmanager

from app.api import employees, health, insights
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import RequestIdMiddleware, get_logger, setup_logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    setup_logging(settings.log_level)
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)

    @app.exception_handler(Exception)
    async def unhandled(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        log.exception("unhandled error request_id=%s", request_id)
        return JSONResponse(
            status_code=500,
            content={
                "code": "internal_error",
                "message": "unexpected error",
                "details": {},
                "request_id": request_id,
            },
        )

    app.include_router(health.router)
    app.include_router(employees.router)
    app.include_router(insights.router)

    return app


app = create_app()
