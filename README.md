# LME+ Memory Systems Overview

## Experiments: What This Lets You Say (Cleanly)

- Whether retrieval improvements correlate with agent gains
- Where gains fail to transfer
- The latency / cost tax of agenticity
- Retrieval vs. memory: Whether memory helps only after retrieval is solved
- How results vary based on 3 different memory methods: tools, compression, or filesystem


---

### Table 1 — Agent Memory / Storage Comparison (Sample-Averaged)

| ID | Agent Variant | Retrieval / Memory | File System | Compression | Avg Time (s) | Avg Tokens | Avg Cost | Avg Judge Score | Notes |
|----|---------------|-------------------|-------------|-------------|--------------|------------|----------|-----------------|-------|
| A  | ReAct | Built-in Memory MCP | ❌ | ❌ | | | | | baseline |
| B  | ReAct | Memory MCP-2 | ❌ | ❌ | | | | | |
| C  | ReAct | Built-in Memory MCP | ✅ | ❌ | | | | | |
| D  | ReAct | Memory MCP-2| ✅ | ❌ | | | | | |
| E  | ReAct | ❌ | ❌ | Compression v1 | | | | | |
| F  | ReAct | ❌ | ❌ | Compression v2 | | | | | |
| O  | ReAct (Oracle) | Gold answer after 1 query | ❌ | ❌ | ~min | ~min | ~min | max | judge sanity check |

Memory MCP-2 is Stella v5, Round-based, K=V+fact

---

### Table 2 — Chat-to-Agentic Translation Comparison for End-to-End QA: LME vs LME+ (Core Claim)

*Comparing static retrieval (LME) vs agentic retrieval (LME+) on the same task.*
*All scores are **end-to-end QA accuracy** with GPT-4o as reader/actor.*

#### LME Published Baselines (Static Retrieval, from paper Table 10)

| ID | Config | Value | Key Design | QA@5 | QA@10 | Notes |
|----|--------|-------|------------|------|-------|-------|
| L1 | Stella V5 | Round | K = V | 0.615 | **0.670** | baseline |
| L2 | Stella V5 | Round | K = V + fact | 0.657 | **0.720** | best round config |
| L3 | Stella V5 | Session | K = V | 0.670 | 0.676 | session baseline |
| L4 | Stella V5 | Session | K = V + fact | **0.714** | 0.700 | best overall |

#### LME+ Agentic Variants (Maps to Table 1)

| ID | Table 1 Row | Memory System | Agentic | QA Score | Time (s) | Tokens | Cost |
|----|-------------|---------------|---------|----------|----------|--------|------|
| A | A | Built-in Memory MCP | ✅ | — | — | — | — |
| B | B | Memory MCP-2 | ✅ | — | — | — | — |
| C | C | Built-in MCP + Filesystem | ✅ | — | — | — | — |
| D | D | Memory MCP-2 + Filesystem | ✅ | — | — | — | — |
| O | O | Oracle (perfect retrieval if MCP is called) | ✅ | — | — | — | — |

**Method Definitions:**
- **LME (L1–L4):** Static retrieval → read → answer. No iteration. QA@5/QA@10 = accuracy when given top-5 or top-10 retrieved items.
- **LME+ (A–D):** Agentic memory with **dynamic retrieval** — agent issues queries, refines searches, reads from memory.
- **O (Oracle):** Gold evidence provided directly — upper bound.

**Key Question:** Does agentic retrieval (LME+) match or beat LME's best static config (L4 = 0.714)?

---

### Table 3 — Per-Sample Translation Analysis (Key Evidence Table)

**This is the proof table.**

| Sample ID | Δ Retrieval (R2−R1) | Δ Judge Score (R2−R1) | Δ Time | Δ Tokens | Δ Cost | Translation? |
|-----------|---------------------|----------------------|--------|----------|--------|--------------|
| s₁ | | | | | | |
| s₂ | | | | | | |
| … | | | | | | |

#### Interpretation Rule

| Condition | Meaning |
|-----------|---------|
| ✅ Translation | Δretrieval ↑ **and** Δagent score ↑ |
| ❌ No translation | Δretrieval ↑ **but** Δagent score ≈ 0 |
| ⚠️ Negative | Δretrieval ↑ **but** agent worsens (overhead / misuse) |

---

### Table 4 — Retrieval-Gated Stratification (Based on LME Recall@10)

**Stratify samples by LME retrieval quality, then compare LME vs LME+ scores.**

| Stratum | Recall@10 Range | NDCG@10 Range | LME Score | LME+ Score | Δ | Takeaway |
|---------|-----------------|---------------|-----------|------------|---|----------|
| **Failed** | 0.0 | any | | | | retrieval bottleneck — gold evidence not retrieved |
| **Partial** | (0, 0.5] | < 0.4 | | | | partial retrieval — some evidence, low rank |
| **Good** | (0.5, 0.8] | 0.4–0.6 | | | | decent retrieval — agent quality matters |
| **Excellent** | > 0.8 | > 0.6 | | | | agent bottleneck — retrieval solved, agent fumbles |

**LME Reference Scores** (Stella V5 1.5B, Value=Round, K=V+fact):
- Recall@10: **0.784**, NDCG@10: **0.536**
- GPT-4o End-to-End QA (Top-10): **72.0%**

**Error Distribution** (from LME paper):
- 15–19% of errors: correct retrieval but wrong generation → **agent bottleneck**
- ~90% of correct answers required correct retrieval → **retrieval is necessary**

---

### Table 5 — BrowseComp Results (Dynamic Memory Add + Retrieve)

*BrowseComp tests a different paradigm: agent actively writes AND reads memories during the task.*

| ID | Memory System | Write Ops | Read Ops | QA Score | Time (s) | Tokens | Cost | Notes |
|----|---------------|-----------|----------|----------|----------|--------|------|-------|
| BC1 | Built-in MCP | ✅ | ✅ | — | — | — | — | |
| BC2 | Memory MCP-2 | ✅ | ✅ | — | — | — | — | |
| BC3 | Filesystem only | ✅ | ✅ | — | — | — | — | |
| BC4 | Hybrid (MCP + FS) | ✅ | ✅ | — | — | — | — | |

**Key Question:** Does letting the agent manage its own memory (add + retrieve) help vs. read-only retrieval?

---

### Table 6 — Benchmark Comparison: Memory Paradigms

*Progression from retrieval → end-to-end QA → agentic QA (based on LME paper structure)*

| Paradigm | Benchmark | Memory Ops | Agent | Metric | What It Tests |
|----------|-----------|------------|-------|--------|---------------|
| **Retrieval** | LME | Read (static) | ❌ | Recall@k, NDCG@k | Can we find the right evidence? |
| **End-to-End QA** | LME | Read (static) | ❌ | QA Accuracy | Can LLM answer given retrieved context? |
| **Agentic QA, Dynamic Retrieval** | LME+ | Read (dynamic) | ✅ | QA Accuracy | Does iterative search improve QA? |
| **Agentic QA, Dynamic Update + Retrieval** | BrowseComp | Read + Write | ✅ | QA Accuracy | Does memory management improve QA? |

#### Paradigm Differences

| Paradigm | Query Strategy | # Queries | Query Reformulation | Memory Read | Memory Write | Agent Loop |
|----------|----------------|-----------|---------------------|-------------|--------------|------------|
| **Retrieval (LME)** | Single | 1 | ❌ | Static top-k | ❌ | ❌ |
| **E2E QA (LME)** | Single | 1 | ❌ | Static top-k | ❌ | ❌ |
| **Agentic QA (LME+)** | Multiple | 1+ | ✅ Agent reformulates | Dynamic | ❌ | ✅ ReAct |
| **Agentic + Memory (BrowseComp)** | Multiple | 1+ | ✅ Agent reformulates | Dynamic | ✅ Agent writes | ✅ ReAct |

#### What Changes Between Paradigms

| Transition | What's Added | Key Question |
|------------|--------------|--------------|
| Retrieval → E2E QA | LLM reading step | Can LLM extract answer from context? |
| E2E QA → Agentic QA | **Multiple reformulated queries** | Does query refinement find better evidence? |
| Agentic QA → BrowseComp | **Agent-controlled memory writes** | Does storing intermediate results help? |

#### Example Query Patterns

| Paradigm | Query Flow |
|----------|------------|
| **LME** | `"What restaurant did I mention?"` → top-10 → answer |
| **LME+** | `"restaurant"` → partial results → `"restaurant recommendation last week"` → better results → answer |
| **BrowseComp** | Browse → store `{user likes Italian}` → later query `"Italian restaurants"` → retrieve stored fact → answer |

#### Key Insight

```
LME Retrieval     → Single query, retrieval quality
LME E2E QA        → Single query, reading quality  
LME+ Agentic QA   → Multiple queries, query refinement quality
BrowseComp        → Multiple queries + memory management quality
```

**The Core Question:** Does letting the agent reformulate queries (LME+) or manage memory (BrowseComp) improve over single-query retrieval?

### Table 7 - Memory Comparisons

- Tool-based
- Filesystem-based
- In-context with compression

