from typing import AsyncContextManager, Protocol
from app.domain.unit_of_work.transaction import ITransaction


class ITransactionManager(Protocol):
    def get_transaction(self) -> AsyncContextManager[ITransaction]:
        pass
