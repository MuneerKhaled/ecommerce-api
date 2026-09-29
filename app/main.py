from fastapi import FastAPI

from .database import Base, engine
from .routers.products import router as products_router


# ============================================================
# Database Setup
# ============================================================

def setup_database() -> None:
    """
    Create database tables defined by SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)


# Initialize database
setup_database()


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="E-Commerce Backend API",
    version="1.0.0",
    description="Backend API for an online e-commerce system.",
)


# ============================================================
# API Routes
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
def welcome() -> dict:
    """
    API welcome endpoint.
    """
    return {
        "message": "Welcome to the E-Commerce API",
        "version": "1.0.0",
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health_check() -> dict:
    """
    Check whether the API is running.
    """
    return {
        "status": "healthy",
    }