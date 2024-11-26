from dependency_injector import containers, providers
from app.api.v1.controller.todo_controller import TodoController
from app.api.v1.controller.user_controller import UserController
from app.api.v1.v1_router import V1Router
from app.config.app_config import AppConfig
from app.domain.service.todo_service import TodoService
from app.domain.service.user_service import UserService
from app.persistence.repository.todo_repo import TodoRepo
from app.persistence.repository.user_repo import UserRepo
from app.persistence.session_manager import SessionManager


class AppContainer(containers.DeclarativeContainer):
    app_config = providers.Singleton(AppConfig)

    session_manager = providers.Singleton(SessionManager, app_config=app_config)

    user_repo = providers.Singleton(UserRepo, session_manager=session_manager)
    todo_repo = providers.Singleton(TodoRepo, session_manager=session_manager)

    user_service = providers.Singleton(UserService, user_repo=user_repo)
    todo_service = providers.Singleton(TodoService, todo_repo=todo_repo)

    user_controller = providers.Singleton(UserController, user_service=user_service)
    todo_controller = providers.Singleton(TodoController, todo_service=todo_service)

    v1_router = providers.Singleton(
        V1Router, user_controller=user_controller, todo_controller=todo_controller
    )
