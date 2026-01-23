#!/usr/bin/env python3
"""
Experiment Node 10: Stella V5 Dense Retrieval (50 samples)
Test whether dense embeddings beat keyword search
"""
import subprocess
import sys

def run():
    """Run Stella V5 experiment on 50 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "stella_v5",
        "--samples", "50",
        "--output", "results/node_10_stella_v5_50"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
