from dependency_injector import containers, providers
from app.api.v1.controller.todo_controller import TodoController
from app.api.v1.controller.user_controller import UserController
from app.api.v1.v1_router import V1Router
from app.common.model.app_config import AppConfig
from app.configuration.global_exception_handler import GlobalExceptionHandler
from app.configuration.jwt_middleware import JWTMiddleware
from app.configuration.app_logger import AppLogger
from app.domain.service.todo_service import TodoService
from app.domain.service.user_service import UserService
from app.common.util.jwt_util import JWTUtil
from app.infrastructure.repository.todo_repo import TodoRepo
from app.infrastructure.repository.user_repo import UserRepo
from app.infrastructure.unit_of_work.transaction_manager import TransactionManager


class AppContainer(containers.DeclarativeContainer):
    app_config = providers.Singleton(AppConfig)

    app_logger = providers.Singleton(AppLogger)

    jwt_util = providers.Singleton(JWTUtil, app_config=app_config)

    jwt_middleware = providers.Singleton(JWTMiddleware, jwt_util=jwt_util)

    exception_handler = providers.Singleton(GlobalExceptionHandler, log=app_logger)

    unit_of_work = providers.Singleton(TransactionManager, app_config=app_config)

    user_repo = providers.Singleton(UserRepo)
    todo_repo = providers.Singleton(TodoRepo)

    user_service = providers.Singleton(
        UserService,
        transaction_manager=unit_of_work,
        jwt_util=jwt_util,
        user_repo=user_repo,
    )
    todo_service = providers.Singleton(
        TodoService, transaction_manager=unit_of_work, todo_repo=todo_repo
    )

    user_controller = providers.Singleton(UserController, user_service=user_service)
    todo_controller = providers.Singleton(TodoController, todo_service=todo_service)

    v1_router = providers.Singleton(
        V1Router, user_controller=user_controller, todo_controller=todo_controller
    )
