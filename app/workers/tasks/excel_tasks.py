from __future__ import annotations

from celery import shared_task
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.excel import ExcelInventoryFile
from app.services.excel_service import import_excel_file

@shared_task(bind=True)
def excel_import_task(self, *, org_id: int, excel_file_id: int, file_bytes_b64: str):
    import base64
    db: Session = SessionLocal()
    try:
        excel_file = db.get(ExcelInventoryFile, excel_file_id)
        if not excel_file or excel_file.org_id != org_id:
            raise ValueError("Excel file not found")

        excel_file.status = "RUNNING"
        db.commit()

        file_bytes = base64.b64decode(file_bytes_b64.encode("utf-8"))
        stats = import_excel_file(db, org_id=org_id, excel_file_id=excel_file_id, file_bytes=file_bytes)

        excel_file.status = "PROCESSED"
        db.commit()
        return stats
    except Exception as e:
        db.rollback()
        excel_file = db.get(ExcelInventoryFile, excel_file_id)
        if excel_file:
            excel_file.status = "FAILED"
            excel_file.error = str(e)
            db.commit()
        raise
    finally:
        db.close()
