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


class DedupRequest(BaseModel):
    items: List[str]


class DedupGroup(BaseModel):
    representative: str
    duplicates: List[str]


class DedupResponse(BaseModel):
    groups: List[DedupGroup]
