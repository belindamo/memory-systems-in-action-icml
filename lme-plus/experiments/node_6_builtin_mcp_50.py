#!/usr/bin/env python3
"""
Experiment Node 6: Built-in MCP (50 samples)
Validate that MCP 70% pattern holds at scale
"""
import subprocess
import sys

def run():
    """Run Built-in MCP experiment on 50 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "builtin_mcp",
        "--samples", "50",
        "--output", "results/node_6_builtin_mcp_50"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
