from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Request
from backend.app.db.database import SessionLocal
from backend.app.models.lease_document import LeaseDocument, LeaseDocumentStatus
from backend.app.utils.auth import get_current_user
from sqlalchemy.orm import Session
import os
import shutil
from typing import List

router = APIRouter(prefix="/documents", tags=["documents"])

# Dependency: SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

MAX_FILE_SIZE_MB = 20
UPLOAD_FOLDER = os.environ.get("LEASE_DOC_UPLOAD_PATH", "backend/data/lease_pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload", status_code=201)
def upload_document(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Basic validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    contents = file.file.read()
    size_mb = len(contents) / (1024*1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=413, detail="Max file size is 20 MB")
    # Save file
    subdir = os.path.join(UPLOAD_FOLDER, user["id"])
    os.makedirs(subdir, exist_ok=True)
    file_path = os.path.join(subdir, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    # Create LeaseDocument record
    doc = LeaseDocument(
        user_id=user["id"],
        file_name=file.filename,
        file_path=file_path,
        file_size=len(contents),
        mime_type=file.content_type,
        status=LeaseDocumentStatus.UPLOADED,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {
        "document_id": doc.id,
        "file_name": doc.file_name,
        "status": doc.status,
    }