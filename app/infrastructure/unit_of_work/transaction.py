from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.repository.product_repo import IProductRepo
from app.domain.repository.shop_repo import IShopRepo
from app.domain.repository.user_repo import IUserRepo
from app.domain.unit_of_work.transaction import ITransaction
from app.infrastructure.repository.product_repo import ProductRepo
from app.infrastructure.repository.shop_repo import ShopRepo
from app.infrastructure.repository.user_repo import UserRepo


class Transaction(ITransaction):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    @property
    def product_repo(self) -> IProductRepo:
        return ProductRepo(self._session)

    @property
    def shop_repo(self) -> IShopRepo:
        return ShopRepo(self._session)

    @property
    def user_repo(self) -> IUserRepo:
        return UserRepo(self._session)
