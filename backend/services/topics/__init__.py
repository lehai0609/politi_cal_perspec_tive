import spacy
from fastapi import APIRouter

from backend.shared.models import TopicRequest, TopicResponse

_nlp = None

router = APIRouter()


class TopicDetector:
    """Simple topic detector using spaCy."""

    @staticmethod
    def get_topics(text: str) -> list[str]:
        global _nlp
        if _nlp is None:
            _nlp = spacy.load("en_core_web_sm")

        doc = _nlp(text)
        topics: list[str] = []
        seen: set[str] = set()

        for ent in doc.ents:
            if ent.label_ in {"PERSON", "ORG", "GPE", "LOC"}:
                if ent.text not in seen:
                    topics.append(ent.text)
                    seen.add(ent.text)
        for chunk in doc.noun_chunks:
            if chunk.text not in seen:
                topics.append(chunk.text)
                seen.add(chunk.text)

        return topics[:3]


@router.post("/", response_model=TopicResponse)
def detect_topics(request: TopicRequest) -> TopicResponse:
    topics = TopicDetector.get_topics(request.text)
    return TopicResponse(topics=topics)
