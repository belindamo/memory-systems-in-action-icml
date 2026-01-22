#!/usr/bin/env python3
"""
Convert LongMemEval JSON to LME+ environment format.

Creates the folder structure:
  environments/<question_id>/
    ├── chat_history/
    │   └── session_XXXX_<session_id>.json
    ├── chat_turns/
    │   └── turn_XXXXXX.json
    ├── metadata.json
    └── README.md

Usage:
  python convert_to_environments.py <input_json> <output_dir>

Examples:
  python convert_to_environments.py ../medium/longmemeval_m_cleaned.json ../medium/environments
  python convert_to_environments.py ../oracle/longmemeval_oracle.json ../oracle/environments
"""

import json
import os
import sys
from pathlib import Path


def create_environment(question: dict, output_dir: Path) -> dict:
    """Create an environment folder for a single question."""

    question_id = question["question_id"]
    env_dir = output_dir / question_id
    chat_history_dir = env_dir / "chat_history"
    chat_turns_dir = env_dir / "chat_turns"

    # Create directories
    chat_history_dir.mkdir(parents=True, exist_ok=True)
    chat_turns_dir.mkdir(parents=True, exist_ok=True)

    session_ids = []
    dates = []
    total_turns = 0
    turn_global_index = 0

    # Process each session
    for session_index, (session_id, session_turns, date) in enumerate(zip(
        question["haystack_session_ids"],
        question["haystack_sessions"],
        question["haystack_dates"]
    )):
        session_ids.append(session_id)
        dates.append(date)

        # Create session file
        session_data = {
            "session_id": session_id,
            "session_index": session_index,
            "date": date,
            "turns": session_turns
        }

        session_filename = f"session_{session_index:04d}_{session_id}.json"
        with open(chat_history_dir / session_filename, "w") as f:
            json.dump(session_data, f, indent=2)

        # Create individual turn files
        for turn_in_session, turn in enumerate(session_turns):
            turn_data = {
                "turn_global_index": turn_global_index,
                "session_index": session_index,
                "session_id": session_id,
                "turn_in_session": turn_in_session,
                "date": date,
                "role": turn["role"],
                "content": turn["content"],
                "has_answer": turn.get("has_answer", False)
            }

            turn_filename = f"turn_{turn_global_index:06d}.json"
            with open(chat_turns_dir / turn_filename, "w") as f:
                json.dump(turn_data, f, indent=2)

            turn_global_index += 1

        total_turns += len(session_turns)

    # Count evidence sessions
    answer_session_ids = question.get("answer_session_ids", [])

    # Create metadata.json
    metadata = {
        "question_id": question_id,
        "question_type": question["question_type"],
        "question_date": question["question_date"],
        "num_sessions": len(session_ids),
        "num_turns": total_turns,
        "answer_session_ids": answer_session_ids,
        "session_ids": session_ids,
        "dates": dates
    }

    with open(env_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Create README.md
    readme_content = f"""# Environment: {question_id}

## Question Information
- **Question ID**: {question_id}
- **Question Type**: {question["question_type"]}
- **Question Date**: {question["question_date"]}

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
- Total Sessions: {len(session_ids)}
- Total Turns: {total_turns}
- Evidence Sessions: {len(answer_session_ids)}

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
"""

    with open(env_dir / "README.md", "w") as f:
        f.write(readme_content)

    return metadata


def create_evaluation_file(questions: list, output_dir: Path):
    """Create the evaluation questions file (without chat history)."""

    eval_questions = []
    for q in questions:
        eval_q = {
            "question_id": q["question_id"],
            "question_type": q["question_type"],
            "question": q["question"],
            "answer": q["answer"],
            "question_date": q["question_date"],
            "answer_session_ids": q.get("answer_session_ids", [])
        }
        eval_questions.append(eval_q)

    eval_dir = output_dir.parent / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    # Determine filename based on parent folder name
    parent_name = output_dir.parent.name
    if "medium" in parent_name or "_m" in parent_name:
        filename = "lme_m_questions.json"
    elif "oracle" in parent_name:
        filename = "lme_oracle_questions.json"
    else:
        filename = "lme_s_questions.json"

    with open(eval_dir / filename, "w") as f:
        json.dump(eval_questions, f, indent=2)

    print(f"  Created evaluation file: {eval_dir / filename}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    print(f"Loading {input_file}...")
    with open(input_file) as f:
        questions = json.load(f)

    print(f"Found {len(questions)} questions")

    # Clean output directory if exists
    if output_dir.exists():
        import shutil
        print(f"Cleaning existing directory: {output_dir}")
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each question
    print("Creating environments...")
    question_types = {}

    for i, question in enumerate(questions):
        if (i + 1) % 50 == 0 or i == 0 or i == len(questions) - 1:
            print(f"  Processing {i + 1}/{len(questions)}: {question['question_id']}")

        create_environment(question, output_dir)

        qtype = question["question_type"]
        question_types[qtype] = question_types.get(qtype, 0) + 1

    # Create evaluation file
    print("Creating evaluation file...")
    create_evaluation_file(questions, output_dir)

    # Summary
    print("\nConversion complete!")
    print(f"  Total environments: {len(questions)}")
    print(f"  Output directory: {output_dir}")
    print("\nQuestion types:")
    for qtype, count in sorted(question_types.items()):
        print(f"  {qtype}: {count}")


if __name__ == "__main__":
    main()
