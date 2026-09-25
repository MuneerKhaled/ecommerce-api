from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Job(Base):
    """Model for storing job information."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=False)

    salary = Column(Float, nullable=False)

    vacancies = Column(Integer, nullable=False, default=1)