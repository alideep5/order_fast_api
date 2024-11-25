from . import Base
import uuid
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
