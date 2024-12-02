from dependency_injector import containers, providers
from app.api.v1.controller.product_controller import ProductController
from app.api.v1.controller.shop_controller import ShopController
from app.api.v1.controller.user_controller import UserController
from app.api.v1.v1_router import V1Router
from app.common.model.app_config import AppConfig
from app.configuration.global_exception_handler import GlobalExceptionHandler
from app.configuration.jwt_middleware import JWTMiddleware
from app.configuration.app_logger import AppLogger
from app.domain.service.product_service import ProductService
from app.domain.service.shop_service import ShopService
from app.domain.service.user_service import UserService
from app.common.util.jwt_util import JWTUtil
from app.infrastructure.repository.product_repo import ProductRepo
from app.infrastructure.repository.shop_repo import ShopRepo
from app.infrastructure.repository.user_repo import UserRepo
from app.infrastructure.unit_of_work.transaction_manager import TransactionManager


class AppContainer(containers.DeclarativeContainer):
    app_config = providers.Singleton(AppConfig)

    app_logger = providers.Singleton(AppLogger)

    jwt_util = providers.Singleton(JWTUtil, app_config=app_config, log=app_logger)

    jwt_middleware = providers.Singleton(JWTMiddleware, jwt_util=jwt_util)

    exception_handler = providers.Singleton(GlobalExceptionHandler, log=app_logger)

    transaction_manager = providers.Singleton(
        TransactionManager, app_config=app_config, log=app_logger
    )

    user_repo = providers.Singleton(UserRepo)
    shop_repo = providers.Singleton(ShopRepo)
    product_repo = providers.Singleton(ProductRepo)

    user_service = providers.Singleton(
        UserService,
        transaction_manager=transaction_manager,
        jwt_util=jwt_util,
        user_repo=user_repo,
    )
    shop_service = providers.Singleton(
        ShopService,
        transaction_manager=transaction_manager,
        shop_repo=shop_repo,
        user_repo=user_repo,
    )
    product_service = providers.Singleton(
        ProductService,
        transaction_manager=transaction_manager,
        product_repo=product_repo,
        shop_repo=shop_repo,
    )

    user_controller = providers.Singleton(UserController, user_service=user_service)
    shop_controller = providers.Singleton(ShopController, shop_service=shop_service)
    product_controller = providers.Singleton(
        ProductController, product_service=product_service
    )

    v1_router = providers.Singleton(
        V1Router,
        user_controller=user_controller,
        shop_controller=shop_controller,
        product_controller=product_controller,
    )
