"""
Stella V5 Adapter: Dense retrieval using sentence embeddings
"""
import json
import numpy as np
from pathlib import Path
from typing import Any, Dict, List
from sentence_transformers import SentenceTransformer


class StellaV5Adapter:
    """
    Stella V5 adapter using dense retrieval with sentence embeddings.
    Tests whether dense retrieval beats keyword search.
    """
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.env_dir = None
        self.model = None
        self.session_embeddings = []
        self.session_data = []

    def _load_model(self):
        """Lazy load Stella V5 model"""
        if self.model is None:
            print("Loading Stella V5 model (this may take a minute)...")
            self.model = SentenceTransformer('dunzhang/stella_en_1.5B_v5')
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
                text_parts = []
                for turn in data.get("turns", []):
                    role = turn.get("role", "unknown")
                    content = turn.get("content", "")
                    text_parts.append(f"{role}: {content}")

                session_text = "\n".join(text_parts)
                session_texts.append(session_text)

        # Pre-compute embeddings
        print(f"Embedding {len(session_texts)} sessions...")
        self.session_embeddings = self.model.encode(
            session_texts,
            show_progress_bar=False,
            convert_to_numpy=True
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
        """
        Dense retrieval: embed query and find nearest sessions
        """
        if not self.env_dir or len(self.session_embeddings) == 0:
            return "Error: Environment not set"

        # Embed query
        query_embedding = self.model.encode(
            query,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Normalize session embeddings if not already
        session_norms = np.linalg.norm(self.session_embeddings, axis=1, keepdims=True)
        normalized_sessions = self.session_embeddings / session_norms

        # Compute cosine similarity
        similarities = np.dot(normalized_sessions, query_embedding)

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Format results
        lines = [f"Found top {len(top_indices)} semantically similar session(s):", ""]
        for idx in top_indices:
            lines.append("=" * 60)
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
