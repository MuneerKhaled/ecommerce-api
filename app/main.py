from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Initialize database
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="E-Commerce REST API",
    description="Backend API for managing e-commerce products",
    version="1.0.0",
)


# Include API routers
app.include_router(products.router)


# Root endpoint
@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to the E-Commerce API",
    }