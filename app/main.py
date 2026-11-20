
from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Initialize database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI application
app = FastAPI(
    title="Online Store API",
    description="Backend API for an online shopping platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Register product routes
app.include_router(
    products.router,
    prefix="/api/products",
    tags=["Product Management"]
)


# Root endpoint
@app.get("/", tags=["Main"])
def root():
    return {
        "message": "Welcome to Online Store API",
        "version": "2.0.0",
        "status": "running"
    }


# Health check endpoint
@app.get("/health", tags=["Main"])
def health_check():
    return {
        "application": "Online Store API",
        "status": "healthy",
        "database": "connected"
    }
