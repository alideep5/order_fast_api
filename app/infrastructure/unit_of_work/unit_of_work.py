from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repository.product_repo import IProductRepo
from app.domain.repository.shop_repo import IShopRepo
from app.domain.repository.user_repo import IUserRepo
from app.domain.unit_of_work.unit_of_work import IUnitOfWork
from app.infrastructure.repository.product_repo import ProductRepo
from app.infrastructure.repository.shop_repo import ShopRepo
from app.infrastructure.repository.user_repo import UserRepo


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._product_repo: Optional[IProductRepo] = None
        self._shop_repo: Optional[IShopRepo] = None
        self._user_repo: Optional[IUserRepo] = None

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    @property
    def product_repo(self) -> IProductRepo:
        if self._product_repo is None:
            self._product_repo = ProductRepo(self._session)

        return self._product_repo

    @property
    def shop_repo(self) -> IShopRepo:
        if self._shop_repo is None:
            self._shop_repo = ShopRepo(self._session)

        return self._shop_repo

    @property
    def user_repo(self) -> IUserRepo:
        if self._user_repo is None:
            self._user_repo = UserRepo(self._session)

        return self._user_repo
