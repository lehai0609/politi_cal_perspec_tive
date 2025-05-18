from __future__ import annotations

from fastapi import APIRouter

from backend.shared.models import BiasRequest, BiasResponse

router = APIRouter()


class BiasAnnotator:
    """Simple bias annotator using a predefined source map."""

    _BIAS_MAP = {
        "Fox News": ("Right", 10),
        "MSNBC": ("Left", 10),
        "AP": ("Center", 5),
    }

    @classmethod
    def annotate(cls, source: str) -> BiasResponse:
        bias, score = cls._BIAS_MAP.get(source, ("Center", 0))
        return BiasResponse(bias=bias, bias_score=score)


@router.post("/", response_model=BiasResponse)
def bias_endpoint(request: BiasRequest) -> BiasResponse:
    return BiasAnnotator.annotate(request.source)
