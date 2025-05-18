try:
    import spacy
except ModuleNotFoundError:  # pragma: no cover - spaCy unavailable in some envs
    spacy = None
from fastapi import APIRouter

from backend.shared.models import TopicRequest, TopicResponse

_nlp = None

router = APIRouter()


class TopicDetector:
    """Simple topic detector using spaCy."""

    @staticmethod
    def get_topics(text: str) -> list[str]:
        global _nlp
        if spacy is None:
            tokens = text.split()
            seen: set[str] = set()
            deduped = []
            for t in tokens:
                if t not in seen:
                    deduped.append(t)
                    seen.add(t)
            return deduped[:3]

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
