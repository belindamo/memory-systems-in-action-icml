#!/usr/bin/env python3
"""
Experiment: BM25 + Cross-Encoder Reranker (100 questions)

Hypothesis: Two-stage retrieval (BM25 -> cross-encoder reranker) will improve
precision over BM25 alone by using neural scoring for final ranking.

This addresses ICML reviewer concern about missing reranker baseline.

Pipeline:
1. BM25 retrieves top-20 candidates (fast, high recall)
2. Cross-encoder reranks to top-3 (accurate, high precision)

Model: cross-encoder/ms-marco-MiniLM-L-6-v2 (MS-MARCO trained)

Run: cd lme-plus && python experiments/node_17_reranker_100.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "reranker",
        "--samples", "100",
        "--output", "results/node_17_reranker_100",
        "--data", "data/lme_plus"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd="/Users/bmo/make-co-scientist-skill/memory-systems-in-action/lme-plus")
