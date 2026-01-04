from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, ForeignKey, UniqueConstraint, TIMESTAMP
from app.models.base import Base


class OrderItemReservation(Base):
    __tablename__ = "order_item_reservation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)

    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("order.id", ondelete="CASCADE"), index=True)
    order_item_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("order_item.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product.id", ondelete="CASCADE"), index=True)

    qty: Mapped[int] = mapped_column(Integer, nullable=False)

    reserved_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))
    released_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))

    reserve_event: Mapped[str | None] = mapped_column(default=None)
    release_event: Mapped[str | None] = mapped_column(default=None)

    __table_args__ = (
        UniqueConstraint("org_id", "order_item_id", name="uq_reservation_org_order_item"),
    )
