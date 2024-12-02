from typing import Optional
from fastapi import APIRouter, Body, Depends, Path, Query
from app.api.dto.create_product_dto import CreateProductDTO
from app.api.dto.product_dto import ProductDTO
from app.api.dto.product_list_dto import ProductListDTO
from app.api.dto.update_product_dto import UpdateProductDTO
from app.common.model.user_info import UserInfo
from app.common.util.dto_util import DTOUtil
from app.common.util.request_util import RequestUtil
from app.domain.service.product_service import ProductService


class ProductController(APIRouter):
    def __init__(self, product_service: ProductService, prefix: str = "/products"):
        super().__init__(prefix=prefix, tags=["Product"])
        self.product_service = product_service

        self.add_api_route(
            path="/shops/{shop_id}/products",
            methods=["GET"],
            endpoint=self.get_products,
            summary="Get products",
            description="Endpoint to get list of products for a given shop.",
        )
        self.add_api_route(
            path="/{product_id}",
            methods=["GET"],
            endpoint=self.get_product,
            summary="Get product by ID",
            description="Endpoint to get a product by its ID.",
        )
        self.add_api_route(
            path="/shops/{shop_id}/products",
            methods=["POST"],
            status_code=201,
            endpoint=self.create_product,
            summary="Create product",
            description="Endpoint to create a new product for a given shop.",
        )
        self.add_api_route(
            path="/{product_id}",
            methods=["PUT"],
            endpoint=self.update_product,
            summary="Update product",
            description="Endpoint to update an existing product.",
        )
        self.add_api_route(
            path="/{product_id}",
            methods=["DELETE"],
            endpoint=self.delete_product,
            summary="Delete product",
            description="Endpoint to delete an existing product.",
        )

    async def get_products(
        self,
        shop_id: str = Path(..., description="The ID of the shop."),
        page: int = Query(1, ge=1, description="Page number for pagination"),
        size: int = Query(10, ge=1, description="Number of items per page"),
        search: Optional[str] = Query(None, description="Search query"),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ProductListDTO:
        products = await self.product_service.get_products(
            shop_id=shop_id, search=search, page=page, size=size
        )
        return ProductListDTO(
            products=DTOUtil.convert_to_dto_list(products, ProductDTO)
        )

    async def get_product(
        self,
        product_id: str = Path(..., description="The ID of the product."),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ProductDTO:
        product = await self.product_service.get_product(product_id=product_id)
        return DTOUtil.convert_to_dto(product, ProductDTO)

    async def create_product(
        self,
        shop_id: str = Path(..., description="The ID of the shop."),
        create_product_request: CreateProductDTO = Body(...),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ProductDTO:
        product = await self.product_service.create_product(
            user=user,
            shop_id=shop_id,
            name=create_product_request.name,
            price=create_product_request.price,
        )
        return DTOUtil.convert_to_dto(product, ProductDTO)

    async def update_product(
        self,
        product_id: str = Path(..., description="The ID of the product."),
        update_product_request: UpdateProductDTO = Body(...),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ProductDTO:
        product = await self.product_service.update_product(
            user=user,
            product_id=product_id,
            name=update_product_request.name,
            price=update_product_request.price,
        )

        return DTOUtil.convert_to_dto(product, ProductDTO)

    async def delete_product(
        self,
        product_id: str = Path(..., description="The ID of the product."),
        user: UserInfo = Depends(RequestUtil.get_auth_user),
    ) -> ProductDTO:
        product = await self.product_service.delete_product(
            user=user, product_id=product_id
        )
        return DTOUtil.convert_to_dto(product, ProductDTO)
