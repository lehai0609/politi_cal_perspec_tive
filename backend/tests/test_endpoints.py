import unittest
from unittest.mock import patch

# Import both sets of dependencies
from backend.services.dedup import Deduplicator, group
from backend.services.retrieval import SearchAggregator, search as search_endpoint
from backend.services.topics import TopicDetector, detect_topics
from backend.shared.models import Article, TopicRequest, SearchRequest, DedupRequest


class APITestCase(unittest.TestCase):
    def setUp(self):
        # If you have an API client, set it up here
        try:
            from backend.main import app
            from fastapi.testclient import TestClient
            self.client = TestClient(app)
        except Exception:
            self.client = None  # If FastAPI or TestClient is not used, skip API tests

    # --- Topics tests ---

    def test_topics_detector_class(self):
        # Direct class-based logic test
        topics = TopicDetector.get_topics("hello world hello")
        self.assertEqual(topics, ["hello", "world"])

    def test_topics_detect_topics_function(self):
        # Direct function test using datamodel
        resp = detect_topics(TopicRequest(text="hello world hello"))
        self.assertEqual(resp.dict(), {"topics": ["hello", "world"]})

    def test_topics_api_endpoint(self):
        # API endpoint test (only runs if self.client is available)
        if self.client:
            text = "Barack Obama met Angela Merkel in Berlin."
            response = self.client.post("/topics/", json={"text": text})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {"topics": ["Barack Obama", "Angela Merkel", "Berlin"]},
            )

    # --- Search tests ---

    def test_search_aggregator_class(self):
        # Direct class-based logic test
        results = SearchAggregator.search("news")
        self.assertEqual(results, ["news", "news result"])

    def test_search_api_function(self):
        # Using mock to test API search endpoint function
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

    # --- Deduplication tests ---

    def test_dedup_class_simhash(self):
        # Deduplicator class/group_by_simhash logic
        groups = Deduplicator.group_by_simhash(["a", "a", "b"])
        self.assertEqual(
            [g.dict() for g in groups],
            [
                {"representative": "a", "duplicates": ["a"]},
                {"representative": "b", "duplicates": []},
            ],
        )

    def test_dedup_function(self):
        # Using API function/dedup endpoint logic
        resp = group(DedupRequest(items=["a", "a", "b"]))
        self.assertEqual(resp.dict(), {"groups": [["a", "a"], ["b"]]})

    def test_near_duplicate_grouping(self):
        # Test near-duplicate grouping logic
        items = ["hello world", "hello world!", "another text"]
        groups = Deduplicator.group_by_simhash(items)
        self.assertEqual(len(groups), 2)
        first_group = groups[0].dict()
        self.assertIn(first_group["representative"], {"hello world", "hello world!"})
        self.assertEqual(len(first_group["duplicates"]), 1)
        self.assertIn(first_group["duplicates"][0], {"hello world", "hello world!"})


if __name__ == "__main__":
    unittest.main()
