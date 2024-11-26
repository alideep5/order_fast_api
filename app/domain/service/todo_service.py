from typing import List
from app.domain.entity.todo import Todo
from app.persistence.repository.todo_repository import TodoRepository


class TodoService:
    def __init__(self) -> None:
        self.todo_repository = TodoRepository()

    def get_all_tasks(self) -> List[Todo]:
        return self.todo_repository.get_all_tasks()
