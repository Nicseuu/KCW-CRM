from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, Boolean, ForeignKey, UniqueConstraint, TIMESTAMP, func
from app.models.base import Base


class PlatformAccount(Base):
    __tablename__ = "platform_account"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)

    platform: Mapped[str] = mapped_column(Text, nullable=False)  # SHOPEE/LAZADA/TIKTOK
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    merchant_id: Mapped[str | None] = mapped_column(Text)

    access_token: Mapped[str | None] = mapped_column(Text)
    refresh_token: Mapped[str | None] = mapped_column(Text)
    token_expires_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))

    settings: Mapped[dict] = mapped_column(default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("org_id", "platform", "merchant_id", name="uq_platform_account"),
    )
