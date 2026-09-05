from fastapi import FastAPI

from . import models
from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="A REST API for an E-Commerce application",
    version="1.0.0",
)


# Register routers
app.include_router(products.router)


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "E-Commerce API is running!"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }