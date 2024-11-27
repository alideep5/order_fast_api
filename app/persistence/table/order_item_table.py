from sqlalchemy import String, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class OrderItemTable(Base):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("orders.id"), primary_key=True, index=True
    )
    product_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("products.id"), primary_key=True, index=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
