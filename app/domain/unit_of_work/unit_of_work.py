from typing import Any, AsyncContextManager, Protocol
from app.domain.unit_of_work.transaction import ITransaction


class IUnitOfWork(Protocol):
    def get_transaction(self) -> AsyncContextManager[ITransaction[Any]]:
        pass
