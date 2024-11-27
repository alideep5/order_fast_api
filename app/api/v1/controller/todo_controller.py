from fastapi import APIRouter
from typing import List
from app.api.dto.todo_dto import TodoDTO
from app.api.utils.dto_util import DTOUtil
from app.domain.entity.todo import Todo
from app.domain.service.todo_service import TodoService


class TodoController(APIRouter):
    def __init__(self, todo_service: TodoService, prefix: str = "/todo"):
        self.todo_service = todo_service
        super().__init__(prefix=prefix)

        self.tags = ["Todo"]
        self.description = "Operations related to Todo"

        self.add_api_route(
            path="/tasks",
            methods=["GET"],
            endpoint=self.get_todo,
            summary="Get Todo tasks",
            description="Retrieve list if todo task",
        )

    async def get_todo(self) -> List[TodoDTO]:
        return DTOUtil.convert_to_dto_list(self.todo_service.get_all_tasks(), TodoDTO)
