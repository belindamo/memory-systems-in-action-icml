#!/usr/bin/env python3
"""
LME+ Evaluation: Agentic Memory Retrieval Benchmark
"""
import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

from agent import ReActAgent
from adapters.oracle import OracleAdapter
from adapters.filesystem import FilesystemAdapter
from adapters.builtin_mcp import BuiltinMCPAdapter
from adapters.stella_v5 import StellaV5Adapter
from adapters.hybrid import HybridAdapter
from adapters.bm25 import BM25Adapter
from adapters.bge import BGEAdapter
from adapters.mcp_filesystem import MCPFilesystemAdapter
from adapters.reranker import RerankerAdapter
from judge import LLMJudge


def load_questions(data_dir: Path, sample_ids=None, samples=None):
    """Load evaluation questions"""
    questions_file = data_dir / "evaluation" / "lme_s_questions.json"
    with open(questions_file) as f:
        questions = json.load(f)

    # Filter out questions without environment directories
    env_dir = data_dir / "environments"
    questions = [q for q in questions if (env_dir / q['question_id']).exists()]

    # Filter by specific IDs if provided
    if sample_ids:
        id_set = set(sample_ids.split(','))
        questions = [q for q in questions if q['question_id'] in id_set]

    # Limit to N samples if specified
    if samples:
        questions = questions[:samples]

    return questions


def create_adapter(memory_type: str, data_dir: Path, filesystem: bool):
    """Create memory adapter based on type"""
    if memory_type == "oracle":
        return OracleAdapter(data_dir)
    elif memory_type == "filesystem":
        return FilesystemAdapter(data_dir)
    elif memory_type == "builtin_mcp":
        return BuiltinMCPAdapter(data_dir, enable_filesystem=filesystem)
    elif memory_type == "stella_v5":
        return StellaV5Adapter(data_dir)
    elif memory_type == "hybrid":
        return HybridAdapter(data_dir)
    elif memory_type == "bm25":
        return BM25Adapter(data_dir)
    elif memory_type == "bge":
        return BGEAdapter(data_dir)
    elif memory_type == "mcp_filesystem":
        return MCPFilesystemAdapter(data_dir)
    elif memory_type == "reranker":
        return RerankerAdapter(data_dir)
    else:
        raise ValueError(f"Unknown memory type: {memory_type}")


def run_evaluation(args):
    """Run evaluation on specified memory system"""
    data_dir = Path(args.data)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load questions
    questions = load_questions(data_dir, args.sample_ids, args.samples)
    print(f"Loaded {len(questions)} questions")

    # Create adapter and agent
    adapter = create_adapter(args.memory, data_dir, args.filesystem)
    agent = ReActAgent(
        adapter=adapter,
        model=args.model,
        max_iterations=args.max_iterations
    )

    # Create judge
    judge = LLMJudge(model=args.judge_model)

    # Run evaluation
    results = []
    for i, question_data in enumerate(questions):
        print(f"\n[{i+1}/{len(questions)}] Question: {question_data['question_id']}")

        question_id = question_data['question_id']
        question = question_data['question']
        gold_answer = question_data['answer']

        # Set up environment for this question
        env_dir = data_dir / "environments" / question_id
        adapter.set_environment(env_dir)

        # Run agent
        start_time = time.time()
        agent_answer, trace = agent.run(question)
        elapsed_time = time.time() - start_time

        # Judge answer
        is_correct = judge.evaluate(question, agent_answer, gold_answer)

        # Collect metrics
        result = {
            "question_id": question_id,
            "question": question,
            "gold_answer": gold_answer,
            "agent_answer": agent_answer,
            "correct": is_correct,
            "time_seconds": elapsed_time,
            "tokens": trace["total_tokens"],
            "cost_usd": trace["total_cost"],
            "tool_calls": trace["tool_calls"],
            "iterations": trace["iterations"]
        }
        results.append(result)

        print(f"  Answer: {agent_answer}")
        print(f"  Correct: {is_correct}")
        print(f"  Time: {elapsed_time:.1f}s, Tokens: {trace['total_tokens']}, Cost: ${trace['total_cost']:.4f}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = output_dir / f"results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Calculate summary statistics
    summary = {
        "memory_type": args.memory,
        "filesystem_enabled": args.filesystem,
        "num_questions": len(results),
        "accuracy": sum(r["correct"] for r in results) / len(results),
        "avg_time_seconds": sum(r["time_seconds"] for r in results) / len(results),
        "avg_tokens": sum(r["tokens"] for r in results) / len(results),
        "total_cost_usd": sum(r["cost_usd"] for r in results),
        "avg_iterations": sum(r["iterations"] for r in results) / len(results),
        "timestamp": timestamp
    }

    summary_file = output_dir / f"summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Results saved to {results_file}")
    print(f"Summary: Accuracy={summary['accuracy']:.2%}, Cost=${summary['total_cost_usd']:.2f}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="LME+ Evaluation")
    parser.add_argument("--memory", "-m", required=True,
                        choices=["oracle", "filesystem", "builtin_mcp", "stella_v5", "hybrid", "bm25", "bge", "mcp_filesystem", "reranker"],
                        help="Memory system to use")
    parser.add_argument("--samples", "-n", type=int, default=50,
                        help="Number of samples to run")
    parser.add_argument("--sample-ids", type=str,
                        help="Comma-separated specific sample IDs")
    parser.add_argument("--output", "-o", default="results/eval",
                        help="Output directory")
    parser.add_argument("--data", "-d", default="data/lme_plus",
                        help="LME+ data directory")
    parser.add_argument("--filesystem", "-f", action="store_true",
                        help="Enable filesystem tools")
    parser.add_argument("--model", default="gpt-4o",
                        help="Agent model")
    parser.add_argument("--judge-model", default="gpt-4o",
                        help="Judge model")
    parser.add_argument("--max-iterations", type=int, default=5,
                        help="Max ReAct iterations")

    args = parser.parse_args()

    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")

    run_evaluation(args)


if __name__ == "__main__":
    main()
