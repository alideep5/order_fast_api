from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager
from app.common.model.app_config import AppConfig
from app.common.app_logger import AppLogger
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.infrastructure.unit_of_work.transaction import Transaction


class TransactionManager(ITransactionManager):
    def __init__(self, app_config: AppConfig, log: AppLogger) -> None:
        self._DATABASE_URL = app_config.database_url
        self.log = log
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
            except Exception as e:
                await session.rollback()
                self.log.error(
                    f"Transaction failed and rolled back due to an error: {e}"
                )
                raise
