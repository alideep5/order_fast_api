from typing import List
from app.domain.entity.todo import Todo
from app.domain.unit_of_work.transaction_manager import ITransactionManager
from app.persistence.repository.todo_repo import TodoRepo


class TodoService:
    def __init__(self, unit_of_work: ITransactionManager, todo_repo: TodoRepo) -> None:
        self.unit_of_work = unit_of_work
        self.todo_repo = todo_repo

    def get_all_tasks(self) -> List[Todo]:
        return self.todo_repo.get_all_tasks()
