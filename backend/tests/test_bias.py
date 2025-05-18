import unittest

from backend.services.bias import BiasAnnotator, bias_endpoint
from backend.shared.models import BiasRequest


class BiasTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient

            from backend.main import app

            self.client = TestClient(app)
        except Exception:
            self.client = None

    def test_bias_annotator_class(self):
        result = BiasAnnotator.annotate("Fox News")
        self.assertEqual(result.bias, "Right")
        self.assertEqual(result.bias_score, 10)

    def test_bias_function(self):
        resp = bias_endpoint(BiasRequest(source="MSNBC"))
        self.assertEqual(resp.dict(), {"bias": "Left", "bias_score": 10})

    def test_bias_endpoint(self):
        if not self.client:
            self.skipTest("no fastapi")
        response = self.client.post("/bias/", json={"source": "AP"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"bias": "Center", "bias_score": 5})


if __name__ == "__main__":
    unittest.main()
