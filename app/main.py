from fastapi import FastAPI

from .database import Base, engine
from .routers.products import router as product_router


# Setup database
Base.metadata.create_all(bind=engine)


# Initialize API
application = FastAPI(
    title="Online Store API",
    version="1.0.0",
    description="Backend API for an online store",
)


# Connect product endpoints
application.include_router(product_router)


# Default route
@application.get("/")
def index():
    return {
        "message": "Online Store API is active"
    }


# Server status route
@application.get("/health")
def status():
    return {
        "status": "up"
    }


app = application