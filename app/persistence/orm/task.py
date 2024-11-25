import uuid
from . import Base
from sqlalchemy import Column, String, ForeignKey


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    task = Column(String(256), nullable=False)
