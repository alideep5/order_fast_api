from fastapi import APIRouter
from app.api.v1.dto.create_account_dto import CreateAccountDTO
from app.api.v1.dto.user_dto import UserDTO
from app.domain.entity.user import User
from app.domain.service.user_service import UserService


class UserController(APIRouter):
    def __init__(self, user_service: UserService, prefix: str = "/account"):
        self.user_service = user_service
        super().__init__(prefix=prefix)

        self.tags = ["Account"]
        self.description = "Operations related to user accounts"

        self.add_api_route(
            path="/create-account",
            methods=["POST"],
            endpoint=self.create_account,
            summary="User Login",
            description="Authenticate a user and return a token",
        )

    async def create_account(self, body: CreateAccountDTO) -> UserDTO:
        user_detail: User = await self.user_service.create_account(
            user_name=body.user_name, password=body.password
        )
        return UserDTO(user_id=user_detail.user_id, user_name=user_detail.name)
