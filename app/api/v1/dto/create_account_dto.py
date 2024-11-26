from pydantic import BaseModel


class CreateAccountDTO(BaseModel):
    user_name: str
    password: str
