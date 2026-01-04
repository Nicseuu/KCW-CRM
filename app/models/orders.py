from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, ForeignKey, UniqueConstraint, TIMESTAMP, func, Numeric
from app.models.base import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)

    platform: Mapped[str] = mapped_column(Text, nullable=False)  # SHOPEE/LAZADA/TIKTOK
    platform_account_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("platform_account.id", ondelete="CASCADE"))
    platform_order_id: Mapped[str] = mapped_column(Text, nullable=False)

    customer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("customer.id", ondelete="SET NULL"))

    status: Mapped[str] = mapped_column(Text, nullable=False)  # PENDING/CONFIRMED/...
    currency: Mapped[str] = mapped_column(Text, default="PHP", nullable=False)

    total_amount: Mapped[object] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    order_created_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))
    imported_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    raw: Mapped[dict] = mapped_column(default=dict)

    __table_args__ = (
        UniqueConstraint("org_id", "platform_account_id", "platform_order_id", name="uq_order_platform_id"),
    )


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("order.id", ondelete="CASCADE"), index=True)

    product_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("product.id", ondelete="SET NULL"))
    platform_sku: Mapped[str | None] = mapped_column(Text)

    name: Mapped[str | None] = mapped_column(Text)
    quantity: Mapped[int] = mapped_column(BigInteger, nullable=False)

    raw: Mapped[dict] = mapped_column(default=dict)
