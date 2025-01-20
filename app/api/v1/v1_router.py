from fastapi import APIRouter
from app.api.v1.controller.file_controller import FileController
from app.api.v1.controller.product_controller import ProductController
from app.api.v1.controller.user_controller import UserController
from app.api.v1.controller.shop_controller import ShopController
from app.common.model.error_response import ErrorResponse


class V1Router(APIRouter):
    def __init__(
        self,
        user_controller: UserController,
        shop_controller: ShopController,
        product_controller: ProductController,
        file_controller: FileController,
        prefix: str = "/v1",
    ):
        super().__init__(prefix=prefix)

        self.responses = {
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": ErrorResponse(error="error message")
                    }
                },
            },
            "401": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "example": ErrorResponse(error="error message")
                    }
                },
            },
            "403": {
                "description": "Forbidden",
                "content": {
                    "application/json": {
                        "example": ErrorResponse(error="error message")
                    }
                },
            },
            "404": {
                "description": "Not Found",
                "content": {
                    "application/json": {
                        "example": ErrorResponse(error="error message")
                    }
                },
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "example": ErrorResponse(error="error message")
                    }
                },
            },
            "422": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "example": ErrorResponse(error="error message")
                    }
                },
            },
        }

        self.include_router(user_controller)
        self.include_router(shop_controller)
        self.include_router(product_controller)
        self.include_router(file_controller)
