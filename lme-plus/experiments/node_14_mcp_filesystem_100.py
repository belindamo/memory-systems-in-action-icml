#!/usr/bin/env python3
"""
Experiment: MCP Filesystem Tools (100 questions)

Hypothesis: Proper MCP-style filesystem tools (list, read, grep, search) will
outperform the original simple filesystem adapter due to better tool design
matching what agents are trained on.

Run: cd lme-plus && python experiments/node_14_mcp_filesystem_100.py
"""
import subprocess
import sys

if __name__ == "__main__":
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "mcp_filesystem",
        "--samples", "100",
        "--output", "results/node_14_mcp_filesystem_100",
        "--data", "data/lme_plus"
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd="/Users/bmo/make-co-scientist-skill/memory-systems-in-action/lme-plus")
