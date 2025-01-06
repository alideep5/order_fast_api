from typing import Protocol
from app.domain.repository.product_repo import IProductRepo
from app.domain.repository.shop_repo import IShopRepo
from app.domain.repository.user_repo import IUserRepo


class IUnitOfWork(Protocol):
    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    @property
    def product_repo(self) -> IProductRepo:
        pass

    @property
    def shop_repo(self) -> IShopRepo:
        pass

    @property
    def user_repo(self) -> IUserRepo:
        pass
