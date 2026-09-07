from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Product(Base):
    """Database model representing a product."""

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    description = Column(
        String,
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
    )

    stock = Column(
        Integer,
        default=0,
        nullable=False,
    )