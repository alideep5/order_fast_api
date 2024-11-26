from typing import List
from app.domain.entity.todo import Todo
from app.persistence.repository.todo_repo import TodoRepo


class TodoService:
    def __init__(self, todo_repo: TodoRepo) -> None:
        self.todo_repo = todo_repo

    def get_all_tasks(self) -> List[Todo]:
        return self.todo_repo.get_all_tasks()
