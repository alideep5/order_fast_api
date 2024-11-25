from typing import List
from domain.model.todo_detail import TodoDetail


class TodoRepository:
    def __init__(self):
        self.db = "db"

    def get_all_tasks(self) -> List[TodoDetail]:
        return [
            TodoDetail(task_id="1", task="Buy milk"),
            TodoDetail(task_id="2", task="Buy eggs"),
        ]
