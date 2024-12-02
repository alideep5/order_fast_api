from pydantic import BaseModel
from app.common.model.user_info import UserInfo


class ShopDTO(BaseModel):
    id: str
    name: str
    address: str
    owner_id: str
