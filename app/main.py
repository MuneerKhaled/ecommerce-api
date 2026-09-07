from fastapi import FastAPI

from .database import Base, engine
from .routers.products import router as product_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI app
app = FastAPI(
    title="Online Store API",
    description="Backend API for an online store",
    version="1.0.0",
)


# Register product routes
app.include_router(product_router)


# Home endpoint
@app.get("/")
def index():
    return {
        "message": "Online Store API is active"
    }


# Health endpoint
@app.get("/health")
def status():
    return {
        "status": "up"
    }