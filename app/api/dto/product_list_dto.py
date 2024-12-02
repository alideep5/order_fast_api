from typing import List
from pydantic import BaseModel
from app.api.dto.product_dto import ProductDTO


class ProductListDTO(BaseModel):
    products: List[ProductDTO]
