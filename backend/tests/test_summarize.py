import unittest

from backend.services.summarize import Summarizer, summarize_endpoint
from backend.shared.models import SummarizeRequest


class SummarizeTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient

            from backend.main import app

            self.client = TestClient(app)
        except Exception:
            self.client = None

    def test_summarizer_class(self):
        text = "A. B. C. D."
        summary = Summarizer.summarize(text, max_sentences=2)
        self.assertEqual(summary, "A. B.")

    def test_summarize_function(self):
        resp = summarize_endpoint(SummarizeRequest(text="A. B. C.", max_sentences=1))
        self.assertEqual(resp.dict(), {"summary": "A."})

    def test_summarize_endpoint(self):
        if not self.client:
            self.skipTest("no fastapi")
        response = self.client.post(
            "/summarize/",
            json={"text": "A. B. C.", "max_sentences": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"summary": "A. B."})


if __name__ == "__main__":
    unittest.main()
