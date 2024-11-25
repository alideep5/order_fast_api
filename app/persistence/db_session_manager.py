from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


class DbSessionManager:
    def __init__(self):
        self._DATABASE_URL = (
            "postgresql+asyncpg://order:orderpassword@localhost:5432/order"
        )
        self.engine = create_async_engine(
            self._DATABASE_URL,
            echo=True,
            future=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
        )

        self.AsyncSessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self):
        """
        Create a new session and ensure proper cleanup after use.
        """
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
