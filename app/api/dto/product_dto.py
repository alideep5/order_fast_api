from pydantic import BaseModel


class ProductDTO(BaseModel):
    id: str
    shop_id: str
    name: str
    price: float
