"""In-memory BM25 tool catalog index for fast tool discovery."""
import math
import re
from typing import Dict, List, Any, Tuple


class ToolCatalogSearch:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self._tools: List[Dict[str, Any]] = []
        self._corpus: List[List[str]] = []
        self._doc_lens: List[int] = []
        self._avgdl: float = 0.0
        self._df: Dict[str, int] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def index_tools(self, tools: List[Dict[str, Any]]):
        self._tools = list(tools)
        self._corpus.clear()
        self._doc_lens.clear()
        self._df.clear()

        for tool in tools:
            doc_text = f"{tool.get('name', '')} {tool.get('description', '')}"
            tokens = self._tokenize(doc_text)
            self._corpus.append(tokens)
            self._doc_lens.append(len(tokens))
            for token in set(tokens):
                self._df[token] = self._df.get(token, 0) + 1

        total_docs = len(self._corpus)
        self._avgdl = (sum(self._doc_lens) / total_docs) if total_docs > 0 else 1.0

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        scores = []
        n_docs = len(self._corpus)

        for idx, doc_tokens in enumerate(self._corpus):
            score = 0.0
            doc_len = self._doc_lens[idx]
            for token in query_tokens:
                if token not in self._df:
                    continue
                tf = doc_tokens.count(token)
                df = self._df[token]
                # IDF formula
                idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1.0)
                # BM25 TF formula
                tf_norm = (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * (doc_len / self._avgdl)))
                score += idf * tf_norm
            scores.append((idx, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[:top_k]:
            if score > 0:
                results.append(self._tools[idx])
        return results
