import unittest

from backend.services.dedup import Deduplicator
from backend.services.retrieval import SearchAggregator
from backend.services.topics import TopicDetector


class APITestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_topics(self):
        topics = TopicDetector.get_topics("hello world hello")
        self.assertEqual(topics, ["hello", "world"])

    def test_search(self):
        results = SearchAggregator.search("news")
        self.assertEqual(results, ["news", "news result"])

    def test_dedup(self):
        groups = Deduplicator.group_by_simhash(["a", "a", "b"])
        self.assertEqual(
            [g.dict() for g in groups],
            [
                {"representative": "a", "duplicates": ["a"]},
                {"representative": "b", "duplicates": []},
            ],
        )

    def test_near_duplicate_grouping(self):
        items = ["hello world", "hello world!", "another text"]
        groups = Deduplicator.group_by_simhash(items)
        self.assertEqual(len(groups), 2)
        first_group = groups[0].dict()
        self.assertIn(first_group["representative"], {"hello world", "hello world!"})
        self.assertEqual(len(first_group["duplicates"]), 1)
        self.assertIn(first_group["duplicates"][0], {"hello world", "hello world!"})


if __name__ == "__main__":
    unittest.main()
