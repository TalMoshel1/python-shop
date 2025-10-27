from fastapi import FastAPI
from app.core.logging_config import setup_logging
from app.core.config import get_settings
from app.core.error_handler import register_exception_handlers
from app.db.database import engine
from app.db import models
from app.routers import products, orders, health, auth


def create_app() -> FastAPI:
    setup_logging()
    settings = get_settings()

    # dev bootstrap tables (SQLite or first run with Postgres)
    models.Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="Shop API",
        version="1.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_exception_handlers(app)

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(products.router)
    app.include_router(orders.router)

    @app.get("/")
    def root():
        return {
            "name": "Shop API",
            "env": settings.ENV,
            "docs": "/docs",
        }

    return app


app = create_app()
