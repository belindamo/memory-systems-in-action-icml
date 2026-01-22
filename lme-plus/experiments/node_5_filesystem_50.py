#!/usr/bin/env python3
"""
Experiment Node 5: Filesystem (50 samples)
Validate that filesystem underperformance holds at scale
"""
import subprocess
import sys

def run():
    """Run Filesystem experiment on 50 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "filesystem",
        "--samples", "50",
        "--output", "results/node_5_filesystem_50"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
