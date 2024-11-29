from fastapi import APIRouter
from app.api.dto.create_account_dto import CreateAccountDTO
from app.api.dto.login_dto import LoginDTO
from app.api.dto.login_user_dto import LoginUserDTO
from app.common.model.user_info import UserInfo
from app.api.dto.user_list_dto import UserListDTO
from app.common.utils.dto_util import DTOUtil
from app.domain.entity.login_user import LoginUser
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
            summary="Create User",
            description="Create a user and return a user details",
        )

        self.add_api_route(
            path="/login",
            methods=["POST"],
            endpoint=self.login,
            summary="User Login",
            description="Authenticate a user and return a token",
        )

        self.add_api_route(
            path="/users",
            methods=["GET"],
            endpoint=self.get_users,
            summary="Get Users",
            description="Get all users",
        )

    async def create_account(self, body: CreateAccountDTO) -> UserInfo:
        user: User = await self.user_service.create_account(
            username=body.username, password=body.password
        )
        return DTOUtil.convert_to_dto(user, UserInfo)

    async def login(self, body: LoginDTO) -> LoginUserDTO:
        user: LoginUser = await self.user_service.login(
            username=body.username, password=body.password
        )
        return DTOUtil.convert_to_dto(user, LoginUserDTO)

    async def get_users(self) -> UserListDTO:
        users = await self.user_service.get_users()
        return UserListDTO(users=DTOUtil.convert_to_dto_list(users, UserInfo))
