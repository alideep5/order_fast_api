from typing import List
from domain.model.todo_detail import TodoDetail
from persistence.repository.todo_repository import TodoRepository


class TodoService:
    def __init__(self):
        self.todo_repository = TodoRepository()

    def get_all_tasks(self) -> List[TodoDetail]:
        return self.todo_repository.get_all_tasks()
