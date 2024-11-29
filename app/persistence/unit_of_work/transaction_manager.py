from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from app.common.configuration.app_config import AppConfig
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.persistence.unit_of_work.transaction import Transaction


class TransactionManager(ITransactionManager):
    def __init__(self, app_config: AppConfig) -> None:
        self._DATABASE_URL = app_config.database_url
        self.engine = create_async_engine(
            self._DATABASE_URL,
            echo=True,
            future=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
        )

        self.AsyncSessionLocal = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_transaction(self) -> AsyncIterator[Transaction]:
        async with self.AsyncSessionLocal() as session:
            try:
                yield Transaction(session)
            except Exception:
                await session.rollback()
                raise
