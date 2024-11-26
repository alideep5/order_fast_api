from fastapi import APIRouter
from typing import List
from app.api.v1.dto.todo_dto import TodoDTO
from app.domain.service.todo_service import TodoService
from app.utils.schema_util import SchemaUtil


class TodoRouterController(APIRouter):
    def __init__(self, prefix: str = "/todo"):
        super().__init__(prefix=prefix)
        self.tags = ["Todo"]
        self.description = "Operations related to Todo"
        self.todo_service = TodoService()
        self.add_api_route(
            path="/tasks",
            methods=["GET"],
            endpoint=self.get_todo,
            summary="Get Todo tasks",
            description="Retrieve list if todo task",
        )

    async def get_todo(self) -> List[TodoDTO]:
        return SchemaUtil.convert_list_to_schema(
            self.todo_service.get_all_tasks(), TodoDTO
        )
