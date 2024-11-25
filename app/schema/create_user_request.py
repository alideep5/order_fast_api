from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    user_name: str
    password: str