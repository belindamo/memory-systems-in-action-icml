"""
MCP Filesystem Adapter: Proper filesystem tools matching MCP specification

Based on: https://github.com/modelcontextprotocol/servers/blob/main/src/filesystem/README.md

Provides read/write/search tools that agents trained on coding tasks will be familiar with.
"""
import json
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List


class MCPFilesystemAdapter:
    """
    MCP-compatible filesystem adapter with standard file operations.

    Tools:
    - list_directory: List contents with metadata
    - read_file: Read file contents
    - search_files: Search for files matching patterns
    - grep_files: Search within file contents
    """
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.env_dir = None
        self.chat_history_dir = None

    def set_environment(self, env_dir: Path):
        """Set the current question environment"""
        self.env_dir = env_dir
        self.chat_history_dir = env_dir / "chat_history"

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return OpenAI function calling tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List all conversation session files with metadata (date, number of turns). Returns file indices that can be used with read_file.",
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
                    "name": "read_file",
                    "description": "Read the complete contents of a conversation session file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_index": {
                                "type": "integer",
                                "description": "Index of the file to read (from list_directory output)"
                            }
                        },
                        "required": ["file_index"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_files",
                    "description": "Search for conversation files matching a date or session ID pattern.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": "Pattern to match (e.g., '2024-01*' for January 2024, '*ultrachat*' for source)"
                            }
                        },
                        "required": ["pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "grep_files",
                    "description": "Search for text content across all conversation files. Returns matching files with context.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Text to search for in conversation content"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of matching files to return (default: 5)",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_multiple_files",
                    "description": "Read multiple conversation files at once by their indices.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_indices": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "List of file indices to read"
                            }
                        },
                        "required": ["file_indices"]
                    }
                }
            }
        ]

    def execute_tool(self, function_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool call"""
        if function_name == "list_directory":
            return self._list_directory()
        elif function_name == "read_file":
            return self._read_file(args["file_index"])
        elif function_name == "search_files":
            return self._search_files(args["pattern"])
        elif function_name == "grep_files":
            max_results = args.get("max_results", 5)
            return self._grep_files(args["query"], max_results)
        elif function_name == "read_multiple_files":
            return self._read_multiple_files(args["file_indices"])
        else:
            return f"Unknown function: {function_name}"

    def _list_directory(self) -> str:
        """List all session files with metadata"""
        if not self.chat_history_dir:
            return "Error: Environment not set"

        session_files = sorted(self.chat_history_dir.glob("*.json"))

        if not session_files:
            return "No conversation files found."

        lines = [
            f"Conversation history directory: {len(session_files)} files",
            "",
            "Index | Date       | Session ID                    | Turns",
            "-" * 65
        ]

        for idx, session_file in enumerate(session_files):
            with open(session_file) as f:
                data = json.load(f)
                session_id = data.get("session_id", "unknown")[:30]
                date = data.get("date", "unknown")[:10]
                num_turns = len(data.get("turns", []))
                lines.append(f"{idx:5} | {date:10} | {session_id:30} | {num_turns:5}")

        lines.append("")
        lines.append("Use read_file(index) to view a session, or grep_files(query) to search.")

        return "\n".join(lines)

    def _read_file(self, file_index: int) -> str:
        """Read a specific session file"""
        if not self.chat_history_dir:
            return "Error: Environment not set"

        session_files = sorted(self.chat_history_dir.glob("*.json"))

        if file_index < 0 or file_index >= len(session_files):
            return f"Error: Invalid file index {file_index}. Valid range: 0-{len(session_files)-1}"

        session_file = session_files[file_index]
        with open(session_file) as f:
            session_data = json.load(f)

        return self._format_session(session_data, file_index)

    def _search_files(self, pattern: str) -> str:
        """Search for files matching pattern"""
        if not self.chat_history_dir:
            return "Error: Environment not set"

        session_files = sorted(self.chat_history_dir.glob("*.json"))
        matching = []

        for idx, session_file in enumerate(session_files):
            with open(session_file) as f:
                data = json.load(f)
                session_id = data.get("session_id", "")
                date = data.get("date", "")

                # Check if pattern matches session_id, date, or filename
                searchable = f"{session_id} {date} {session_file.name}"
                if fnmatch(searchable.lower(), f"*{pattern.lower()}*"):
                    num_turns = len(data.get("turns", []))
                    matching.append(f"[{idx}] {date} - {session_id} ({num_turns} turns)")

        if not matching:
            return f"No files matching pattern: {pattern}"

        lines = [f"Found {len(matching)} file(s) matching '{pattern}':", ""] + matching
        lines.append("")
        lines.append("Use read_file(index) to view a file.")

        return "\n".join(lines)

    def _grep_files(self, query: str, max_results: int = 5) -> str:
        """Search content across all files"""
        if not self.chat_history_dir:
            return "Error: Environment not set"

        session_files = sorted(self.chat_history_dir.glob("*.json"))
        query_lower = query.lower()
        matches = []

        for idx, session_file in enumerate(session_files):
            with open(session_file) as f:
                content = f.read()
                content_lower = content.lower()

                if query_lower in content_lower:
                    # Find matching context
                    f.seek(0)
                    data = json.load(f)

                    # Find which turn(s) contain the query
                    matching_turns = []
                    for turn_idx, turn in enumerate(data.get("turns", [])):
                        turn_content = turn.get("content", "")
                        if query_lower in turn_content.lower():
                            # Extract snippet around match
                            snippet = self._extract_snippet(turn_content, query, max_len=100)
                            matching_turns.append((turn_idx, turn.get("role", "?"), snippet))

                    matches.append({
                        "index": idx,
                        "session_id": data.get("session_id", "unknown"),
                        "date": data.get("date", "unknown"),
                        "matching_turns": matching_turns[:3]  # Limit turns shown
                    })

                    if len(matches) >= max_results:
                        break

        if not matches:
            return f"No files contain: {query}"

        lines = [f"Found {len(matches)} file(s) containing '{query}':", ""]

        for match in matches:
            lines.append(f"[{match['index']}] {match['date']} - {match['session_id']}")
            for turn_idx, role, snippet in match["matching_turns"]:
                lines.append(f"  Turn {turn_idx} ({role}): ...{snippet}...")
            lines.append("")

        lines.append("Use read_file(index) to view full content.")

        return "\n".join(lines)

    def _read_multiple_files(self, file_indices: List[int]) -> str:
        """Read multiple files at once"""
        if not self.chat_history_dir:
            return "Error: Environment not set"

        session_files = sorted(self.chat_history_dir.glob("*.json"))
        results = []

        for file_index in file_indices[:5]:  # Limit to 5 files
            if 0 <= file_index < len(session_files):
                with open(session_files[file_index]) as f:
                    data = json.load(f)
                    results.append(self._format_session(data, file_index))
            else:
                results.append(f"[Error: Invalid index {file_index}]")

        return "\n\n".join(results)

    def _extract_snippet(self, text: str, query: str, max_len: int = 100) -> str:
        """Extract snippet around query match"""
        idx = text.lower().find(query.lower())
        if idx == -1:
            return text[:max_len]

        start = max(0, idx - max_len // 2)
        end = min(len(text), idx + len(query) + max_len // 2)
        snippet = text[start:end]

        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet

    def _format_session(self, session_data: Dict, file_index: int) -> str:
        """Format session data for LLM context"""
        lines = [
            f"=== File [{file_index}] ===",
            f"Session ID: {session_data.get('session_id', 'unknown')}",
            f"Date: {session_data.get('date', 'unknown')}",
            f"Turns: {len(session_data.get('turns', []))}",
            ""
        ]

        for turn in session_data.get("turns", []):
            role = turn.get("role", "unknown").title()
            content = turn.get("content", "")
            lines.append(f"{role}: {content}")
            lines.append("")

        return "\n".join(lines)
