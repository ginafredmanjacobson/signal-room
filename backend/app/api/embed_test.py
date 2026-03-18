from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding_service import embed_text


router = APIRouter(prefix="/embed", tags=["embed"])


class EmbedRequest(BaseModel):
    text: str

@router.post("")
def embed(payload: EmbedRequest):
    vec = embed_text(payload.text)
    return {"dim": len(vec), "vector_preview": vec[:8]}