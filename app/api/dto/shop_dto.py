from pydantic import BaseModel


class ShopDTO(BaseModel):
    id: str
    name: str
    address: str
    owner_id: str
