from fastapi import APIRouter

from backend.shared.models import DedupGroup, DedupRequest, DedupResponse
from backend.shared.simhash import hamming_distance, simhash

router = APIRouter()


class Deduplicator:
    """Simhash-based deduplicator."""

    @staticmethod
    def group_by_simhash(items: list[str], threshold: int = 3) -> list[DedupGroup]:
        """Group near-duplicate strings using simhash."""
        groups: list[dict] = []
        for item in items:
            item_hash = simhash(item)
            placed = False
            for group in groups:
                if hamming_distance(group["hash"], item_hash) <= threshold:
                    group["duplicates"].append(item)
                    placed = True
                    break
            if not placed:
                groups.append(
                    {"hash": item_hash, "representative": item, "duplicates": []}
                )

        return [
            DedupGroup(representative=g["representative"], duplicates=g["duplicates"])
            for g in groups
        ]


@router.post("/", response_model=DedupResponse)
def group(request: DedupRequest) -> DedupResponse:
    groups = Deduplicator.group_by_simhash(request.items)
    return DedupResponse(groups=[[g.representative, *g.duplicates] for g in groups])
