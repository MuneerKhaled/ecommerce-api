from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI applicaton
app = FastAPI(
    title="E-Commerce API",
    description="REST API for managing e-commerce products",
    version="1.0.0",
)


# Register routes
app.include_router(products.router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "E-Commerce API is running",
        "status": "success"
    }