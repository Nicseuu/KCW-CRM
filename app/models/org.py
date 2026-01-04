from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, TIMESTAMP, func
from app.models.base import Base


class Org(Base):
    __tablename__ = "org"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
