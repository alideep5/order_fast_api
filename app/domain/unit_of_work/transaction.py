from typing import Protocol, TypeVar, Generic

T = TypeVar("T", covariant=True)


class ITransaction(Protocol, Generic[T]):
    def get_session(self) -> T:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
