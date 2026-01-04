from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, ForeignKey, TIMESTAMP, func
from app.models.base import Base


class SyncRun(Base):
    __tablename__ = "sync_run"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)

    platform: Mapped[str | None] = mapped_column(Text)  # optional
    platform_account_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("platform_account.id", ondelete="SET NULL"))

    job_type: Mapped[str] = mapped_column(Text, nullable=False)  # PULL_ORDERS / PUSH_STOCK / EXCEL_IMPORT / PULL_EXCEL_FROM_SOURCE
    status: Mapped[str] = mapped_column(Text, default="QUEUED", nullable=False)  # QUEUED/RUNNING/SUCCESS/FAILED/PARTIAL

    started_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))
    finished_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))

    error: Mapped[str | None] = mapped_column(Text)
    stats: Mapped[dict] = mapped_column(default=dict)

    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
