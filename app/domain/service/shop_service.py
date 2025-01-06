from typing import List, Optional
from app.common.error.response_exception import BadRequestException, ForbiddenException
from app.common.model.user_info import UserInfo
from app.domain.entity.shop import Shop
from app.domain.unit_of_work.transaction_manager import ITransactionManager


class ShopService:
    def __init__(
        self,
        transaction_manager: ITransactionManager,
    ) -> None:
        self.transaction_manager = transaction_manager

    async def createShop(self, user_info: UserInfo, name: str, address: str) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop: Shop = await transaction.shop_repo.create_shop(
                user_info.id, name, address
            )
            await transaction.commit()

        return shop

    async def get_shops(self) -> List[Shop]:
        async with self.transaction_manager.get_transaction() as transaction:
            shops = await transaction.shop_repo.get_all_shops()
        return shops

    async def get_shop(self, shop_id: str) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await transaction.shop_repo.get_shop(shop_id)
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
            shop = await transaction.shop_repo.get_shop(shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user_info.id:
                raise ForbiddenException("You are not allowed to update this shop")

            updated_shop = await transaction.shop_repo.update_shop(
                shop_id,
                name,
                address,
            )
            await transaction.commit()
        return updated_shop

    async def delete_shop(self, user_info: UserInfo, shop_id: str) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await transaction.shop_repo.get_shop(shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user_info.id:
                raise ForbiddenException("You are not allowed to delete this shop")

            await transaction.shop_repo.delete_shop(shop_id)
            await transaction.commit()
        return shop

    async def change_owner(
        self, user_info: UserInfo, shop_id: str, new_owner_id: str
    ) -> Shop:
        async with self.transaction_manager.get_transaction() as transaction:
            shop = await transaction.shop_repo.get_shop(shop_id)
            if shop is None:
                raise BadRequestException("Shop not found")

            if shop.owner_id != user_info.id:
                raise ForbiddenException(
                    "You are not allowed to change owner of this shop"
                )

            new_owner = await transaction.user_repo.find_by_id(new_owner_id)
            if new_owner is None:
                raise BadRequestException("New owner not found")

            await transaction.shop_repo.change_owner(shop_id, new_owner_id)
            await transaction.commit()

        return Shop(
            id=shop.id, name=shop.name, address=shop.address, owner_id=new_owner_id
        )
