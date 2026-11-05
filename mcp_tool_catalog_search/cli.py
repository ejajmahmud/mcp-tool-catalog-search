"""CLI for mcp-tool-catalog-search."""
import sys
import argparse
from .search import ToolCatalogSearch


def main():
    parser = argparse.ArgumentParser(description="MCP Tool Catalog Search")
    parser.add_argument("--demo", action="store_true", help="Run tool catalog search demonstration")
    args = parser.parse_args()

    searcher = ToolCatalogSearch()
    if args.demo:
        catalog = [
            {"name": "query_sql", "description": "Execute queries on PostgreSQL database"},
            {"name": "write_file", "description": "Write text data to local filesystem"},
            {"name": "search_web", "description": "Perform online queries via search engine"},
            {"name": "list_tables", "description": "List all schema tables in database"}
        ]
        searcher.index_tools(catalog)
        found = searcher.search("find tables in relational database", top_k=2)
        print("Discovered Relevant Tools:")
        for t in found:
            print(" -", t["name"], ":", t["description"])
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
