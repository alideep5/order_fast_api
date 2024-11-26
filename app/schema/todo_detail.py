from pydantic import BaseModel
from app.domain.model.todo_detail import TodoDetail as ServiceTodoDetail


class TodoDetail(BaseModel):
    task_id: str
    task: str
