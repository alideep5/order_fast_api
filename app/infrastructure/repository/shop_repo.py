from typing import List, Optional
from sqlalchemy import delete, select, update
from app.domain.entity.shop import Shop
from app.domain.repository.shop_repo import IShopRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.table.shop_table import ShopTable


class ShopRepo(IShopRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_shop(self, owner_id: str, name: str, address: str) -> Shop:
        shop = ShopTable(owner_id=owner_id, name=name, address=address)
        self._session.add(shop)

        await self._session.flush()
        await self._session.refresh(shop)

        return Shop(
            id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
        )

    async def get_all_shops(self) -> List[Shop]:
        result = await self._session.execute(select(ShopTable))

        shops = result.scalars().all()

        return [
            Shop(
                id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
            )
            for shop in shops
        ]

    async def get_shop(self, shop_id: str) -> Optional[Shop]:
        result = await self._session.execute(
            select(ShopTable).where(ShopTable.id == shop_id)
        )

        shop = result.scalar_one_or_none()

        if not shop:
            return None
        return Shop(
            id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
        )

    async def update_shop(
        self,
        shop_id: str,
        name: Optional[str],
        address: Optional[str],
    ) -> Shop:
        result = await self._session.execute(
            select(ShopTable).where(ShopTable.id == shop_id)
        )

        shop = result.scalar_one()

        if name is not None:
            shop.name = name
        if address is not None:
            shop.address = address

        await self._session.flush()
        await self._session.refresh(shop)

        return Shop(
            id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
        )

    async def delete_shop(self, shop_id: str) -> None:
        await self._session.execute(delete(ShopTable).where(ShopTable.id == shop_id))
        await self._session.flush()

    async def change_owner(self, shop_id: str, new_owner_id: str) -> None:
        stmt = (
            update(ShopTable)
            .where(ShopTable.id == shop_id)
            .values(owner_id=new_owner_id)
        )
        await self._session.execute(stmt)

        await self._session.flush()
