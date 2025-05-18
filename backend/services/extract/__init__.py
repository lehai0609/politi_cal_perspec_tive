from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Optional

try:
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - environment without requests

    class _Response:
        def __init__(self, text: str) -> None:
            self.text = text

    class _Requests:
        def get(self, *args, **kwargs):  # pragma: no cover - HTTP disabled
            raise NotImplementedError

    requests = _Requests()  # type: ignore

from fastapi import APIRouter, HTTPException

from backend.shared.models import ExtractRequest, ExtractResponse

router = APIRouter()


class _TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.chunks: list[str] = []

    def handle_data(self, data: str) -> None:  # pragma: no cover - simple logic
        self.chunks.append(data)

    def get_text(self) -> str:
        return " ".join(self.chunks)


class ArticleExtractor:
    """Naïve article extractor."""

    @staticmethod
    def _extract_text(html: str) -> str:
        parser = _TextParser()
        parser.feed(html)
        text = parser.get_text()
        return " ".join(text.split())

    @staticmethod
    def _get_title(html: str) -> str:
        match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if match:
            return re.sub(r"\s+", " ", match.group(1)).strip()
        return ""

    @classmethod
    def extract(
        cls, url: Optional[str], html: Optional[str], force: bool = False
    ) -> ExtractResponse:
        if (url and html) or (not url and not html):
            raise HTTPException(status_code=400, detail="INVALID_ARGUMENT")
        if url:
            response = requests.get(url)
            html = response.text
        if html is None:
            raise HTTPException(status_code=400, detail="UNREADABLE")
        clean_text = cls._extract_text(html)
        title = cls._get_title(html)
        return ExtractResponse(
            clean_text=clean_text,
            title=title,
            language="en",
            chars=len(clean_text),
        )


@router.post("/", response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse:
    return ArticleExtractor.extract(request.url, request.html, request.force)
