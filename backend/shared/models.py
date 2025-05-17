from __future__ import annotations

from typing import List

from pydantic import BaseModel


class TopicRequest(BaseModel):
    text: str


class TopicResponse(BaseModel):
    topics: List[str]


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    results: List[str]


class DedupRequest(BaseModel):
    items: List[str]


class DedupGroup(BaseModel):
    representative: str
    duplicates: List[str]


class DedupResponse(BaseModel):
    groups: List[DedupGroup]
