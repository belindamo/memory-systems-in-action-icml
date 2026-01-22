# Environment: 4d6b87c8

## Question Information
- **Question ID**: 4d6b87c8
- **Question Type**: knowledge-update
- **Question Date**: 2023/06/03 (Sat) 15:47

## Chat History Structure

This environment contains chat history in two formats:

### 1. Session-based format (chat_history/)
- Each file represents one complete conversation session
- Files are named: `session_XXXX_<session_id>.json`
- Each session contains:
  - `session_id`: Original session identifier
  - `session_index`: Sequential index (0-based)
  - `date`: Timestamp of the session
  - `turns`: List of conversation turns in the session

### 2. Turn-based format (chat_turns/)
- Each file represents one conversation turn
- Files are named: `turn_XXXXXX.json`
- Each turn contains:
  - `turn_global_index`: Global sequential index across all sessions
  - `session_index`: Which session this turn belongs to
  - `session_id`: Original session identifier
  - `turn_in_session`: Turn index within its session
  - `date`: Timestamp of the session
  - `role`: "user" or "assistant"
  - `content`: The message content
  - `has_answer`: Whether this turn contains evidence for the question

## Statistics
- Total Sessions: 52
- Total Turns: 516
- Evidence Sessions: 2

## Usage Modes

### Filesystem Access Mode
Agents can directly read files from `chat_history/` or `chat_turns/` directories.

### Memory Ingestion Mode
Chat history can be ingested into memory systems from either format.

### Combined Mode
Agents can access both filesystem and memory systems simultaneously.

## Evaluation
The question and ground truth answer are stored separately in the evaluation dataset.
Do not access the evaluation data when running agents in this environment.
