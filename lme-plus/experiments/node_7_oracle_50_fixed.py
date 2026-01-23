#!/usr/bin/env python3
"""
Experiment Node 7: Oracle 50 (Fixed)
Rerun with bug fixes to validate results
"""
import subprocess
import sys

def run():
    """Run Oracle experiment with fixed formatting"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "oracle",
        "--samples", "50",
        "--output", "results/node_7_oracle_50_fixed"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
