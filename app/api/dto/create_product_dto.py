from pydantic import BaseModel


from pydantic import BaseModel, Field


class CreateProductDTO(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=20, description="Name of the product"
    )
    price: float = Field(
        ..., gt=0, description="Price of the product, must be greater than 0"
    )
