
from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="E-Commerce REST API",
    description="Backend API for managing e-commerce products",
    version="1.0.0",
)


# Register product routes
app.include_router(products.router)


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to the E-Commerce API",
    }