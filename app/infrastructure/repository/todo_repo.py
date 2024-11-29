from typing import List
from app.domain.entity.todo import Todo


class TodoRepo:
    def get_all_tasks(self) -> List[Todo]:
        return [
            Todo(task_id="1", task="Buy milk"),
            Todo(task_id="2", task="Buy eggs"),
        ]
