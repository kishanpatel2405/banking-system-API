from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import api_router
from config import settings
from core.error_handlers import api_exception_handler
from core.event_handlers import start_app_handler, stop_app_handler
from utils.errors import ApiException
from utils.misc import get_project_meta


def get_app() -> FastAPI:
    pkg_meta = get_project_meta("pyproject.toml")

    fast_app = FastAPI(
        title="Banking System API",
        description="A comprehensive API for managing banking operations.",
        version=pkg_meta.get("version", "unknown"),
        debug=settings.ENVIRONMENT != "production",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url=None
    )

    if settings.BACKEND_CORS_ORIGINS:
        fast_app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    fast_app.include_router(api_router)

    fast_app.add_exception_handler(ApiException, api_exception_handler)

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    return fast_app


app = get_app()
