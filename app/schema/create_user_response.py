from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    user_id: str
    user_name: str
