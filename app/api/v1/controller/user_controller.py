from fastapi import APIRouter
from domain.model.user_detail import UserDetail
from domain.service.user_service import UserService
from schema.create_account_request import CreateAccountRequest
from schema.create_account_response import CreateAccountResponse


class UserController(APIRouter):
    def __init__(self, prefix: str = "/account"):
        super().__init__(prefix=prefix)
        self.tags = ["Account"]
        self.description = "Operations related to user accounts"
        self.user_service = UserService()
        self.add_api_route(
            path="/create-account",
            methods=["POST"],
            endpoint=self.create_account,
            summary="User Login",
            description="Authenticate a user and return a token",
        )

    async def create_account(self, body: CreateAccountRequest) -> CreateAccountResponse:
        user_detail: UserDetail = self.user_service.create_account(
            user_name=body.user_name, password=body.password
        )
        return CreateAccountResponse(
            user_id=user_detail.user_id, user_name=user_detail.name
        )
