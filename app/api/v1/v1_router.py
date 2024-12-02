from fastapi import APIRouter
from app.api.v1.controller.user_controller import UserController
from app.api.v1.controller.shop_controller import ShopController


class V1Router(APIRouter):
    def __init__(
        self,
        user_controller: UserController,
        shop_controller: ShopController,
        prefix: str = "/v1",
    ):
        super().__init__(prefix=prefix)
        self.include_router(user_controller)
        self.include_router(shop_controller)
