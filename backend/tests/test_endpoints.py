import unittest

from fastapi.testclient import TestClient

from backend.main import app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_topics(self):
        response = self.client.post("/topics/", json={"text": "hello world hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"topics": ["hello", "world"]})

    def test_search(self):
        response = self.client.post("/search/", json={"query": "news"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results": ["news", "news result"]})

    def test_dedup(self):
        response = self.client.post("/dedup/", json={"items": ["a", "a", "b"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"groups": [["a", "a"], ["b"]]})


if __name__ == "__main__":
    unittest.main()
