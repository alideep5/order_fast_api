from sqlalchemy.orm import DeclarativeBase
from .task_table import TaskTable
from .user_table import UserTable


class Base(DeclarativeBase):
    pass


__all__ = ["Base", "TaskTable", "UserTable"]
