from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from app.domain.entity.user import User
from app.domain.entity.user_detail import UserDetail
from app.domain.repository.user_repo import IUserRepo
from app.infrastructure.table.user_table import UserTable


class UserRepo(IUserRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, username: str, password: str) -> User:
        user = UserTable(username=username, password=password)
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return User(id=user.id, username=user.username)

    async def find_by_username(self, username: str) -> Optional[UserDetail]:
        result = await self._session.execute(
            select(UserTable).where(UserTable.username == username)
        )
        user = result.scalars().first()
        return (
            UserDetail(id=user.id, username=user.username, password=user.password)
            if user
            else None
        )

    async def is_username_exists(self, username: str) -> bool:
        result = await self._session.execute(
            select(exists().where(UserTable.username == username))
        )
        return bool(result.scalar())

    async def find_by_id(self, user_id: str) -> Optional[User]:
        result = await self._session.execute(
            select(UserTable).where(UserTable.id == user_id)
        )
        user = result.scalars().first()
        return User(id=user.id, username=user.username) if user else None

    async def get_all_users(self) -> List[User]:
        result = await self._session.execute(select(UserTable))
        users = result.scalars().all()
        return [User(id=user.id, username=user.username) for user in users]
