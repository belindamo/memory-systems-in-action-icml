#!/usr/bin/env python3
"""
Experiment Node 1: Oracle Baseline
Tests upper bound performance with perfect retrieval
"""
import subprocess
import sys

def run():
    """Run Oracle experiment on 20 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "oracle",
        "--samples", "20",
        "--output", "results/node_1_oracle_baseline"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
