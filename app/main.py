from fastapi import FastAPI

from .database import Base, engine
from .routers.products import router as product_routes


# ============================================================
# Database Initialization
# ============================================================

def create_database() -> None:
    """Create the required database tables."""
    Base.metadata.create_all(bind=engine)


create_database()


# ============================================================
# Application Setup
# ============================================================

app = FastAPI(
    title="Product Management API",
    description="Backend API for creating and managing e-commerce products.",
    version="1.0.0",
)


# ============================================================
# API Routes
# ============================================================

app.include_router(
    product_routes,
    prefix="/products",
    tags=["Product Management"],
)


# ============================================================
# API Information
# ============================================================

@app.get("/")
def home():
    """Display basic API information."""
    return {
        "name": "Product Management API",
        "version": app.version,
        "status": "running",
        "docs": "/docs",
    }


# ============================================================
# Server Health
# ============================================================

@app.get("/health")
def health():
    """Return the current API health status."""
    return {
        "status": "ok",
        "service": "product-api",
    }