from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Initialize database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="REST API for managing products in an online store",
    version="1.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Register product routes
app.include_router(
    products.router,
    prefix="/api",
    tags=["Products"]
)


# Root endpoint
@app.get("/", tags=["General"])
def home():
    return {
        "message": "Welcome to the E-Commerce API",
        "version": "1.3.0",
        "status": "running"
    }


# Health check endpoint
@app.get("/health", tags=["General"])
def health():
    return {
        "service": "E-Commerce API",
        "status": "healthy",
        "database": "connected"
    }