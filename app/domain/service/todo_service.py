from typing import List
from app.domain.model.todo_detail import TodoDetail
from app.persistence.repository.todo_repository import TodoRepository


class TodoService:
    def __init__(self) -> None:
        self.todo_repository = TodoRepository()

    def get_all_tasks(self) -> List[TodoDetail]:
        return self.todo_repository.get_all_tasks()
