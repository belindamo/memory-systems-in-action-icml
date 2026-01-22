# LME+ Evaluation

## Architecture

All evaluations use the **same ReAct agent** with different memory adapters:

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                   (unified entry point)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      ReAct Agent                             │
│            (OpenAI function calling loop)                    │
│                                                              │
│   Tools: search_memory [+ optional filesystem tools]         │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │  Oracle  │       │ Stella   │       │ Compress │
    │ Adapter  │       │ V5       │       │ Adapter  │
    │          │       │ Adapter  │       │          │
    │ (gold)   │       │ (dense)  │       │ (window) │
    └──────────┘       └──────────┘       └──────────┘
```

---

## Data Setup

The benchmark uses [LongMemEval](https://github.com/xiaowu0162/LongMemEval) with three variants:

| Variant | Sessions/env | Download Size | Description |
|---------|-------------|---------------|-------------|
| **Small** | ~40 | 265MB | Moderate context (~115k tokens) |
| **Medium** | ~500 | 2.5GB | Hard needle-in-haystack (~1.2M tokens) |
| **Oracle** | 1-5 | 15MB | Gold evidence only (no retrieval challenge) |

### Quick Setup

Run the setup script to download data and generate environments:

```bash
# From lme-plus/ directory
python scripts/setup_data.py                    # Set up all variants
python scripts/setup_data.py --variant small    # Set up only small (fastest)
python scripts/setup_data.py --variant oracle   # Set up only oracle
python scripts/setup_data.py --force            # Force re-download
```

This downloads from HuggingFace and creates:
```
data/lme_plus/{small,medium,oracle}/
├── longmemeval_*.json              # Source data
├── environments/                    # 500 question folders
│   └── <question_id>/
│       ├── chat_history/session_XXXX.json
│       ├── chat_turns/turn_XXXXXX.json
│       ├── metadata.json
│       └── README.md
└── evaluation/lme_*_questions.json  # Questions + answers
```

---

## Quick Start

```bash
export OPENAI_API_KEY=<your-key>
```

---

## Table 1 Commands

### Row O: Oracle (Perfect Retrieval)
ReAct agent with oracle adapter that returns gold evidence.

```bash
PYTHONPATH=code uv run python code/main.py \
  --memory oracle \
  --samples 50 \
  --output results/row_O_oracle
```

---

### Row A: Built-in Memory MCP
```bash
PYTHONPATH=code uv run python code/main.py \
  --memory builtin_mcp \
  --samples 50 \
  --output results/row_A_builtin_mcp
```

---

### Row B: Stella V5 (Memory MCP-2)
```bash
PYTHONPATH=code uv run python code/main.py \
  --memory stella_v5 \
  --samples 50 \
  --output results/row_B_stella_v5
```

---

### Row C: Built-in MCP + Filesystem
```bash
PYTHONPATH=code uv run python code/main.py \
  --memory builtin_mcp \
  --filesystem \
  --samples 50 \
  --output results/row_C_builtin_mcp_fs
```

---

### Row D: Stella V5 + Filesystem
```bash
PYTHONPATH=code uv run python code/main.py \
  --memory stella_v5 \
  --filesystem \
  --samples 50 \
  --output results/row_D_stella_v5_fs
```

---

### Row E: Compression (Sliding Window)
```bash
PYTHONPATH=code uv run python code/main.py \
  --memory compression \
  --compression-method sliding_window \
  --samples 50 \
  --output results/row_E_compression_sliding
```

---

### Row F: Compression (Extractive)
```bash
PYTHONPATH=code uv run python code/main.py \
  --memory compression \
  --compression-method extractive \
  --samples 50 \
  --output results/row_F_compression_extractive
```

---

## CLI Options

```
usage: main.py [-h] --memory {oracle,builtin_mcp,stella_v5,bm25,contriever,hipporag,compression}
               [--samples N] [--sample-ids IDS] [--output DIR] [--data DIR]
               [--filesystem] [--model MODEL] [--judge-model MODEL]
               [--max-iterations N] [--device DEVICE] [--batch-size N]
               [--compression-method {sliding_window,extractive}]

Options:
  --memory, -m       Memory system to use (required)
  --samples, -n      Number of samples to run (default: 50)
  --sample-ids       Comma-separated specific sample IDs
  --output, -o       Output directory (default: results/eval)
  --data, -d         LME+ data directory (default: data/lme_plus)
  --filesystem, -f   Enable filesystem tools
  --model            Agent model (default: gpt-4o)
  --judge-model      Judge model (default: gpt-4o)
  --max-iterations   Max ReAct iterations (default: 5)
```

---

## Memory Systems

| Adapter | Description | Table 1 Row |
|---------|-------------|-------------|
| `oracle` | Returns gold evidence (perfect retrieval) | O |
| `builtin_mcp` | Built-in MCP keyword search | A, C |
| `stella_v5` | Stella V5 1.5B dense retrieval | B, D |
| `bm25` | BM25 sparse retrieval | - |
| `contriever` | Contriever dense retrieval | - |
| `hipporag` | HippoRAG knowledge graph | - |
| `compression` | Context compression | E, F |

---

## Run Specific Samples

```bash
# Run only specific question IDs
PYTHONPATH=code uv run python code/main.py \
  --memory oracle \
  --sample-ids "q001,q002,q003" \
  --output results/test
```

---

## Output Structure

```
results/row_X/
├── results_<timestamp>.json   # Full per-question results
└── summary_<timestamp>.json   # Aggregated metrics
```

---

## Notes

- **All rows use the same ReAct agent** - only the memory adapter changes
- **Oracle (Row O)** now uses the ReAct loop with perfect retrieval, not direct LLM
- **Filesystem flag** enables additional tools for Row C/D (TODO: implement)
- LME-S = 50 samples, Full LME = 500 samples
