from typing import List
from pydantic import BaseModel
from app.api.dto.user_dto import UserDTO


class UserListDTO(BaseModel):
    users: List[UserDTO]
