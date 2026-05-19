from fastapi import FastAPI

from backend.app.api.documents import router as documents_router

app = FastAPI(
    title="LandLease AI API",
    description="Backend API for LandLease AI. Handles authentication, PDF/document processing, lease and well data, and more.",
    version="0.1.0"
)

app.include_router(documents_router)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "LandLease AI", "phase": 1}
