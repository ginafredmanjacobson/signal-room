from fastapi import APIRouter
from app.api.ai import router as ai_router
from app.api.ingest import router as ingest_router
#from app.api.embed_test import router as embed_router

router = APIRouter()

router.include_router(ai_router, prefix="/ai")
router.include_router(ingest_router, prefix="/ingest")
#router.include_router(embed_router)
