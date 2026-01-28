"""
BGE Adapter: Dense retrieval using BGE embeddings (alternative to Stella V5)
"""
import json
import numpy as np
from pathlib import Path
from typing import Any, Dict, List
from sentence_transformers import SentenceTransformer


class BGEAdapter:
    """
    BGE (BAAI General Embedding) adapter using dense retrieval.
    Tests whether a different embedding model performs differently than Stella V5.

    BGE-large-en-v1.5 is a popular alternative on the MTEB leaderboard.
    """
    def __init__(self, data_dir: Path, model_name: str = "BAAI/bge-large-en-v1.5"):
        self.data_dir = data_dir
        self.model_name = model_name
        self.env_dir = None
        self.model = None
        self.session_embeddings = []
        self.session_data = []

    def _load_model(self):
        """Lazy load BGE model"""
        if self.model is None:
            print(f"Loading {self.model_name} model (this may take a minute)...")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded.")

    def set_environment(self, env_dir: Path):
        """Set the current question environment and pre-compute embeddings"""
        self.env_dir = env_dir
        self._load_model()

        # Load all sessions
        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        self.session_data = []
        session_texts = []

        for session_file in session_files:
            with open(session_file) as f:
                data = json.load(f)
                self.session_data.append(data)

                # Create text representation for embedding
                # BGE recommends adding instruction prefix for queries
                text_parts = []
                for turn in data.get("turns", []):
                    role = turn.get("role", "unknown")
                    content = turn.get("content", "")
                    text_parts.append(f"{role}: {content}")

                session_text = "\n".join(text_parts)
                session_texts.append(session_text)

        # Pre-compute embeddings (no instruction prefix for documents)
        print(f"Embedding {len(session_texts)} sessions with BGE...")
        self.session_embeddings = self.model.encode(
            session_texts,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        print("Embeddings ready.")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search conversation history using semantic similarity. Returns top matching sessions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query to find semantically relevant conversations"
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
        """Dense retrieval: embed query and find nearest sessions"""
        if not self.env_dir or len(self.session_embeddings) == 0:
            return "Error: Environment not set"

        # BGE recommends instruction prefix for queries
        # For retrieval: "Represent this sentence for searching relevant passages: "
        query_with_instruction = f"Represent this sentence for searching relevant passages: {query}"

        # Embed query
        query_embedding = self.model.encode(
            query_with_instruction,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Compute cosine similarity (embeddings already normalized)
        similarities = np.dot(self.session_embeddings, query_embedding)

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Format results
        lines = [f"Found top {len(top_indices)} semantically similar session(s):", ""]
        for idx in top_indices:
            lines.append("=" * 60)
            lines.append(f"[Similarity: {similarities[idx]:.3f}]")
            lines.append(self._format_session(self.session_data[idx]))

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
