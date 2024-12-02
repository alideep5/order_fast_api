from typing import Any, List, Optional
from sqlalchemy import delete, select, update
from app.domain.entity.shop import Shop
from app.domain.unit_of_work.transaction import ITransaction
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.table.shop_table import ShopTable


class ShopRepo:
    async def create_shop(
        self, transaction: ITransaction[Any], owner_id: str, name: str, address: str
    ) -> Shop:
        session: AsyncSession = transaction.get_session()

        shop = ShopTable(owner_id=owner_id, name=name, address=address)
        session.add(shop)

        await session.flush()
        await session.refresh(shop)

        return Shop(
            id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
        )

    async def get_all_shops(self, transaction: ITransaction[Any]) -> List[Shop]:
        session: AsyncSession = transaction.get_session()

        result = await session.execute(select(ShopTable))

        shops = result.scalars().all()

        return [
            Shop(
                id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
            )
            for shop in shops
        ]

    async def get_shop(
        self, transaction: ITransaction[Any], shop_id: str
    ) -> Optional[Shop]:
        session: AsyncSession = transaction.get_session()

        result = await session.execute(select(ShopTable).where(ShopTable.id == shop_id))

        shop = result.scalar_one_or_none()

        if not shop:
            return None
        return Shop(
            id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
        )

    async def update_shop(
        self,
        transaction: ITransaction[Any],
        shop_id: str,
        name: Optional[str],
        address: Optional[str],
    ) -> Shop:
        session: AsyncSession = transaction.get_session()

        result = await session.execute(select(ShopTable).where(ShopTable.id == shop_id))

        shop = result.scalar_one()

        if name is not None:
            shop.name = name
        if address is not None:
            shop.address = address

        await session.flush()
        await session.refresh(shop)

        return Shop(
            id=shop.id, owner_id=shop.owner_id, name=shop.name, address=shop.address
        )

    async def delete_shop(self, transaction: ITransaction[Any], shop_id: str) -> None:
        session: AsyncSession = transaction.get_session()
        await session.execute(delete(ShopTable).where(ShopTable.id == shop_id))
        await session.flush()

    async def change_owner(
        self, transaction: ITransaction[Any], shop_id: str, new_owner_id: str
    ) -> None:
        session: AsyncSession = transaction.get_session()

        stmt = (
            update(ShopTable)
            .where(ShopTable.id == shop_id)
            .values(owner_id=new_owner_id)
        )
        await session.execute(stmt)

        await session.flush()
