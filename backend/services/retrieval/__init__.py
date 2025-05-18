from fastapi import APIRouter

from backend.shared.models import SearchRequest, SearchResponse

from .aggregator import SearchAggregator

router = APIRouter()


@router.post("/", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    articles = SearchAggregator.search(request.query)
    return SearchResponse(articles=articles)
