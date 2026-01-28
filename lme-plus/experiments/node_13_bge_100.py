#!/usr/bin/env python3
"""
Experiment: BGE Embeddings (100 questions)

Hypothesis: BGE-large may perform differently than Stella V5 on conversational QA.
Tests whether the embedding model choice matters (ICML W2).

Run: cd lme-plus && python experiments/node_13_bge_100.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "bge",
        "--samples", "100",
        "--output", "results/node_13_bge_100",
        "--data", "data/lme_plus"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd="/Users/bmo/make-co-scientist-skill/memory-systems-in-action/lme-plus")
