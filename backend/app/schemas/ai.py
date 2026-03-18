from pydantic import BaseModel, Field
from typing import List


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class SummarizeResponse(BaseModel):
    summary: str
    bullets: List[str]