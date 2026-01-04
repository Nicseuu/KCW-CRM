from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class InventoryFileSource(Base):
    """
    Tracks where inventory files come from (manual upload, shared drive polling, etc.).
    """
    __tablename__ = "inventory_file_source"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # e.g. "manual_upload", "shared_drive_poll"
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # JSON config for source behavior (path, schedule, credentials ref, etc.)
    # IMPORTANT: Must be a JSON/JSONB column, not just Mapped[dict] alone.
    config: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    files: Mapped[list["ExcelInventoryFile"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
    )


class ExcelInventoryFile(Base):
    """
    Represents a particular Excel inventory file import/upload record.
    """
    __tablename__ = "excel_inventory_file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    source_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("inventory_file_source.id", ondelete="SET NULL"),
        nullable=True,
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    source: Mapped[InventoryFileSource | None] = relationship(back_populates="files")
