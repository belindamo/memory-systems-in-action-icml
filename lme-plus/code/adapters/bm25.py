"""
BM25 Adapter: Proper sparse retrieval with IDF weighting and length normalization
"""
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


class BM25Adapter:
    """
    Proper BM25 implementation with:
    - IDF (Inverse Document Frequency) weighting
    - Document length normalization
    - Term frequency saturation (k1 parameter)

    BM25(D,Q) = Σ IDF(qi) * (f(qi,D) * (k1+1)) / (f(qi,D) + k1 * (1 - b + b * |D|/avgdl))
    """
    def __init__(self, data_dir: Path, k1: float = 1.2, b: float = 0.75):
        self.data_dir = data_dir
        self.env_dir = None
        self.k1 = k1  # Term frequency saturation
        self.b = b    # Length normalization

        # Computed on set_environment
        self.session_data = []
        self.session_tokens = []  # Tokenized sessions
        self.doc_freqs = Counter()  # Document frequency per term
        self.avgdl = 0  # Average document length
        self.N = 0  # Number of documents

    def set_environment(self, env_dir: Path):
        """Set the current question environment and compute IDF statistics"""
        self.env_dir = env_dir

        # Load all sessions
        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        self.session_data = []
        self.session_tokens = []
        self.doc_freqs = Counter()

        total_tokens = 0

        for session_file in session_files:
            with open(session_file) as f:
                data = json.load(f)
                self.session_data.append(data)

                # Tokenize session content
                text = self._session_to_text(data)
                tokens = self._tokenize(text)
                self.session_tokens.append(tokens)

                # Count document frequencies (unique terms per doc)
                unique_terms = set(tokens)
                for term in unique_terms:
                    self.doc_freqs[term] += 1

                total_tokens += len(tokens)

        self.N = len(session_files)
        self.avgdl = total_tokens / self.N if self.N > 0 else 1

    def _session_to_text(self, session_data: Dict) -> str:
        """Convert session to searchable text"""
        parts = []
        for turn in session_data.get("turns", []):
            content = turn.get("content", "")
            parts.append(content)
        return " ".join(parts)

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization: lowercase, split on non-alphanumeric"""
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _idf(self, term: str) -> float:
        """Compute IDF for a term: log((N - df + 0.5) / (df + 0.5) + 1)"""
        df = self.doc_freqs.get(term, 0)
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def _bm25_score(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        """Compute BM25 score for a document given query"""
        doc_len = len(doc_tokens)
        term_freqs = Counter(doc_tokens)

        score = 0.0
        for term in query_tokens:
            if term not in term_freqs:
                continue

            tf = term_freqs[term]
            idf = self._idf(term)

            # BM25 formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
            score += idf * (numerator / denominator)

        return score

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search conversation history using BM25 ranking. Returns top matching sessions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query to find relevant conversations"
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of top sessions to return (default: 3)",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool call"""
        if function_name == "search_memory":
            top_k = args.get("top_k", 3)
            return self._search_memory(args["query"], top_k)
        else:
            return f"Unknown function: {function_name}"

    def _search_memory(self, query: str, top_k: int = 3) -> str:
        """BM25-based search"""
        if not self.env_dir or len(self.session_tokens) == 0:
            return "Error: Environment not set"

        query_tokens = self._tokenize(query)

        # Score all sessions
        scored_sessions = []
        for idx, doc_tokens in enumerate(self.session_tokens):
            score = self._bm25_score(query_tokens, doc_tokens)
            if score > 0:
                scored_sessions.append((score, idx, self.session_data[idx]))

        if not scored_sessions:
            return f"No sessions found matching: {query}"

        # Sort by score (descending) and take top-k
        scored_sessions.sort(reverse=True, key=lambda x: x[0])
        top_sessions = scored_sessions[:top_k]

        # Format results
        lines = [f"Found {len(scored_sessions)} matching session(s). Showing top {len(top_sessions)}:", ""]
        for score, idx, session_data in top_sessions:
            lines.append("=" * 60)
            lines.append(f"[BM25 Score: {score:.2f}]")
            lines.append(self._format_session(session_data))

        return "\n".join(lines)

    def _format_session(self, session_data: Dict) -> str:
        """Format session data for LLM context"""
        lines = [
            f"Session ID: {session_data.get('session_id', 'unknown')}",
            f"Date: {session_data.get('date', 'unknown')}",
            ""
        ]

        for turn in session_data.get("turns", []):
            role = turn.get("role", "unknown").title()
            content = turn.get("content", "")
            lines.append(f"{role}: {content}")
            lines.append("")

        return "\n".join(lines)
