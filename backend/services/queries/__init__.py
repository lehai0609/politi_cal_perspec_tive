from fastapi import APIRouter

from backend.shared.models import QueryRequest, QueryResponse

router = APIRouter()


class QueryGenerator:
    """Simple query generator."""

    @staticmethod
    def build_queries(topics: list[str]) -> list[str]:
        """Return naive search queries based on topics."""
        if not topics:
            return []
        queries = [f'"{t}"' for t in topics]
        if len(topics) > 1:
            combined = " AND ".join(f'"{t}"' for t in topics)
            queries.append(combined)
        return queries


@router.post("/", response_model=QueryResponse)
def generate(request: QueryRequest) -> QueryResponse:
    queries = QueryGenerator.build_queries(request.topics)
    return QueryResponse(queries=queries)
