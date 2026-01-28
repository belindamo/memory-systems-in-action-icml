#!/usr/bin/env python3
"""
Experiment: Oracle at 100 questions

Scale up Oracle to 100 questions to establish upper bound at larger scale.

Run: cd lme-plus && python experiments/node_16_oracle_100.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "oracle",
        "--samples", "100",
        "--output", "results/node_16_oracle_100",
        "--data", "data/lme_plus"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd="/Users/bmo/make-co-scientist-skill/memory-systems-in-action/lme-plus")
