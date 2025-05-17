from fastapi import APIRouter

from backend.shared.models import DedupRequest, DedupResponse

router = APIRouter()


class Deduplicator:
    """Placeholder deduplicator."""

    @staticmethod
    def group_by_simhash(items: list[str]) -> list[list[str]]:
        groups: list[list[str]] = []
        for item in items:
            for group in groups:
                if group[0] == item:
                    group.append(item)
                    break
            else:
                groups.append([item])
        return groups


@router.post("/", response_model=DedupResponse)
def group(request: DedupRequest) -> DedupResponse:
    groups = Deduplicator.group_by_simhash(request.items)
    return DedupResponse(groups=groups)
