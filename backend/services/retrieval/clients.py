from __future__ import annotations

import os
from typing import List

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for restricted envs
    class _StubResponse:  # minimal stub so tests can patch requests.get
        def __init__(self, data):
            self._data = data
            self.status_code = 200

        def json(self):
            return self._data

    class _Requests:
        def get(self, *args, **kwargs):  # pragma: no cover - real HTTP disabled
            raise NotImplementedError("requests module not available")

    requests = _Requests()  # type: ignore

from backend.shared.models import Article


class GDELTClient:
    """Client for the GDELT Events API."""

    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def search(self, query: str) -> List[Article]:
        params = {
            "query": query,
            "mode": "ArtList",
            "maxrecords": 10,
            "format": "json",
        }
        response = requests.get(self.BASE_URL, params=params, timeout=5)
        data = response.json()
        articles = []
        for item in data.get("articles", []):
            url = item.get("url")
            title = item.get("title", "")
            if url:
                articles.append(Article(url=url, title=title))
        return articles


class NewsAPIClient:
    """Client for the NewsAPI service."""

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self) -> None:
        self.api_key = os.environ.get("NEWSAPI_KEY", "")

    def search(self, query: str) -> List[Article]:
        if not self.api_key:
            return []
        params = {"q": query, "pageSize": 10, "apiKey": self.api_key}
        response = requests.get(self.BASE_URL, params=params, timeout=5)
        data = response.json()
        articles = []
        for item in data.get("articles", []):
            url = item.get("url")
            title = item.get("title", "")
            if url:
                articles.append(Article(url=url, title=title))
        return articles


class SerpAPIClient:
    """Client for the SerpAPI Google News API."""

    BASE_URL = "https://serpapi.com/search.json"

    def __init__(self) -> None:
        self.api_key = os.environ.get("SERPAPI_KEY", "")

    def search(self, query: str) -> List[Article]:
        if not self.api_key:
            return []
        params = {"q": query, "api_key": self.api_key, "engine": "google", "tbm": "nws"}
        response = requests.get(self.BASE_URL, params=params, timeout=5)
        data = response.json()
        articles = []
        for item in data.get("news_results", []):
            url = item.get("link") or item.get("url")
            title = item.get("title", "")
            if url:
                articles.append(Article(url=url, title=title))
        return articles
