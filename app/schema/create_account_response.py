from pydantic import BaseModel


class CreateAccountResponse(BaseModel):
    user_id: str
    user_name: str
