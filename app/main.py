from fastapi import FastAPI

from .database import Base, engine
from .routers import products


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce API",
    description="A simple E-Commerce REST API built with FastAPI and SQLAlchemy",
    version="1.0.0",
)


# Register routers
app.include_router(products.router)


@app.get("/")
def root():
    return {
        "message": "E-Commerce API is running"
    }