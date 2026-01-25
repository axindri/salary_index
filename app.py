from fastapi import FastAPI
from fastapi.routing import APIRoute

from src.api import router
from src.config import settings
from src.logger import setup_logging

setup_logging()
app = FastAPI(
    debug=settings.debug,
    version=settings.version,
    title="Salary index API",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)
app.include_router(router)


@app.get("/")
async def home() -> dict[str, str | list[str]]:
    routes = app.routes
    api_routes = []
    for route in routes:
        if isinstance(route, APIRoute) and route.path.startswith("/api"):
            api_routes.append(str(route.path))
    return {
        "app_version": settings.version,
        "available_routes": api_routes,
    }
