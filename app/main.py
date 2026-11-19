
from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="API for managing products in an online store",
    version="1.2.0",
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
        "message": "E-Commerce API is online",
        "version": "1.2.0",
        "status": "success"
    }


# API status endpoint
@app.get("/health", tags=["General"])
def health():
    return {
        "service": "E-Commerce API",
        "status": "operational"
    }
