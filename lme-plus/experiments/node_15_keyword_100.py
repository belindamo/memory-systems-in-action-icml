#!/usr/bin/env python3
"""
Experiment: Keyword (frequency) at 100 questions

Scale up the original keyword experiment to 100 questions for fair comparison
with BM25 and other new methods.

Run: cd lme-plus && python experiments/node_15_keyword_100.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "builtin_mcp",
        "--samples", "100",
        "--output", "results/node_15_keyword_100",
        "--data", "data/lme_plus"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd="/Users/bmo/make-co-scientist-skill/memory-systems-in-action/lme-plus")
