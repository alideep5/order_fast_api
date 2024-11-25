from . import Base
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
