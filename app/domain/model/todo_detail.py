from dataclasses import dataclass


@dataclass
class TodoDetail:
    task_id: str
    task: str
