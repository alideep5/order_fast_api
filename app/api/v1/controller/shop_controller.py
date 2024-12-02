from fastapi import APIRouter, Body, Depends, Path
from typing import List
from app.api.dto.change_shop_owner_request import ChangeShopOwnerRequest
from app.api.dto.create_shop_request import CreateShopRequest
from app.api.dto.shop_dto import ShopDTO
from app.api.dto.shop_list_dto import ShopListDTO
from app.api.dto.update_shop_request import UpdateShopRequest
from app.common.model.user_info import UserInfo
from app.common.util.dto_util import DTOUtil
from app.common.util.request_util import RequestUtil
from app.domain.service.shop_service import ShopService


class ShopController(APIRouter):
    def __init__(self, shop_service: ShopService, prefix: str = "/shops"):
        super().__init__(prefix=prefix, tags=["Shop"])
        self.shop_service = shop_service

        self.add_api_route(
            path="/",
            methods=["GET"],
            endpoint=self.get_shops,
            summary="Get shops",
            description="Endpoint to get the list of shops.",
            response_model=ShopListDTO,
        )
        self.add_api_route(
            path="/",
            methods=["POST"],
            endpoint=self.create_shop,
            summary="Create shop",
            description="Endpoint to create a shop.",
            response_model=ShopDTO,
        )
        self.add_api_route(
            path="/{shop_id}",
            methods=["GET"],
            endpoint=self.get_shop_by_id,
            summary="Get shop by ID",
            description="Endpoint to get a shop by its ID.",
            response_model=ShopDTO,
        )
        self.add_api_route(
            path="/{shop_id}",
            methods=["PUT"],
            endpoint=self.update_shop,
            summary="Update shop by ID",
            description="Endpoint to update a shop by its ID.",
            response_model=ShopDTO,
        )
        self.add_api_route(
            path="/{shop_id}",
            methods=["DELETE"],
            endpoint=self.delete_shop,
            summary="Delete shop by ID",
            description="Endpoint to delete a shop by its ID.",
            response_model=ShopDTO,
        )
        self.add_api_route(
            path="/{shop_id}/change-owner",
            methods=["PATCH"],
            endpoint=self.change_owner,
            summary="Change owner of shop",
            description="Endpoint to change the owner of a shop.",
            response_model=ShopDTO,
        )

    async def get_shops(
        self, user: UserInfo = Depends(RequestUtil.get_auth_user)
    ) -> ShopListDTO:
        shops = await self.shop_service.get_shops()
        return ShopListDTO(shops=DTOUtil.convert_to_dto_list(shops, ShopDTO))

    async def create_shop(
        self,
        create_shop: CreateShopRequest = Body(...),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ShopDTO:
        shop = await self.shop_service.createShop(
            user_info=user, name=create_shop.name, address=create_shop.address
        )
        return DTOUtil.convert_to_dto(shop, ShopDTO)

    async def get_shop_by_id(
        self,
        shop_id: str = Path(..., description="The ID of the shop."),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ShopDTO:
        shop = await self.shop_service.get_shop(shop_id)
        return DTOUtil.convert_to_dto(shop, ShopDTO)

    async def update_shop(
        self,
        shop_id: str = Path(..., description="The ID of the shop."),
        update_shop_request: UpdateShopRequest = Body(...),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ShopDTO:
        shop = await self.shop_service.update_shop(
            user_info=user,
            shop_id=shop_id,
            name=update_shop_request.name,
            address=update_shop_request.address,
        )
        return DTOUtil.convert_to_dto(shop, ShopDTO)

    async def delete_shop(
        self,
        shop_id: str = Path(..., description="The ID of the shop."),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ShopDTO:
        shop = await self.shop_service.delete_shop(user_info=user, shop_id=str(shop_id))
        return DTOUtil.convert_to_dto(shop, ShopDTO)

    async def change_owner(
        self,
        shop_id: str = Path(..., description="The ID of the shop."),
        change_shop_owner_request: ChangeShopOwnerRequest = Body(...),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ShopDTO:
        shop = await self.shop_service.change_owner(
            user_info=user,
            shop_id=str(shop_id),
            new_owner_id=str(change_shop_owner_request.new_owner_id),
        )
        return DTOUtil.convert_to_dto(shop, ShopDTO)
