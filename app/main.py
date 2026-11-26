from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="API for managing products in an online store",
    version="1.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Include product routes
app.include_router(
    products.router,
    prefix="/api",
    tags=["Products"]
)


# Main endpoint
@app.get("/", tags=["General"])
def home():
    return {
        "message": "Welcome to E-Commerce API",
        "version": "1.3.0",
        "status": "success"
    }


# API status endpoint
@app.get("/health", tags=["General"])
def health():
    return {
        "service": "E-Commerce API",
        "status": "operational"
    }


# API information endpoint
@app.get("/info", tags=["General"])
def info():
    return {
        "name": "E-Commerce API",
        "description": "API for managing products in an online store",
        "documentation": "/docs",
        "version": "1.3.0"
    }