from typing import List, Optional
from app.common.error.response_exception import BadRequestException, ForbiddenException
from app.common.model.user_info import UserInfo
from app.domain.entity.product import Product
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.infrastructure.repository.product_repo import ProductRepo
from app.infrastructure.repository.shop_repo import ShopRepo
from app.infrastructure.repository.user_repo import UserRepo


class ProductService:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        product_repo: ProductRepo,
        shop_repo: ShopRepo,
    ) -> None:
        self.transaction_manager = transaction_manager
        self.product_repo = product_repo
        self.shop_repo = shop_repo

    async def get_products(
        self,
        shop_id: str,
        page: int,
        size: int,
        search: Optional[str],
    ) -> List[Product]:
        async with self.transaction_manager.get_transaction() as transaction:
            return await self.product_repo.get_products(
                transaction=transaction,
                shop_id=shop_id,
                search=search,
                page=page,
                size=size,
            )

    async def get_product(self, product_id: str) -> Product:
        async with self.transaction_manager.get_transaction() as transaction:
            product = await self.product_repo.get_product(
                transaction=transaction,
                product_id=product_id,
            )

            if not product:
                raise BadRequestException("Product not found")

            return product

    async def create_product(
        self, user: UserInfo, shop_id: str, name: str, price: float
    ) -> Product:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await self.shop_repo.get_shop(
                transaction=transaction, shop_id=shop_id
            )

            if not shop:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user.id:
                raise ForbiddenException(
                    "You are not allowed to add product to this shop"
                )

            product = await self.product_repo.create_product(
                transaction=transaction,
                shop_id=shop_id,
                name=name,
                price=price,
            )
            await transaction.commit()

            return product

    async def update_product(
        self,
        user: UserInfo,
        product_id: str,
        name: Optional[str],
        price: Optional[float],
    ) -> Product:
        async with self.transaction_manager.get_transaction() as transaction:
            product_shop_owner_id = await self.product_repo.get_product_shop_owner_id(
                transaction=transaction,
                product_id=product_id,
            )

            if not product_shop_owner_id:
                raise BadRequestException("Product not found")

            if product_shop_owner_id != user.id:
                raise ForbiddenException("You are not allowed to update this product")

            product = await self.product_repo.update_product(
                transaction=transaction,
                product_id=product_id,
                name=name,
                price=price,
            )
            await transaction.commit()

            return product

    async def delete_product(self, user: UserInfo, product_id: str) -> Product:
        async with self.transaction_manager.get_transaction() as transaction:
            product = await self.product_repo.get_product(
                transaction=transaction,
                product_id=product_id,
            )

            if not product:
                raise BadRequestException("Product not found")

            product_shop_owner_id = await self.product_repo.get_product_shop_owner_id(
                transaction=transaction,
                product_id=product_id,
            )

            if product_shop_owner_id != user.id:
                raise ForbiddenException("You are not allowed to delete this product")

            await self.product_repo.delete_product(
                transaction=transaction,
                product_id=product_id,
            )
            await transaction.commit()

            return product
