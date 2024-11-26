from pydantic import BaseModel


class TodoDetail(BaseModel):
    task_id: str
    task: str
