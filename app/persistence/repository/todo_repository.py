from typing import List
from app.domain.model.todo_detail import TodoDetail
from app.persistence.session_manager import SessionManager


class TodoRepository:
    def __init__(self) -> None:
        self.db_session = SessionManager()

    def get_all_tasks(self) -> List[TodoDetail]:
        return [
            TodoDetail(task_id="1", task="Buy milk"),
            TodoDetail(task_id="2", task="Buy eggs"),
        ]
