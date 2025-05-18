import unittest
from unittest.mock import patch

from backend.services.perspectives import (
    PerspectivePipeline,
    generate_perspective,
)
from backend.shared.models import (
    PerspectiveRequest,
    Article,
    DedupGroup,
    ExtractResponse,
    BiasResponse,
)


class PerspectivesTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient
            from backend.main import app

            self.client = TestClient(app)
        except Exception:
            self.client = None

    @patch("backend.services.perspectives.BiasAnnotator.annotate")
    @patch("backend.services.perspectives.Summarizer.summarize")
    @patch("backend.services.perspectives.Deduplicator.group_by_simhash")
    @patch("backend.services.perspectives.SearchAggregator.search")
    @patch("backend.services.perspectives.QueryGenerator.build_queries")
    @patch("backend.services.perspectives.TopicDetector.get_topics")
    @patch("backend.services.perspectives.ArticleExtractor.extract")
    def test_pipeline_function(
        self,
        m_extract,
        m_topics,
        m_queries,
        m_search,
        m_dedup,
        m_sum,
        m_bias,
    ) -> None:
        m_extract.return_value = ExtractResponse(
            clean_text="text", title="t", language="en", chars=4
        )
        m_topics.return_value = ["topic"]
        m_queries.return_value = ["q"]
        m_search.return_value = [Article(url="u", title="T")]
        m_dedup.return_value = [DedupGroup(representative="T", duplicates=[])]
        m_sum.return_value = "summary"
        m_bias.return_value = BiasResponse(bias="Center", bias_score=5)

        resp = generate_perspective(PerspectiveRequest(url="u"))
        self.assertEqual(resp.summary, "summary")
        self.assertEqual(resp.bias, "Center")
        self.assertEqual(resp.topics, ["topic"])
        self.assertEqual(resp.queries, ["q"])
        self.assertEqual(resp.groups, [["T"]])
        self.assertEqual(resp.articles, [Article(url="u", title="T")])

    @patch("backend.services.perspectives.BiasAnnotator.annotate")
    @patch("backend.services.perspectives.Summarizer.summarize")
    @patch("backend.services.perspectives.Deduplicator.group_by_simhash")
    @patch("backend.services.perspectives.SearchAggregator.search")
    @patch("backend.services.perspectives.QueryGenerator.build_queries")
    @patch("backend.services.perspectives.TopicDetector.get_topics")
    @patch("backend.services.perspectives.ArticleExtractor.extract")
    def test_pipeline_endpoint(
        self,
        m_extract,
        m_topics,
        m_queries,
        m_search,
        m_dedup,
        m_sum,
        m_bias,
    ) -> None:
        if not self.client:
            self.skipTest("no fastapi")
        m_extract.return_value = ExtractResponse(
            clean_text="text", title="t", language="en", chars=4
        )
        m_topics.return_value = ["topic"]
        m_queries.return_value = ["q"]
        m_search.return_value = [Article(url="u", title="T")]
        m_dedup.return_value = [DedupGroup(representative="T", duplicates=[])]
        m_sum.return_value = "summary"
        m_bias.return_value = BiasResponse(bias="Center", bias_score=5)

        response = self.client.post("/v1/perspectives/", json={"url": "u"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["summary"], "summary")
        self.assertEqual(response.json()["bias"], "Center")
        self.assertEqual(response.json()["topics"], ["topic"])


if __name__ == "__main__":
    unittest.main()
