from __future__ import annotations

from fastapi import APIRouter

from backend.services.extract import ArticleExtractor
from backend.services.topics import TopicDetector
from backend.services.queries import QueryGenerator
from backend.services.retrieval.aggregator import SearchAggregator
from backend.services.dedup import Deduplicator
from backend.services.summarize import Summarizer
from backend.services.bias import BiasAnnotator
from backend.shared.models import (
    PerspectiveRequest,
    PerspectiveResponse,
)

router = APIRouter()


class PerspectivePipeline:
    """Runs the full perspectives pipeline."""

    @staticmethod
    def run(url: str | None, html: str | None, force: bool = False) -> PerspectiveResponse:
        extract = ArticleExtractor.extract(url, html, force)
        topics = TopicDetector.get_topics(extract.clean_text)
        queries = QueryGenerator.build_queries(topics)
        articles = []
        for q in queries:
            articles.extend(SearchAggregator.search(q))
        titles = [a.title for a in articles]
        groups_models = Deduplicator.group_by_simhash(titles)
        groups = [[g.representative, *g.duplicates] for g in groups_models]
        summary = Summarizer.summarize(extract.clean_text, 3)
        bias = BiasAnnotator.annotate(url or "")
        return PerspectiveResponse(
            topics=topics,
            queries=queries,
            articles=articles,
            groups=groups,
            summary=summary,
            bias=bias.bias,
            bias_score=bias.bias_score,
        )


@router.post("/", response_model=PerspectiveResponse)
def generate_perspective(request: PerspectiveRequest) -> PerspectiveResponse:
    return PerspectivePipeline.run(request.url, request.html, request.force)
