from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    id: str
    username: str
    token: str
