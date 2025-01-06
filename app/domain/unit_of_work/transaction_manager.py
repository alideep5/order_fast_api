from typing import AsyncContextManager, Protocol
from app.domain.unit_of_work.unit_of_work import IUnitOfWork


class ITransactionManager(Protocol):
    def get_uow(self) -> AsyncContextManager[IUnitOfWork]:
        pass
