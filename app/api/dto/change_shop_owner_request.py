from pydantic import BaseModel, Field


class ChangeShopOwnerRequest(BaseModel):
    new_owner_id: str = Field(..., description="The UUID of the new shop owner")
