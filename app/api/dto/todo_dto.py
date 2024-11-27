from pydantic import BaseModel
from app.domain.entity.todo import Todo as ServiceTodoDetail


class TodoDTO(BaseModel):
    task_id: str
    task: str
