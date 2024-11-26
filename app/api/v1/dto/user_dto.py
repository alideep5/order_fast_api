from pydantic import BaseModel


class UserDTO(BaseModel):
    user_id: str
    user_name: str
