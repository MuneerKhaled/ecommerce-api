from pydantic import BaseModel, Field


# ============================================================
# Product Create Schema
# ============================================================

class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str = Field(
        min_length=1,
        max_length=500,
    )

    price: float = Field(
        gt=0,
    )

    stock: int = Field(
        ge=0,
    )


# ============================================================
# Product Response Schema
# ============================================================

class ProductResponse(BaseModel):
    """
    Schema for returning product information.
    """

    id: int
    name: str
    description: str
    price: float
    stock: int

    class Config:
        from_attributes = True