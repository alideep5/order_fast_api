from typing import List
import bcrypt
from app.common.model.user_info import UserInfo
from app.domain.entity.login_user import LoginUser
from app.domain.entity.user import User
from app.common.error.response_exception import BadRequestException
from app.common.util.jwt_util import JWTUtil
from app.domain.unit_of_work.transaction_manager import ITransactionManager


class UserService:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        jwt_util: JWTUtil,
    ) -> None:
        self.transaction_manager = transaction_manager
        self.jwt_util = jwt_util

    async def create_account(self, username: str, password: str) -> User:
        async with self.transaction_manager.get_uow() as uow:
            if await uow.user_repo.is_username_exists(username=username):
                raise BadRequestException("Username already exists")
            hashed_password = (
                bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            ).decode("utf-8")
            user: User = await uow.user_repo.create_user(
                username=username, password=hashed_password
            )
            await uow.commit()

            return user

    async def login(self, username: str, password: str) -> LoginUser:
        async with self.transaction_manager.get_uow() as uow:
            user_detail = await uow.user_repo.find_by_username(username=username)
            if not user_detail or not bcrypt.checkpw(
                password.encode("utf-8"), user_detail.password.encode("utf-8")
            ):
                raise BadRequestException("Invalid username or password")

            token = self.jwt_util.generate_token(
                UserInfo(id=user_detail.id, username=user_detail.username)
            )
            return LoginUser(
                id=user_detail.id,
                username=user_detail.username,
                token=token,
            )

    async def get_users(self) -> List[User]:
        async with self.transaction_manager.get_uow() as uow:
            users = await uow.user_repo.get_all_users()
            return users
