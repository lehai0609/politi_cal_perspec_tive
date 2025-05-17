import unittest
from unittest.mock import patch

from backend.services.dedup import group
from backend.services.retrieval import search as search_endpoint
from backend.services.topics import detect_topics
from backend.shared.models import Article, TopicRequest, SearchRequest, DedupRequest


class APITestCase(unittest.TestCase):
    def test_topics(self):
        resp = detect_topics(TopicRequest(text="hello world hello"))
        self.assertEqual(resp.dict(), {"topics": ["hello", "world"]})

    def test_search(self):
        dummy = [Article(url="http://example.com", title="Example")]
        with patch(
            "backend.services.retrieval.aggregator.SearchAggregator.search",
            return_value=dummy,
        ):
            resp = search_endpoint(SearchRequest(query="news"))
        self.assertEqual(
            resp.dict(),
            {"articles": [{"url": "http://example.com", "title": "Example"}]},
        )

    def test_dedup(self):
        resp = group(DedupRequest(items=["a", "a", "b"]))
        self.assertEqual(resp.dict(), {"groups": [["a", "a"], ["b"]]})


if __name__ == "__main__":
    unittest.main()
