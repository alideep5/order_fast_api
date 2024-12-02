from typing import List, Optional
from app.common.error.response_exception import BadRequestException, ForbiddenException
from app.common.model.user_info import UserInfo
from app.domain.entity.shop import Shop
from app.domain.repository.shop_repo import IShopRepo
from app.domain.repository.user_repo import IUserRepo
from app.domain.unit_of_work.transaction_manager import ITransactionManager


class ShopService:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        shop_repo: IShopRepo,
        user_repo: IUserRepo,
    ) -> None:
        self.transaction_manager = transaction_manager
        self.shop_repo = shop_repo
        self.user_repo = user_repo

    async def createShop(self, user_info: UserInfo, name: str, address: str) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop: Shop = await self.shop_repo.create_shop(
                transaction, user_info.id, name, address
            )
            await transaction.commit()

        return shop

    async def get_shops(self) -> List[Shop]:
        async with self.transaction_manager.get_transaction() as transaction:
            shops = await self.shop_repo.get_all_shops(transaction)
        return shops

    async def get_shop(self, shop_id: str) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await self.shop_repo.get_shop(transaction, shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")
        return shop

    async def update_shop(
        self,
        user_info: UserInfo,
        shop_id: str,
        name: Optional[str],
        address: Optional[str],
    ) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await self.shop_repo.get_shop(transaction, shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user_info.id:
                raise ForbiddenException("You are not allowed to update this shop")

            updated_shop = await self.shop_repo.update_shop(
                transaction,
                shop_id,
                name,
                address,
            )
            await transaction.commit()
        return updated_shop

    async def delete_shop(self, user_info: UserInfo, shop_id: str) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await self.shop_repo.get_shop(transaction, shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user_info.id:
                raise ForbiddenException("You are not allowed to delete this shop")

            await self.shop_repo.delete_shop(transaction, shop_id)
            await transaction.commit()
        return shop

    async def change_owner(
        self, user_info: UserInfo, shop_id: str, new_owner_id: str
    ) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await self.shop_repo.get_shop(transaction, shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user_info.id:
                raise ForbiddenException(
                    "You are not allowed to change owner of this shop"
                )

            new_owner = await self.user_repo.find_by_id(transaction, new_owner_id)
            if new_owner is None:
                raise BadRequestException("New owner not found")

            await self.shop_repo.change_owner(transaction, shop_id, new_owner_id)
            await transaction.commit()

        return Shop(
            id=shop.id, name=shop.name, address=shop.address, owner_id=new_owner_id
        )
