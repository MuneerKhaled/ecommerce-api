from fastapi import FastAPI

from .database import Base, engine
from .routers.products import router


# Prepare database
def setup_database():
    Base.metadata.create_all(bind=engine)


setup_database()


# Create application
api = FastAPI(
    title="E-Commerce Backend",
    version="1.0.0",
    description="API backend for an online shopping system",
)


# Attach product routes
api.include_router(router)


# Welcome endpoint
@api.get("/")
def welcome():
    return {
        "message": "Welcome to the E-Commerce API"
    }


# Health endpoint
@api.get("/health")
def check_status():
    return {
        "status": "running"
    }


app = api