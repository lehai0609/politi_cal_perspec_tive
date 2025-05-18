import unittest

from backend.services.queries import QueryGenerator, generate
from backend.shared.models import QueryRequest


class QueryTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient
            from backend.main import app

            self.client = TestClient(app)
        except Exception:
            self.client = None

    def test_build_queries(self):
        queries = QueryGenerator.build_queries(["a", "b"])
        self.assertEqual(queries, ['"a"', '"b"', '"a" AND "b"'])

    def test_generate_function(self):
        resp = generate(QueryRequest(topics=["x"]))
        self.assertEqual(resp.dict(), {"queries": ['"x"']})

    def test_endpoint(self):
        if not self.client:
            self.skipTest("no fastapi")
        response = self.client.post("/queries/", json={"topics": ["x", "y"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"queries": ['"x"', '"y"', '"x" AND "y"']})


if __name__ == "__main__":
    unittest.main()
