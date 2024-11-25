from persistence.orm import Base
from sqlalchemy import Column, String, ForeignKey


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    task = Column(String(256), nullable=False)
