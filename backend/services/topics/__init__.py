from fastapi import APIRouter

from backend.shared.models import TopicRequest, TopicResponse

router = APIRouter()


class TopicDetector:
    """Placeholder topic detector."""

    @staticmethod
    def get_topics(text: str) -> list[str]:
        words = text.split()
        return list(dict.fromkeys(words))[:3]


@router.post("/", response_model=TopicResponse)
def detect_topics(request: TopicRequest) -> TopicResponse:
    topics = TopicDetector.get_topics(request.text)
    return TopicResponse(topics=topics)
