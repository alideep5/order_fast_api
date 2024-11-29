import uuid
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class ProductTable(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    shop_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("shops.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
