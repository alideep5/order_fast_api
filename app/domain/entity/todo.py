from dataclasses import dataclass


@dataclass
class Todo:
    task_id: str
    task: str
