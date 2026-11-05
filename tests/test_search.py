"""Tests for mcp-tool-catalog-search."""
import unittest
from mcp_tool_catalog_search.search import ToolCatalogSearch


class TestToolCatalogSearch(unittest.TestCase):
    def setUp(self):
        self.searcher = ToolCatalogSearch()
        self.catalog = [
            {"name": "git_commit", "description": "Commit changes to git version control"},
            {"name": "s3_upload", "description": "Upload cloud object to AWS S3 bucket"}
        ]
        self.searcher.index_tools(self.catalog)

    def test_search_accuracy(self):
        hits = self.searcher.search("git version control", top_k=1)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["name"], "git_commit")


if __name__ == "__main__":
    unittest.main()
