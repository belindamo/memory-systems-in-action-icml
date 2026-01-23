"""
Filesystem Adapter: Direct file access to conversation history
"""
import json
from pathlib import Path
from typing import Any, Dict, List


class FilesystemAdapter:
    """
    Filesystem adapter that gives agent direct access to conversation files.
    Tests whether simple file access is sufficient for memory retrieval.
    """
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.env_dir = None

    def set_environment(self, env_dir: Path):
        """Set the current question environment"""
        self.env_dir = env_dir

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_sessions",
                    "description": "List all conversation sessions with metadata (date, session_id)",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_session",
                    "description": "Read the full content of a specific conversation session",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "session_index": {
                                "type": "integer",
                                "description": "Index of the session to read (from list_sessions)"
                            }
                        },
                        "required": ["session_index"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_sessions",
                    "description": "Search for sessions containing specific keywords",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "string",
                                "description": "Keywords to search for in session content"
                            }
                        },
                        "required": ["keywords"]
                    }
                }
            }
        ]

    def execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool call"""
        if function_name == "list_sessions":
            return self._list_sessions()
        elif function_name == "read_session":
            return self._read_session(args["session_index"])
        elif function_name == "search_sessions":
            return self._search_sessions(args["keywords"])
        else:
            return f"Unknown function: {function_name}"

    def _list_sessions(self) -> str:
        """List all sessions with metadata"""
        if not self.env_dir:
            return "Error: Environment not set"

        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        if not session_files:
            return "No sessions found."

        lines = ["Available sessions:", ""]
        for idx, session_file in enumerate(session_files):
            with open(session_file) as f:
                data = json.load(f)
                session_id = data.get("session_id", "unknown")
                date = data.get("date", "unknown")
                num_turns = len(data.get("turns", []))
                lines.append(f"[{idx}] {date} - {session_id} ({num_turns} turns)")

        return "\n".join(lines)

    def _read_session(self, session_index: int) -> str:
        """Read a specific session by index"""
        if not self.env_dir:
            return "Error: Environment not set"

        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        if session_index < 0 or session_index >= len(session_files):
            return f"Error: Invalid session index {session_index}. Valid range: 0-{len(session_files)-1}"

        session_file = session_files[session_index]
        with open(session_file) as f:
            session_data = json.load(f)

        return self._format_session(session_data)

    def _search_sessions(self, keywords: str) -> str:
        """Search for sessions containing keywords"""
        if not self.env_dir:
            return "Error: Environment not set"

        chat_history_dir = self.env_dir / "chat_history"
        session_files = sorted(chat_history_dir.glob("*.json"))

        keywords_lower = keywords.lower()
        matching_sessions = []

        for idx, session_file in enumerate(session_files):
            with open(session_file) as f:
                content = f.read().lower()
                if keywords_lower in content:
                    # Load session data
                    f.seek(0)
                    session_data = json.load(f)
                    date = session_data.get("date", "unknown")
                    session_id = session_data.get("session_id", "unknown")
                    matching_sessions.append(f"[{idx}] {date} - {session_id}")

        if not matching_sessions:
            return f"No sessions found containing: {keywords}"

        lines = [
            f"Found {len(matching_sessions)} session(s) containing '{keywords}':",
            ""
        ] + matching_sessions + [
            "",
            "Use read_session(index) to view full content."
        ]

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
