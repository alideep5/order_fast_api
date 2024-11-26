from pydantic import BaseModel
from app.domain.model.todo_detail import TodoDetail as ServiceTodoDetail


class TodoDetail(BaseModel):
    task_id: str
    task: str

    @staticmethod
    def from_service_model(normal_model: ServiceTodoDetail) -> "TodoDetail":
        return TodoDetail(task_id=normal_model.task_id, task=normal_model.task)
