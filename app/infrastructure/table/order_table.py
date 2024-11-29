import uuid
from sqlalchemy import String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from .base import Base


class OrderTable(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    customer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    shop_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("shops.id"), nullable=False, index=True
    )
    date_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    total: Mapped[float] = mapped_column(Float, nullable=False)
