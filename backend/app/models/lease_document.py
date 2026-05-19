from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, func
from backend.app.db.database import Base

class LeaseDocumentStatus:
    UPLOADED = "uploaded"
    TEXT_EXTRACTION_PENDING = "text_extraction_pending"
    TEXT_EXTRACTION_COMPLETE = "text_extraction_complete"
    FIELD_EXTRACTION_PENDING = "field_extraction_pending"
    FIELD_EXTRACTION_COMPLETE = "field_extraction_complete"
    NEEDS_REVIEW = "needs_review"
    FAILED = "failed"

class LeaseDocument(Base):
    __tablename__ = "lease_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True, nullable=False)  # Supabase UID
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default=LeaseDocumentStatus.UPLOADED)
    raw_text = Column(Text, nullable=True)
    extraction_method = Column(String(64), nullable=True)
    extraction_error = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)