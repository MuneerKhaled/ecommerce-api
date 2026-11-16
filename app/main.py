from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Initialize database
Base.metadata.create_all(bind=engine)


# Initialize FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="A RESTful API for managing e-commerce products",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Register API routers
app.include_router(
    products.router,
    tags=["Products"]
)


# Root endpoint
@app.get("/", tags=["General"])
def root():
    return {
        "message": "Welcome to E-Commerce API",
        "version": "1.1.0",
        "status": "running"
    }


# Health check endpoint
@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "service": "E-Commerce API"
    }