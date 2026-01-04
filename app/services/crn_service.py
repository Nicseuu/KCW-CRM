from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session


def ensure_crn_sequence(db: Session, *, org_id: int) -> None:
    # per-org sequence table (simple)
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS crn_seq (
          org_id BIGINT PRIMARY KEY,
          last_value BIGINT NOT NULL DEFAULT 0
        )
    """))
    db.execute(text("INSERT INTO crn_seq (org_id, last_value) VALUES (:org_id, 0) ON CONFLICT (org_id) DO NOTHING"), {"org_id": org_id})


def next_crn(db: Session, *, org_id: int) -> str:
    ensure_crn_sequence(db, org_id=org_id)
    row = db.execute(
        text("UPDATE crn_seq SET last_value = last_value + 1 WHERE org_id = :org_id RETURNING last_value"),
        {"org_id": org_id},
    ).one()
    seq = int(row[0])
    year = datetime.now(timezone.utc).astimezone().year
    return f"CRN-{year}-{seq:06d}"
