from fastapi import APIRouter
from app.api.v1.controller.user_controller import UserController
from app.api.v1.controller.todo_controller import TodoRouterController


class V1Router(APIRouter):
    def __init__(self, prefix: str = "/v1"):
        super().__init__(prefix=prefix)
        self.include_router(UserController())
        self.include_router(TodoRouterController())
