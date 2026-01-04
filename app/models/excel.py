from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, ForeignKey, TIMESTAMP, func
from app.models.base import Base


class InventoryFileSource(Base):
    __tablename__ = "inventory_file_source"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)

    source_type: Mapped[str] = mapped_column(Text, nullable=False)  # MANUAL_UPLOAD/GOOGLE_DRIVE/ONEDRIVE/S3_COMPAT
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    config: Mapped[dict] = mapped_column(default=dict)

    is_enabled: Mapped[bool] = mapped_column(default=True)
    poll_minutes: Mapped[int | None] = mapped_column(default=None)
    last_poll_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))

    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ExcelInventoryFile(Base):
    __tablename__ = "excel_inventory_file"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    org_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("org.id", ondelete="CASCADE"), index=True)

    source_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("inventory_file_source.id", ondelete="SET NULL"))
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(Text, nullable=False)

    remote_file_id: Mapped[str | None] = mapped_column(Text)
    remote_modified_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))

    status: Mapped[str] = mapped_column(Text, default="UPLOADED", nullable=False)  # UPLOADED/PROCESSED/FAILED
    error: Mapped[str | None] = mapped_column(Text)

    uploaded_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    processed_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True))


class ExcelInventoryRow(Base):
    __tablename__ = "excel_inventory_row"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    excel_file_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("excel_inventory_file.id", ondelete="CASCADE"), index=True)

    sku: Mapped[str] = mapped_column(Text, nullable=False)
    product_name: Mapped[str | None] = mapped_column(Text)
    total_stock: Mapped[int | None] = mapped_column(BigInteger)
    raw: Mapped[dict] = mapped_column(default=dict)
