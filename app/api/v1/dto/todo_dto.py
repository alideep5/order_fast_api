from pydantic import BaseModel
from app.domain.model.todo_detail import TodoDetail as ServiceTodoDetail


class TodoDTO(BaseModel):
    task_id: str
    task: str
