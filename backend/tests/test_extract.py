import unittest
from unittest.mock import patch

from backend.services.extract import ArticleExtractor


class ExtractTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient

            from backend.main import app

            self.client = TestClient(app)
        except Exception:
            self.client = None

    def test_extract_from_html(self):
        html = "<html><head><title>T</title></head><body><p>Hello</p></body></html>"
        resp = ArticleExtractor.extract(None, html)
        self.assertEqual(resp.title, "T")
        self.assertIn("Hello", resp.clean_text)
        self.assertEqual(resp.chars, len(resp.clean_text))

    @patch("backend.services.extract.requests.get")
    def test_extract_from_url(self, mock_get):
        mock_get.return_value.text = (
            "<html><head><title>U</title></head><body><p>Body</p></body></html>"
        )
        resp = ArticleExtractor.extract("http://example.com", None)
        self.assertEqual(resp.title, "U")
        self.assertIn("Body", resp.clean_text)

    def test_endpoint(self):
        if not self.client:
            self.skipTest("no fastapi")
        html = "<html><head><title>T</title></head><body><p>Hello</p></body></html>"
        response = self.client.post("/extract/", json={"html": html})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "T")

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ArticleExtractor.extract(None, None)
        with self.assertRaises(Exception):
            ArticleExtractor.extract("u", "h")


if __name__ == "__main__":
    unittest.main()
