from pydantic import BaseModel, Field


class LoginDTO(BaseModel):
    username: str = Field(..., description="Username of the user.")
    password: str = Field(..., description="Password of the user.")
