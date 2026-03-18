from fastapi import APIRouter

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.get("/health")
def health():
    return {"ok": True, "service": "ingest"}