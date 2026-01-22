#!/usr/bin/env python3
"""
Experiment Node 4: Oracle Baseline (50 samples)
Scale up to validate 80% accuracy pattern holds
"""
import subprocess
import sys

def run():
    """Run Oracle experiment on 50 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "oracle",
        "--samples", "50",
        "--output", "results/node_4_oracle_50"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
