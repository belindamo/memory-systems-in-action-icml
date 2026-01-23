"""
Hybrid Adapter: Keyword search + embedding reranking
"""
import json
import numpy as np
from pathlib import Path
from typing import Any, Dict, List
from sentence_transformers import SentenceTransformer


class HybridAdapter:
    """
    Hybrid adapter combining keyword search (recall) + embedding reranking (precision).
    Strategy: MCP keyword search retrieves top-10, then Stella V5 reranks to top-3.
    """
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.env_dir = None
        self.model = None
        self.session_data = []

    def _load_model(self):
        """Lazy load Stella V5 model"""
        if self.model is None:
            print("Loading Stella V5 for reranking...")
            self.model = SentenceTransformer('dunzhang/stella_en_1.5B_v5')
            print("Model ready.")

    def set_environment(self, env_dir: Path):
        """Set the current question environment"""
        self.env_dir = env_dir

        # Load all sessions (no pre-embedding - we'll embed on-demand)
        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        self.session_data = []
        for session_file in session_files:
            with open(session_file) as f:
                data = json.load(f)
                self.session_data.append(data)

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search conversation history using hybrid keyword + semantic reranking. Returns top matching sessions.",
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
        """
        Hybrid retrieval:
        1. Keyword search (MCP-style) to get top-10 candidates
        2. Embed query + candidates
        3. Rerank by cosine similarity
        4. Return top-k
        """
        if not self.env_dir or len(self.session_data) == 0:
            return "Error: Environment not set"

        # Step 1: Keyword search (MCP-style) for recall
        keywords = set(query.lower().split())

        scored_sessions = []
        for idx, session_data in enumerate(self.session_data):
            # Create text representation
            text_parts = []
            for turn in session_data.get("turns", []):
                content = turn.get("content", "")
                text_parts.append(content)

            session_text = " ".join(text_parts).lower()

            # Score by keyword frequency
            score = sum(session_text.count(kw) for kw in keywords)
            if score > 0:
                scored_sessions.append((score, idx, session_data, session_text))

        if not scored_sessions:
            return f"No sessions found matching: {query}"

        # Get top-10 candidates (or all if fewer)
        scored_sessions.sort(reverse=True, key=lambda x: x[0])
        candidates = scored_sessions[:min(10, len(scored_sessions))]

        # Step 2: Rerank with embeddings for precision
        if len(candidates) > top_k:
            self._load_model()

            # Embed query
            query_embedding = self.model.encode(
                query,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            # Embed candidate sessions
            candidate_texts = [c[3] for c in candidates]
            candidate_embeddings = self.model.encode(
                candidate_texts,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            # Compute cosine similarity
            similarities = np.dot(candidate_embeddings, query_embedding)

            # Rerank by similarity
            reranked_indices = np.argsort(similarities)[-top_k:][::-1]
            top_sessions = [candidates[i] for i in reranked_indices]
        else:
            # If candidates <= top_k, no need to rerank
            top_sessions = candidates[:top_k]

        # Format results
        lines = [f"Found {len(scored_sessions)} matching session(s). Showing top {len(top_sessions)} (hybrid ranked):", ""]
        for score, idx, session_data, _ in top_sessions:
            lines.append("=" * 60)
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
