import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class TaskTable(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    task: Mapped[str] = mapped_column(String(256), nullable=False)
