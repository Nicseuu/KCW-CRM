from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, ForeignKey, UniqueConstraint, TIMESTAMP, func
from app.models.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product.id", ondelete="CASCADE"), index=True)

    total_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    available_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("org_id", "product_id", name="uq_inventory_org_product"),
    )
