from typing import List
from pydantic import BaseModel
from app.api.dto.shop_dto import ShopDTO


class ShopListDTO(BaseModel):
    shops: List[ShopDTO]
