from typing import List, Optional, Protocol
from app.domain.entity.shop import Shop


class IShopRepo(Protocol):
    async def create_shop(self, owner_id: str, name: str, address: str) -> Shop:
        pass

    async def get_all_shops(self) -> List[Shop]:
        pass

    async def get_shop(self, shop_id: str) -> Optional[Shop]:
        pass

    async def update_shop(
        self,
        shop_id: str,
        name: Optional[str],
        address: Optional[str],
    ) -> Shop:
        pass

    async def delete_shop(self, shop_id: str) -> None:
        pass

    async def change_owner(self, shop_id: str, new_owner_id: str) -> None:
        pass
