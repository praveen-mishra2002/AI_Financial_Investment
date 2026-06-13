"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()
    app = FastAPI(title=settings.app_name, version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["Health"])
    async def health() -> dict[str, str]:
        """Return service health."""
        return {"status": "ok", "service": settings.app_name}

    return app


app = create_app()
