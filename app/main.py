from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routers import products


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce API",
    description="My first E-Commerce backend API",
    version="1.0.0"
)


app.include_router(products.router)


@app.get("/")
def home():
    return {
        "message": "E-Commerce API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }