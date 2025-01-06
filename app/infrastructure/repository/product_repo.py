from typing import List, Optional
from sqlalchemy import delete, select
from app.domain.entity.product import Product
from app.domain.repository.product_repo import IProductRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.table.product_table import ProductTable
from app.infrastructure.table.shop_table import ShopTable


class ProductRepo(IProductRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_product_shop_owner_id(self, product_id: str) -> Optional[str]:
        stmt = (
            select(ShopTable.owner_id)
            .join(ProductTable, ShopTable.id == ProductTable.shop_id)
            .where(ProductTable.id == product_id)
        )
        result = await self._session.execute(stmt)

        shop_owner_id = result.scalar_one_or_none()

        return shop_owner_id

    async def get_products(
        self,
        shop_id: str,
        search: Optional[str],
        page: int,
        size: int,
    ) -> List[Product]:
        stmt = select(ProductTable).where(ProductTable.shop_id == shop_id)
        if search:
            stmt = stmt.where(ProductTable.name.ilike(f"%{search}%"))
        stmt = stmt.limit(size).offset((page - 1) * size)
        result = await self._session.execute(stmt)

        products = result.scalars().all()
        return [
            Product(
                id=product.id,
                shop_id=product.shop_id,
                name=product.name,
                price=product.price,
            )
            for product in products
        ]

    async def get_product(self, product_id: str) -> Optional[Product]:
        stmt = select(ProductTable).where(ProductTable.id == product_id)
        result = await self._session.execute(stmt)

        product = result.scalar_one_or_none()

        if not product:
            return None

        return Product(
            id=product.id,
            shop_id=product.shop_id,
            name=product.name,
            price=product.price,
        )

    async def create_product(self, shop_id: str, name: str, price: float) -> Product:
        product = ProductTable(shop_id=shop_id, name=name, price=price)

        self._session.add(product)

        await self._session.flush()
        await self._session.refresh(product)

        return Product(
            id=product.id,
            shop_id=product.shop_id,
            name=product.name,
            price=product.price,
        )

    async def update_product(
        self,
        product_id: str,
        name: Optional[str],
        price: Optional[float],
    ) -> Product:
        stmt = select(ProductTable).where(ProductTable.id == product_id)
        result = await self._session.execute(stmt)

        product = result.scalar_one()

        if name is not None:
            product.name = name
        if price is not None:
            product.price = price

        await self._session.flush()
        await self._session.refresh(product)

        return Product(
            id=product.id,
            shop_id=product.shop_id,
            name=product.name,
            price=product.price,
        )

    async def delete_product(self, product_id: str) -> None:
        stmt = delete(ProductTable).where(ProductTable.id == product_id)
        await self._session.execute(stmt)

        await self._session.flush()

    async def get_products_by_ids(self, product_ids: List[str]) -> List[Product]:
        stmt = select(ProductTable).where(ProductTable.id.in_(product_ids))
        result = await self._session.execute(stmt)

        products = result.scalars().all()

        return [
            Product(
                id=product.id,
                shop_id=product.shop_id,
                name=product.name,
                price=product.price,
            )
            for product in products
        ]
