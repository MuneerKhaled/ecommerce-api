from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="REST API for managing products in an e-commerce system",
    version="1.0.0",
)


# Register product routes
app.include_router(products.router)


# API health check
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "E-Commerce API is running",
    }