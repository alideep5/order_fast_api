from pydantic import BaseModel, Field


class CreateAccountDTO(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=20, description="Username for the account"
    )
    password: str = Field(
        ..., min_length=6, max_length=25, description="Password for the account"
    )
