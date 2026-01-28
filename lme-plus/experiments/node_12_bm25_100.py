#!/usr/bin/env python3
"""
Experiment: BM25 Retrieval (100 questions)

Hypothesis: Proper BM25 with IDF weighting will outperform simple frequency counting.
Tests whether the ICML review concern about "not real BM25" is valid.

Run: cd lme-plus && python experiments/node_12_bm25_100.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "bm25",
        "--samples", "100",
        "--output", "results/node_12_bm25_100",
        "--data", "data/lme_plus"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd="/Users/bmo/make-co-scientist-skill/memory-systems-in-action/lme-plus")
