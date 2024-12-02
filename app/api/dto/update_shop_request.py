from pydantic import BaseModel, Field
from typing import Optional


class UpdateShopRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=20, description="Name of the shop"
    )
    address: Optional[str] = Field(
        None, min_length=3, max_length=256, description="Address of the shop"
    )
