#!/usr/bin/env python3
"""
Experiment Node 3: Built-in MCP
Tests keyword-based memory search tool
"""
import subprocess
import sys

def run():
    """Run Built-in MCP experiment on 20 validation samples"""
    cmd = [
        sys.executable, "code/main.py",
        "--memory", "builtin_mcp",
        "--samples", "20",
        "--output", "results/node_3_builtin_mcp"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode

if __name__ == "__main__":
    sys.exit(run())
