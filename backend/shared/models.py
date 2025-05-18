from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Article(BaseModel):
    """Represents a single news article."""

    url: str
    title: str


class TopicRequest(BaseModel):
    text: str


class TopicResponse(BaseModel):
    topics: List[str]


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    articles: List[Article]


class QueryRequest(BaseModel):
    topics: List[str]


class QueryResponse(BaseModel):
    queries: List[str]


class DedupRequest(BaseModel):
    items: List[str]


class DedupGroup(BaseModel):
    representative: str
    duplicates: List[str]


class DedupResponse(BaseModel):
    groups: List[List[str]]


class ExtractRequest(BaseModel):
    """Request body for the article extractor."""

    url: str | None = None
    html: str | None = None
    force: bool = False


class ExtractResponse(BaseModel):
    clean_text: str
    title: str
    language: str
    chars: int


class SummarizeRequest(BaseModel):
    text: str
    max_sentences: int = 3


class SummarizeResponse(BaseModel):
    summary: str


class BiasRequest(BaseModel):
    source: str


class BiasResponse(BaseModel):
    bias: str
    bias_score: int
