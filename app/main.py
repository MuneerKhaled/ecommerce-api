from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: clean up resources if needed


# Create FastAPI application
app = FastAPI(
    title="E-Commerce API",
    description="REST API for managing e-commerce products",
    version="1.0.0",
    lifespan=lifespan,
)


# Allow frontend apps to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(products.router)


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "E-Commerce API is running",
        "status": "success",
    }


# Health check endpoint
@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}