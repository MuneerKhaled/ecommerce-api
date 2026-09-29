from fastapi import FastAPI

from .database import Base, engine
from .routers.products import router as products_router


# ============================================================
# Database Configuration
# ============================================================

def initialize_database() -> None:
    """
    Create all database tables defined by the SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)


# Initialize database
initialize_database()


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    description="REST API for managing products in an e-commerce application.",
)


# ============================================================
# Product Routes
# ============================================================

app.include_router(
    products_router,
    prefix="/products",
    tags=["Products"],
)


# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
def root() -> dict:
    """
    Return basic information about the API.
    """
    return {
        "message": "Welcome to the E-Commerce API",
        "version": "1.0.0",
        "documentation": "/docs",
    }


# ============================================================
# Health Check Endpoint
# ============================================================

@app.get("/health")
def health_check() -> dict:
    """
    Check whether the API is running correctly.
    """
    return {
        "status": "healthy",
        "message": "API is running",
    }