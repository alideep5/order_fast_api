from fastapi import APIRouter
from typing import List
from app.api.v1.dto.todo_dto import TodoDTO
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
        todo_list: List[Todo] = self.todo_service.get_all_tasks()
        return [TodoDTO(task_id=todo.task_id, task=todo.task) for todo in todo_list]
