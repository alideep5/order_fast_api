from typing import List, Optional, Protocol
from app.domain.entity.product import Product


class IProductRepo(Protocol):
    async def get_product_shop_owner_id(self, product_id: str) -> Optional[str]:
        pass

    async def get_products(
        self,
        shop_id: str,
        search: Optional[str],
        page: int,
        size: int,
    ) -> List[Product]:
        pass

    async def get_product(self, product_id: str) -> Optional[Product]:
        pass

    async def create_product(self, shop_id: str, name: str, price: float) -> Product:
        pass

    async def update_product(
        self,
        product_id: str,
        name: Optional[str],
        price: Optional[float],
    ) -> Product:
        pass

    async def delete_product(self, product_id: str) -> None:
        pass

    async def get_products_by_ids(self, product_ids: List[str]) -> List[Product]:
        pass
