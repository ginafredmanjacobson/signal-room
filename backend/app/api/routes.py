from fastapi import APIRouter
from app.api import ingest, clusters

router = APIRouter()
router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
router.include_router(clusters.router, prefix="/clusters", tags=["clusters"])