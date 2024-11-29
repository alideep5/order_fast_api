from typing import List
from pydantic import BaseModel
from app.common.model.user_info import UserInfo


class UserListDTO(BaseModel):
    users: List[UserInfo]
