# LME+: Do Memory Tools Help Agents?

**Core Question:** Do memory tools actually help agents, or is a filesystem all you need?

## The Gap

Memory systems are evaluated on static retrieval benchmarks, but agents use memory dynamically. We don't know:
1. Do static retrieval gains translate to agentic gains?
2. How do MCP tools vs filesystem vs compression compare when retrieval is agentic?
3. What's the cost/latency tax of agenticity?

## Hypotheses

### H1: Translation (Primary)
> Agentic retrieval (LME+) will achieve QA accuracy within 5% of static retrieval (LME best = 72%), but at 2-3x higher latency/cost.

| Criterion | Threshold |
|-----------|-----------|
| Success | LME+ accuracy ≥ 67% |
| Failure | LME+ accuracy < 67% OR cost > 5x static |

### H2: Method Ranking
> Simple filesystem access will outperform specialized MCP memory tools in agentic contexts.

Based on [Letta's finding](https://www.letta.com/blog/benchmarking-ai-agent-memory): filesystem (74%) beats specialized tools on LoCoMo.

### H3: Retrieval Gating
> Memory tool effectiveness is modulated by retrieval quality—tools provide no benefit when retrieval fails (Recall@10 = 0) or succeeds excellently (Recall@10 > 0.8).

---

## Experiment Design

### Memory Methods Under Test

| ID | Method | Memory | Filesystem | Compression |
|----|--------|--------|------------|-------------|
| A | Built-in MCP | ✅ | ❌ | ❌ |
| B | Stella v5 MCP | ✅ | ❌ | ❌ |
| C | MCP + Filesystem | ✅ | ✅ | ❌ |
| D | Filesystem only | ❌ | ✅ | ❌ |
| E | Compression | ❌ | ❌ | ✅ |
| O | Oracle | Gold | ❌ | ❌ |

### LME Baselines (Static Retrieval)

| Config | QA@5 | QA@10 | Notes |
|--------|------|-------|-------|
| Stella V5, K=V | 0.615 | 0.670 | baseline |
| Stella V5, K=V+fact | 0.657 | **0.720** | best round |
| Session, K=V+fact | **0.714** | 0.700 | best overall |

**Target to beat:** 72% (best static config)

---

## Results

### Table 1: Method Comparison

| ID | Method | QA Score | Time (s) | Tokens | Cost | vs LME |
|----|--------|----------|----------|--------|------|--------|
| A | Built-in MCP | — | — | — | — | — |
| B | Stella v5 MCP | — | — | — | — | — |
| C | MCP + Filesystem | — | — | — | — | — |
| D | Filesystem only | — | — | — | — | — |
| E | Compression | — | — | — | — | — |
| O | Oracle | — | — | — | — | — |

### Table 2: Retrieval-Gated Analysis

| Stratum | Recall@10 | LME Score | LME+ Score | Δ |
|---------|-----------|-----------|------------|---|
| Failed | 0.0 | — | — | — |
| Partial | (0, 0.5] | — | — | — |
| Good | (0.5, 0.8] | — | — | — |
| Excellent | > 0.8 | — | — | — |

### Table 3: Translation Analysis

| Condition | Count | % |
|-----------|-------|---|
| ✅ Translated (retrieval ↑, agent ↑) | — | — |
| ❌ No translation (retrieval ↑, agent ≈) | — | — |
| ⚠️ Negative (retrieval ↑, agent ↓) | — | — |

---

## Method

### LME+ Benchmark
Converts LongMemEval from static retrieval to agentic retrieval:
- **LME:** Single query → top-k → answer
- **LME+:** Agent issues queries, reformulates, iterates → answer

### Agent Architecture
ReAct agent with tools for memory queries and/or filesystem access.

### Evaluation
- 500 questions from LongMemEval_S
- LLM judge (GPT-4o) for answer correctness
- Log: accuracy, time, tokens, cost per sample

---

## Resources

| Item | Details |
|------|---------|
| Dataset | [LongMemEval](https://github.com/xiaowu0162/LongMemEval) |
| Hardware | MacBook Pro M4 Max, 64GB |
| Initial Budget | $10 |
| Validation Set | 20 questions |
| Priority Methods | Filesystem, Built-in MCP, Oracle |

## References

- [LongMemEval paper](https://arxiv.org/abs/2410.10813)
- [Letta Memory Benchmark](https://www.letta.com/blog/benchmarking-ai-agent-memory)
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)
