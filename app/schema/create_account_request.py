from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    user_name: str
    password: str
