from pydantic import BaseModel, Field


class CreateShopRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=20, description="Name of the shop")
    address: str = Field(
        ..., min_length=3, max_length=256, description="Address of the shop"
    )
