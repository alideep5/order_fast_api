from typing import List
from app.domain.entity.todo import Todo
from app.persistence.session_manager import SessionManager


class TodoRepo:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager

    def get_all_tasks(self) -> List[Todo]:
        return [
            Todo(task_id="1", task="Buy milk"),
            Todo(task_id="2", task="Buy eggs"),
        ]
