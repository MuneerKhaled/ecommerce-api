from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Initialize database
def initialize_database():
    Base.metadata.create_all(bind=engine)


# Initialize database before starting the API
initialize_database()


# FastAPI application instance
app = FastAPI(
    title="E-Commerce Service",
    description="RESTful API for managing an E-Commerce application",
    version="1.0.0",
)


# Add product routes
app.include_router(products.router)


# API root
@app.get("/")
def root():
    return {"message": "Welcome to the E-Commerce API"}


# API health status
@app.get("/health")
def health():
    return {"status": "OK"}