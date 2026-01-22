#!/usr/bin/env python3
"""
LME+ Data Setup Script

Downloads LongMemEval data from HuggingFace and converts to LME+ environment format.

Usage:
  python setup_data.py [--variant small|medium|oracle|all] [--force]

Examples:
  python setup_data.py                    # Set up all variants
  python setup_data.py --variant small    # Set up only small variant
  python setup_data.py --variant medium   # Set up only medium variant (2.5GB download)
  python setup_data.py --force            # Re-download and regenerate even if exists
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# HuggingFace URLs for LongMemEval data
HUGGINGFACE_BASE = "https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main"
VARIANTS = {
    "small": {
        "filename": "longmemeval_s_cleaned.json",
        "size": "~265MB",
        "sessions": "~40/question"
    },
    "medium": {
        "filename": "longmemeval_m_cleaned.json",
        "size": "~2.5GB",
        "sessions": "~500/question"
    },
    "oracle": {
        "filename": "longmemeval_oracle.json",
        "size": "~15MB",
        "sessions": "1-5/question (gold evidence only)"
    }
}


def download_file(url: str, dest: Path) -> bool:
    """Download a file using curl with progress."""
    print(f"  Downloading from {url}")
    print(f"  Destination: {dest}")

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            ["curl", "-L", "-o", str(dest), "--progress-bar", url],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error downloading: {e}")
        return False


def create_environment(question: dict, output_dir: Path) -> dict:
    """Create an environment folder for a single question."""
    question_id = question["question_id"]
    env_dir = output_dir / question_id
    chat_history_dir = env_dir / "chat_history"
    chat_turns_dir = env_dir / "chat_turns"

    chat_history_dir.mkdir(parents=True, exist_ok=True)
    chat_turns_dir.mkdir(parents=True, exist_ok=True)

    session_ids = []
    dates = []
    total_turns = 0
    turn_global_index = 0

    for session_index, (session_id, session_turns, date) in enumerate(zip(
        question["haystack_session_ids"],
        question["haystack_sessions"],
        question["haystack_dates"]
    )):
        session_ids.append(session_id)
        dates.append(date)

        session_data = {
            "session_id": session_id,
            "session_index": session_index,
            "date": date,
            "turns": session_turns
        }

        session_filename = f"session_{session_index:04d}_{session_id}.json"
        with open(chat_history_dir / session_filename, "w") as f:
            json.dump(session_data, f, indent=2)

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

    answer_session_ids = question.get("answer_session_ids", [])

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

    return metadata


def create_evaluation_file(questions: list, variant: str, output_dir: Path):
    """Create the evaluation questions file."""
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

    eval_dir = output_dir / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    filename_map = {"small": "lme_s_questions.json", "medium": "lme_m_questions.json", "oracle": "lme_oracle_questions.json"}
    filename = filename_map.get(variant, f"lme_{variant}_questions.json")

    with open(eval_dir / filename, "w") as f:
        json.dump(eval_questions, f, indent=2)

    print(f"  Created evaluation file: {eval_dir / filename}")


def convert_to_environments(json_path: Path, env_dir: Path, variant: str):
    """Convert JSON to environment format."""
    print(f"  Loading {json_path}...")
    with open(json_path) as f:
        questions = json.load(f)

    print(f"  Found {len(questions)} questions")

    if env_dir.exists():
        print(f"  Cleaning existing directory: {env_dir}")
        shutil.rmtree(env_dir)

    env_dir.mkdir(parents=True, exist_ok=True)

    print("  Creating environments...")
    question_types = {}

    for i, question in enumerate(questions):
        if (i + 1) % 100 == 0 or i == 0 or i == len(questions) - 1:
            print(f"    Processing {i + 1}/{len(questions)}: {question['question_id']}")

        create_environment(question, env_dir)

        qtype = question["question_type"]
        question_types[qtype] = question_types.get(qtype, 0) + 1

    print("  Creating evaluation file...")
    create_evaluation_file(questions, variant, env_dir.parent)

    print(f"  Done! Created {len(questions)} environments")
    print("  Question types:")
    for qtype, count in sorted(question_types.items()):
        print(f"    {qtype}: {count}")


def setup_variant(variant: str, data_dir: Path, force: bool = False):
    """Download and set up a single variant."""
    print(f"\n{'='*60}")
    print(f"Setting up {variant.upper()} variant")
    print(f"  Sessions per question: {VARIANTS[variant]['sessions']}")
    print(f"  Download size: {VARIANTS[variant]['size']}")
    print(f"{'='*60}")

    variant_dir = data_dir / variant
    json_path = variant_dir / VARIANTS[variant]["filename"]
    env_dir = variant_dir / "environments"

    # Check if already exists
    if json_path.exists() and env_dir.exists() and not force:
        print(f"  Already set up (use --force to regenerate)")
        return True

    # Download if needed
    if not json_path.exists() or force:
        url = f"{HUGGINGFACE_BASE}/{VARIANTS[variant]['filename']}"
        print(f"\nDownloading {variant} data...")
        if not download_file(url, json_path):
            print(f"  Failed to download {variant}")
            return False
    else:
        print(f"\n  Using existing JSON: {json_path}")

    # Convert to environments
    print(f"\nConverting to environments...")
    convert_to_environments(json_path, env_dir, variant)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Download and set up LME+ evaluation data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--variant", "-v",
        choices=["small", "medium", "oracle", "all"],
        default="all",
        help="Which variant to set up (default: all)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force re-download and regeneration"
    )
    parser.add_argument(
        "--data-dir", "-d",
        type=Path,
        default=None,
        help="Data directory (default: data/lme_plus relative to script)"
    )

    args = parser.parse_args()

    # Determine data directory
    if args.data_dir:
        data_dir = args.data_dir
    else:
        script_dir = Path(__file__).parent
        data_dir = script_dir.parent / "data" / "lme_plus"

    print(f"LME+ Data Setup")
    print(f"Data directory: {data_dir}")

    # Set up requested variants
    variants = list(VARIANTS.keys()) if args.variant == "all" else [args.variant]

    success = True
    for variant in variants:
        if not setup_variant(variant, data_dir, args.force):
            success = False

    if success:
        print(f"\n{'='*60}")
        print("Setup complete!")
        print(f"{'='*60}")
        print(f"\nData structure:")
        print(f"  {data_dir}/")
        for v in variants:
            print(f"    {v}/")
            print(f"      {VARIANTS[v]['filename']}")
            print(f"      environments/  (500 question folders)")
            print(f"      evaluation/    (questions + answers)")
    else:
        print("\nSetup completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
