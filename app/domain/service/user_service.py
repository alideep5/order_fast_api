from typing import List
import bcrypt
from app.domain.entity.login_user import LoginUser
from app.domain.entity.user import User
from app.common.error.response_exception import BadRequestException
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.common.utils.jwt_util import JWTUtil
from app.infrastructure.repository.user_repo import UserRepo


class UserService:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        jwt_util: JWTUtil,
        user_repo: UserRepo,
    ) -> None:
        self.transaction_manager = transaction_manager
        self.jwt_util = jwt_util
        self.user_repo = user_repo

    async def create_account(self, username: str, password: str) -> User:
        async with self.transaction_manager.get_transaction() as transaction:
            if await self.user_repo.is_username_exists(transaction, username=username):
                raise BadRequestException("Username already exists")
            hashed_password = (
                bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            ).decode("utf-8")
            user: User = await self.user_repo.create_user(
                transaction=transaction, username=username, password=hashed_password
            )
            await transaction.commit()

            return user

    async def login(self, username: str, password: str) -> LoginUser:
        async with self.transaction_manager.get_transaction() as transaction:
            user_detail = await self.user_repo.find_by_username(
                transaction, username=username
            )
            if not user_detail or not bcrypt.checkpw(
                password.encode("utf-8"), user_detail.password.encode("utf-8")
            ):
                raise BadRequestException("Invalid username or password")

            token = self.jwt_util.generate_token(user_detail.id)
            return LoginUser(
                id=user_detail.id,
                username=user_detail.username,
                token=token,
            )

    async def get_users(self) -> List[User]:
        async with self.transaction_manager.get_transaction() as transaction:
            users = await self.user_repo.get_all_users(transaction)
            return users
