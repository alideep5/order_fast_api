from fastapi import APIRouter
from app.api.v1.controller.user_controller import UserController
from app.api.v1.controller.todo_controller import TodoController


class V1Router(APIRouter):
    def __init__(
        self,
        user_controller: UserController,
        todo_controller: TodoController,
        prefix: str = "/v1",
    ):
        super().__init__(prefix=prefix)
        self.include_router(user_controller)
        self.include_router(todo_controller)
