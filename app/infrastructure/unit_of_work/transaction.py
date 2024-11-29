from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.unit_of_work.transaction import ITransaction


class Transaction(ITransaction[AsyncSession]):
    def __init__(self, session: AsyncSession):
        self._session = session

    def get_session(self) -> AsyncSession:
        return self._session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
