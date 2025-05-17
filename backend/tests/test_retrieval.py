import os
import unittest
from unittest.mock import patch

from backend.services.retrieval.aggregator import SearchAggregator
from backend.services.retrieval.clients import GDELTClient, NewsAPIClient, SerpAPIClient
from backend.shared.models import Article


class ClientTests(unittest.TestCase):
    @patch("backend.services.retrieval.clients.requests.get")
    def test_gdelt_client(self, mock_get):
        mock_get.return_value.json.return_value = {"articles": [{"url": "u", "title": "t"}]}
        client = GDELTClient()
        self.assertEqual(client.search("x"), [Article(url="u", title="t")])

    @patch.dict(os.environ, {"NEWSAPI_KEY": "k"})
    @patch("backend.services.retrieval.clients.requests.get")
    def test_newsapi_client(self, mock_get):
        mock_get.return_value.json.return_value = {"articles": [{"url": "n", "title": "N"}]}
        client = NewsAPIClient()
        self.assertEqual(client.search("x"), [Article(url="n", title="N")])

    @patch.dict(os.environ, {"SERPAPI_KEY": "k"})
    @patch("backend.services.retrieval.clients.requests.get")
    def test_serpapi_client(self, mock_get):
        mock_get.return_value.json.return_value = {"news_results": [{"link": "s", "title": "S"}]}
        client = SerpAPIClient()
        self.assertEqual(client.search("x"), [Article(url="s", title="S")])

    @patch.object(GDELTClient, "search", return_value=[Article(url="a", title="A")])
    @patch.object(NewsAPIClient, "search", return_value=[Article(url="b", title="B")])
    @patch.object(SerpAPIClient, "search", return_value=[Article(url="a", title="C")])
    def test_aggregator_dedup(self, m_serp, m_news, m_gdelt):
        agg = SearchAggregator()
        res = agg.search("q")
        urls = {a.url for a in res}
        self.assertEqual(urls, {"a", "b"})


if __name__ == "__main__":
    unittest.main()
