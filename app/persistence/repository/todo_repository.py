from typing import List
from domain.model.todo_detail import TodoDetail
from persistence.db_session_manager import DbSessionManager


class TodoRepository:
    def __init__(self):
        self.db_session = DbSessionManager()

    def get_all_tasks(self) -> List[TodoDetail]:
        return [
            TodoDetail(task_id="1", task="Buy milk"),
            TodoDetail(task_id="2", task="Buy eggs"),
        ]
