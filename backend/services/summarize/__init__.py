from __future__ import annotations

import re

from fastapi import APIRouter

from backend.shared.models import SummarizeRequest, SummarizeResponse

router = APIRouter()


class Summarizer:
    """Very naive text summarizer using sentence splitting."""

    @staticmethod
    def summarize(text: str, max_sentences: int = 3) -> str:
        sentences = re.findall(r"[^.!?]+[.!?]", text)
        summary = " ".join(s.strip() for s in sentences[:max_sentences])
        return summary.strip()


@router.post("/", response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest) -> SummarizeResponse:
    summary = Summarizer.summarize(request.text, request.max_sentences)
    return SummarizeResponse(summary=summary)
