from __future__ import annotations

import base64

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.excel import ExcelInventoryFile
from app.services.excel_service import create_excel_file_record
from app.workers.tasks.excel_tasks import excel_import_task

router = APIRouter()

# MVP shortcut: single org
MVP_ORG_ID = 1

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    excel_file = create_excel_file_record(db, org_id=MVP_ORG_ID, filename=file.filename, file_bytes=content)
    db.commit()

    # Option: auto-import immediately
    b64 = base64.b64encode(content).decode("utf-8")
    excel_import_task.delay(org_id=MVP_ORG_ID, excel_file_id=excel_file.id, file_bytes_b64=b64)

    return {"excel_file_id": excel_file.id, "status": "UPLOADED_AND_IMPORT_QUEUED"}

@router.get("/files")
def list_files(db: Session = Depends(get_db)):
    files = db.query(ExcelInventoryFile).filter(ExcelInventoryFile.org_id == MVP_ORG_ID).order_by(ExcelInventoryFile.uploaded_at.desc()).limit(50).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "status": f.status,
            "error": f.error,
            "uploaded_at": f.uploaded_at,
            "processed_at": f.processed_at,
        }
        for f in files
    ]
