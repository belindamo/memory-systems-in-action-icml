"""
Built-in MCP Adapter: Simulates keyword-based memory tool
"""
import json
from pathlib import Path
from typing import Any, Dict, List


class BuiltinMCPAdapter:
    """
    Simulates a built-in MCP memory tool with keyword-based search.
    Returns top-k sessions based on keyword match frequency.
    """
    def __init__(self, data_dir: Path, enable_filesystem: bool = False):
        self.data_dir = data_dir
        self.env_dir = None
        self.enable_filesystem = enable_filesystem

    def set_environment(self, env_dir: Path):
        """Set the current question environment"""
        self.env_dir = env_dir

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_memory",
                    "description": "Search conversation history using keywords. Returns top matching sessions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query with keywords to find relevant conversations"
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

        # Optionally add filesystem tools
        if self.enable_filesystem:
            tools.append({
                "type": "function",
                "function": {
                    "name": "read_session",
                    "description": "Read a specific session by index",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "session_index": {
                                "type": "integer",
                                "description": "Index of the session (0 to num_sessions-1)"
                            }
                        },
                        "required": ["session_index"]
                    }
                }
            })

        return tools

    def execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool call"""
        if function_name == "search_memory":
            top_k = args.get("top_k", 3)
            return self._search_memory(args["query"], top_k)
        elif function_name == "read_session" and self.enable_filesystem:
            return self._read_session(args["session_index"])
        else:
            return f"Unknown function: {function_name}"

    def _search_memory(self, query: str, top_k: int = 3) -> str:
        """
        Keyword-based search: score sessions by keyword frequency
        """
        if not self.env_dir:
            return "Error: Environment not set"

        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        if not session_files:
            return "No sessions found."

        # Extract keywords (simple: lowercase words)
        keywords = set(query.lower().split())

        # Score each session
        scored_sessions = []
        for idx, session_file in enumerate(session_files):
            with open(session_file) as f:
                content = f.read().lower()
                score = sum(content.count(kw) for kw in keywords)
                if score > 0:
                    f.seek(0)
                    session_data = json.load(f)
                    scored_sessions.append((score, idx, session_data))

        if not scored_sessions:
            return f"No sessions found matching: {query}"

        # Sort by score (descending) and take top-k
        scored_sessions.sort(reverse=True, key=lambda x: x[0])
        top_sessions = scored_sessions[:top_k]

        # Format results
        lines = [f"Found {len(scored_sessions)} matching session(s). Showing top {len(top_sessions)}:", ""]
        for score, idx, session_data in top_sessions:
            lines.append("=" * 60)
            lines.append(self._format_session(session_data))

        return "\\n".join(lines)

    def _read_session(self, session_index: int) -> str:
        """Read a specific session by index"""
        if not self.env_dir:
            return "Error: Environment not set"

        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        if session_index < 0 or session_index >= len(session_files):
            return f"Error: Invalid session index. Valid range: 0-{len(session_files)-1}"

        with open(session_files[session_index]) as f:
            session_data = json.load(f)

        return self._format_session(session_data)

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

        return "\\n".join(lines)
