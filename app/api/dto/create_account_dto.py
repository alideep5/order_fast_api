from pydantic import BaseModel


class CreateAccountDTO(BaseModel):
    username: str
    password: str
