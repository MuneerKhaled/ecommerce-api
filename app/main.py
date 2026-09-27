from fastapi import FastAPI

from .database import Base, engine
from .routers.tasks import router


# Prepare database
def setup_database():
    Base.metadata.create_all(bind=engine)


setup_database()


# Create application
api = FastAPI(
    title="Task Management Backend",
    version="1.0.0",
    description="REST API backend for managing users and tasks",
)


# Attach task routes
api.include_router(router)


# Welcome endpoint
@api.get("/")
def welcome():
    return {
        "message": "Welcome to the Task Management API"
    }


# Health endpoint
@api.get("/health")
def check_status():
    return {
        "status": "running",
        "service": "task-management-api"
    }


# Application instance
app = api