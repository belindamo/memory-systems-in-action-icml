"""
Oracle Adapter: Perfect retrieval (returns gold answer session)
"""
import json
from pathlib import Path
from typing import Any, Dict, List


class OracleAdapter:
    """
    Oracle adapter that returns the exact session containing the gold answer.
    This establishes the upper bound for performance.
    """
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.env_dir = None
        self.metadata = None

    def set_environment(self, env_dir: Path):
        """Set the current question environment"""
        self.env_dir = env_dir
        # Load metadata to get answer session
        with open(env_dir / "metadata.json") as f:
            self.metadata = json.load(f)

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search through conversation history to find relevant information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query to find relevant conversations"
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
            return self._search_memory(args["query"])
        else:
            return f"Unknown function: {function_name}"

    def _search_memory(self, query: str) -> str:
        """
        Oracle retrieval: return the gold answer session(s)
        """
        if not self.metadata or not self.env_dir:
            return "Error: Environment not set"

        # Get answer session IDs
        answer_session_ids = self.metadata.get("answer_session_ids", [])

        if not answer_session_ids:
            return "No relevant information found."

        # Load all answer sessions
        sessions_content = []
        for session_id in answer_session_ids:
            # Find the session file
            session_file = self._find_session_file(session_id)
            if session_file:
                with open(session_file) as f:
                    session_data = json.load(f)
                    sessions_content.append(self._format_session(session_data))

        if not sessions_content:
            return "No relevant information found."

        return "\n\n---\n\n".join(sessions_content)

    def _find_session_file(self, session_id: str) -> Path:
        """Find the session file by session_id"""
        chat_history_dir = self.env_dir / "chat_history"
        for session_file in chat_history_dir.glob("*.json"):
            with open(session_file) as f:
                data = json.load(f)
                if data.get("session_id") == session_id:
                    return session_file
        return None

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
