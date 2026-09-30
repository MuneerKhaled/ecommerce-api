from pydantic import BaseModel, Field, ConfigDict


# ============================================================
# Product Input Schema
# ============================================================

class ProductCreate(BaseModel):
    """Data required to create a product."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product name",
    )

    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Product description",
    )

    price: float = Field(
        ...,
        gt=0,
        description="Product price",
    )

    stock: int = Field(
        ...,
        ge=0,
        description="Available stock quantity",
    )


# ============================================================
# Product Output Schema
# ============================================================

class ProductResponse(BaseModel):
    """Product data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    stock: int