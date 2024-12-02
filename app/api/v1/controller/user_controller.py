from fastapi import APIRouter, Depends
from app.api.dto.create_account_dto import CreateAccountDTO
from app.api.dto.login_dto import LoginDTO
from app.api.dto.login_user_dto import LoginUserDTO
from app.common.model.user_info import UserInfo
from app.api.dto.user_list_dto import UserListDTO
from app.common.util.dto_util import DTOUtil
from app.common.util.request_util import RequestUtil
from app.domain.entity.login_user import LoginUser
from app.domain.entity.user import User
from app.domain.service.user_service import UserService


class UserController(APIRouter):
    def __init__(self, user_service: UserService, prefix: str = "/account"):
        super().__init__(prefix=prefix)
        self.user_service = user_service

        self.add_api_route(
            path="/create-account",
            methods=["POST"],
            status_code=201,
            endpoint=self.create_account,
            tags=["Account"],
            summary="Create User Account",
            description="Endpoint to create a new user account. Returns user details upon successful creation.",
        )
        self.add_api_route(
            path="/login",
            methods=["POST"],
            endpoint=self.login,
            tags=["Account"],
            summary="User Login",
            description="Endpoint to authenticate a user. Returns a token upon successful authentication.",
        )
        self.add_api_route(
            path="/users",
            methods=["GET"],
            endpoint=self.get_users,
            tags=["User"],
            summary="Retrieve All Users",
            description="Endpoint to fetch the list of all registered users.",
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

    async def get_users(
        self, user: UserInfo = Depends(RequestUtil.get_auth_user)
    ) -> UserListDTO:
        users = await self.user_service.get_users()
        return UserListDTO(users=DTOUtil.convert_to_dto_list(users, UserInfo))
