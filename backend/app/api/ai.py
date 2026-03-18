from fastapi import APIRouter

from app.schemas.ai import SummarizeRequest, SummarizeResponse
from app.services.ai_service import summarize_text

router = APIRouter(tags=["ai"])

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    return summarize_text(payload.text)
