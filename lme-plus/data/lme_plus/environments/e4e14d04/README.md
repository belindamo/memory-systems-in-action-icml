# Environment: e4e14d04

## Question Information
- **Question ID**: e4e14d04
- **Question Type**: temporal-reasoning
- **Question Date**: 2023/05/28 (Sun) 15:46

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
- Total Sessions: 45
- Total Turns: 461
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
