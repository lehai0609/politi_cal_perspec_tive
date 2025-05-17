from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from .clients import GDELTClient, NewsAPIClient, SerpAPIClient
from backend.shared.models import Article


class SearchAggregator:
    """Aggregates search results from multiple news APIs."""

    def __init__(self) -> None:
        self.clients = [GDELTClient(), NewsAPIClient(), SerpAPIClient()]

    def search(self, query: str) -> List[Article]:
        results: List[Article] = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(c.search, query) for c in self.clients]
            for future in as_completed(futures):
                try:
                    results.extend(future.result())
                except Exception:
                    pass
        dedup: dict[str, Article] = {}
        for art in results:
            if art.url not in dedup:
                dedup[art.url] = art
        return list(dedup.values())
