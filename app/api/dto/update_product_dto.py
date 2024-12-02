from pydantic import BaseModel, Field
from typing import Optional


class UpdateProductDTO(BaseModel):
    name: Optional[str] = Field(
        None, min_length=2, max_length=20, description="Name of the product"
    )
    price: Optional[float] = Field(
        None,
        gt=0,
        description="Price of the product, must be greater than 0 if provided",
    )
