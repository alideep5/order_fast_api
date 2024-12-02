from typing import Any, List, Optional, Protocol
from app.domain.entity.shop import Shop
from app.domain.unit_of_work.transaction import ITransaction


class IShopRepo(Protocol):
    async def create_shop(
        self, transaction: ITransaction[Any], owner_id: str, name: str, address: str
    ) -> Shop:
        pass

    async def get_all_shops(self, transaction: ITransaction[Any]) -> List[Shop]:
        pass

    async def get_shop(
        self, transaction: ITransaction[Any], shop_id: str
    ) -> Optional[Shop]:
        pass

    async def update_shop(
        self,
        transaction: ITransaction[Any],
        shop_id: str,
        name: Optional[str],
        address: Optional[str],
    ) -> Shop:
        pass

    async def delete_shop(self, transaction: ITransaction[Any], shop_id: str) -> None:
        pass

    async def change_owner(
        self, transaction: ITransaction[Any], shop_id: str, new_owner_id: str
    ) -> None:
        pass
