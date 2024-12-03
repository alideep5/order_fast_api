from typing import Any
import unittest
from unittest.mock import AsyncMock, MagicMock
import bcrypt
from app.domain.service.user_service import UserService
from app.domain.entity.user import User
from app.domain.entity.login_user import LoginUser
from app.common.error.response_exception import BadRequestException
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.common.util.jwt_util import JWTUtil
from app.domain.repository.user_repo import IUserRepo


class TestUserService(unittest.IsolatedAsyncioTestCase):
    transaction_manager: AsyncMock
    jwt_util: MagicMock
    user_repo: AsyncMock
    service: UserService

    def setUp(self) -> None:
        self.transaction_manager = AsyncMock(spec=ITransactionManager)
        self.jwt_util = MagicMock(spec=JWTUtil)
        self.user_repo = AsyncMock(spec=IUserRepo)
        self.service = UserService(
            transaction_manager=self.transaction_manager,
            jwt_util=self.jwt_util,
            user_repo=self.user_repo,
        )

    async def test_create_account_success(self) -> None:
        self.user_repo.is_username_exists.return_value = False
        transaction: AsyncMock = AsyncMock()
        self.transaction_manager.get_transaction.return_value.__aenter__.return_value = (
            transaction
        )
        self.user_repo.create_user.return_value = User(id="1", username="test_user")

        user: User = await self.service.create_account("test_user", "secure_password")

        self.user_repo.is_username_exists.assert_awaited_once_with(
            transaction, username="test_user"
        )
        self.user_repo.create_user.assert_awaited_once_with(
            transaction=transaction, username="test_user", password=Any
        )
        transaction.commit.assert_awaited_once()
        assert user.username == "test_user"

    async def test_create_account_username_exists(self) -> None:
        self.user_repo.is_username_exists.return_value = True
        transaction: AsyncMock = AsyncMock()
        self.transaction_manager.get_transaction.return_value.__aenter__.return_value = (
            transaction
        )

        with self.assertRaises(BadRequestException):
            await self.service.create_account("test_user", "secure_password")

        self.user_repo.is_username_exists.assert_awaited_once_with(
            transaction, username="test_user"
        )
        self.user_repo.create_user.assert_not_awaited()

    async def test_login_success(self) -> None:
        hashed_password: str = bcrypt.hashpw(
            "secure_password".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user_detail = MagicMock(id="1", username="test_user", password=hashed_password)
        self.user_repo.find_by_username.return_value = user_detail
        self.jwt_util.generate_token.return_value = "mock_token"

        login_user: LoginUser = await self.service.login("test_user", "secure_password")

        self.user_repo.find_by_username.assert_awaited_once_with(
            Any, username="test_user"
        )
        self.jwt_util.generate_token.assert_called_once_with(Any)
        assert login_user.token == "mock_token"

    async def test_login_invalid_credentials(self) -> None:
        self.user_repo.find_by_username.return_value = None

        with self.assertRaises(BadRequestException):
            await self.service.login("test_user", "wrong_password")

        self.user_repo.find_by_username.assert_awaited_once_with(
            Any, username="test_user"
        )
        self.jwt_util.generate_token.assert_not_called()

    async def test_get_users(self) -> None:
        mock_users = [User(id="1", username="user1"), User(id="2", username="user2")]
        self.user_repo.get_all_users.return_value = mock_users
        transaction: AsyncMock = AsyncMock()
        self.transaction_manager.get_transaction.return_value.__aenter__.return_value = (
            transaction
        )

        users = await self.service.get_users()

        self.user_repo.get_all_users.assert_awaited_once_with(transaction)
        assert len(users) == 2
        assert users[0].username == "user1"
