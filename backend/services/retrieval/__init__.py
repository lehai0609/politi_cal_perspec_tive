from fastapi import APIRouter

from backend.shared.models import SearchRequest, SearchResponse

router = APIRouter()


class SearchAggregator:
    """Placeholder search aggregator."""

    @staticmethod
    def search(query: str) -> list[str]:
        return [query, f"{query} result"]


@router.post("/", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    results = SearchAggregator.search(request.query)
    return SearchResponse(results=results)
