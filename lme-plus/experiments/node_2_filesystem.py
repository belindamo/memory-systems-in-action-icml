#!/usr/bin/env python3
"""
Experiment Node 2: Filesystem Access
Tests H2: Simple filesystem access outperforms specialized memory tools
"""
import subprocess
import sys

def run():
    """Run Filesystem experiment on 20 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "filesystem",
        "--samples", "20",
        "--output", "results/node_2_filesystem"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
