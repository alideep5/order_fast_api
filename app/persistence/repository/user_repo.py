from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from app.domain.entity.user import User
from app.domain.entity.user_detail import UserDetail
from app.domain.unit_of_work.transaction import ITransaction
from app.persistence.table.user_table import UserTable
from app.persistence.unit_of_work.transaction import Transaction
from typing import Any, cast


class UserRepo:
    async def create_user(
        self, transaction: ITransaction[Any], username: str, password: str
    ) -> User:
        session: AsyncSession = cast(Transaction, transaction).get_session()
        user = UserTable(username=username, password=password)
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return User(id=user.id, username=user.username)

    async def find_by_username(
        self, transaction: ITransaction[Any], username: str
    ) -> Optional[UserDetail]:
        session: AsyncSession = cast(Transaction, transaction).get_session()
        result = await session.execute(
            select(UserTable).where(UserTable.username == username)
        )
        user = result.scalars().first()
        return (
            UserDetail(id=user.id, username=user.username, password=user.password)
            if user
            else None
        )

    async def is_username_exists(
        self, transaction: ITransaction[Any], username: str
    ) -> bool:
        session: AsyncSession = cast(Transaction, transaction).get_session()
        result = await session.execute(
            select(exists().where(UserTable.username == username))
        )
        return bool(result.scalar())

    async def find_by_id(
        self, transaction: ITransaction[Any], user_id: str
    ) -> Optional[User]:
        session: AsyncSession = cast(Transaction, transaction).get_session()
        result = await session.execute(select(UserTable).where(UserTable.id == user_id))
        user = result.scalars().first()
        return User(id=user.id, username=user.username) if user else None

    async def get_all_users(self, transaction: ITransaction[Any]) -> List[User]:
        session: AsyncSession = cast(Transaction, transaction).get_session()
        result = await session.execute(select(UserTable))
        users = result.scalars().all()
        return [User(id=user.id, username=user.username) for user in users]
