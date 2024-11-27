from app.domain.entity.user import User
from app.domain.unit_of_work.transaction import ITransaction
from sqlalchemy.ext.asyncio import AsyncSession
from app.persistence.table.user_table import UserTable
from typing import cast
from app.persistence.unit_of_work.transaction import Transaction


class UserRepo:
    async def create_user(
        self, transaction: ITransaction, username: str, password: str
    ) -> User:
        session: AsyncSession = cast(Transaction, transaction).get_session()

        user = UserTable(username=username, password=password)
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return User(user_id=user.id, name=user.username)
