# Memory Systems in Action: Evaluating SOTA Memory Systems on Agentic Tasks vs Needle-in-the-Haystack Tasks

## Problem

**Core Question:** Do memory tools actually help agents perform long-horizon tasks, and if so, what makes certain memory architectures more effective than others?

Prior work on agent memory systems has focused primarily on direct retrieval tasks—"needle-in-the-haystack" scenarios where the system retrieves a specific piece of information from a large corpus. However, real-world agent tasks involve **agentic retrieval**: agents must actively decide when to search memory, what queries to use, and how to synthesize retrieved information with task context. It remains unclear whether memory systems that excel at direct retrieval maintain their effectiveness when retrieval becomes an agentic subtask.

**The gap:** Three critical unknowns exist:

1. **Effectiveness:** Do memory MCP tools improve agent performance on long-horizon tasks compared to baselines (no memory, or raw filesystem access)? The direction and magnitude of this effect is unknown.

2. **Translation:** Do retrieval improvements from static benchmarks translate to agent gains? Performance rankings from direct retrieval benchmarks may not transfer when retrieval becomes an agentic subtask.

3. **Method comparison:** How do different memory approaches compare in agentic contexts—tool-based memory (MCP), filesystem-based storage, or in-context compression?

**Why this matters:** As LLM-based agents are deployed for increasingly complex tasks (research, coding, multi-hour web browsing), memory becomes a critical component. However, current memory tool development is driven by performance on retrieval benchmarks, not agentic benchmarks. This project will reveal:
- Whether retrieval improvements correlate with agent gains
- Where gains fail to transfer
- The latency/cost tax of agenticity
- Whether memory helps only after retrieval is solved

Importantly, if memory tools provide no benefit—or hurt performance—that would be a critical negative result invalidating current work on memory MCPs.

## Related Work

### Long-Term Memory Benchmarks
- **LongMemEval** (Wu et al., 2025): Comprehensive benchmark for chat assistant long-term memory, testing five core abilities: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. Contains 500 questions across three difficulty levels (S: ~115k tokens, M: ~1.5M tokens, Oracle). Commercial systems show 30% accuracy drop in sustained interactions. [ICLR 2025]
- **BrowseComp** (Wei et al., 2025): 1,266 questions requiring persistent web browsing to find hard-to-locate, entangled information. Tests agent persistence and creativity in information retrieval. [OpenAI]

### Memory Systems
- **Retrieval-based systems:** BM25 (sparse), Contriever, Stella V5 1.5B (dense embeddings)
- **MCP Memory Servers:** Built-in Memory MCP (Anthropic)
- **Context compression:** 

### Key Findings from Prior Work
- LongMemEval: Turn-level (round) granularity with fact-augmented keys achieves best results
- LongMemEval: Stella V5 1.5B with K=V+fact achieves QA@10 = 72.0% (best round config)
- LongMemEval: Session-level with K=V+fact achieves QA@5 = 71.4% (best overall)
- LongMemEval: Recall@10 = 0.784, NDCG@10 = 0.536 for best config
- LongMemEval: 15-19% of errors are correct retrieval but wrong generation (agent bottleneck)
- LongMemEval: ~90% of correct answers required correct retrieval (retrieval is necessary)

## Research Question(s)

**Primary Question:** How do memory MCP tools affect agent performance on long-horizon tasks, and what characteristics explain performance differences between memory architectures in agentic contexts?

**Sub-questions:**

1. **Translation:** Do retrieval improvements (from LME baselines) translate to agent gains (in LME+)? Where do gains fail to transfer?

2. **Method comparison:** How do three memory methods compare: tool-based (MCP), filesystem-based, and in-context compression?

3. **Effectiveness:** Do memory tools improve agent performance at all on long-horizon tasks compared to baselines (no memory, or filesystem access)?

4. **Ablation analysis:** What is the relative contribution of memory tools vs. filesystem access vs. both combined?

5. **Cost of agenticity:** What is the latency/cost tax of agentic retrieval compared to static retrieval?

6. **Retrieval gating:** Does memory help only after retrieval is solved? How do results vary by retrieval quality strata?

7. **Dynamic memory:** Does letting the agent manage its own memory (add + retrieve, as in BrowseComp) help vs. read-only retrieval?

**Hypotheses:**

**H1 (Translation):** Retrieval improvements from static benchmarks (LME) may not fully translate to agent gains (LME+). The key question: Does agentic retrieval match or beat LME's best static config (72.0% QA accuracy)?

**H2 (Agentic vs. Static):** Performance changes will occur when retrieval becomes agentic. The ability to reformulate queries may help or hurt depending on whether the agent can effectively refine searches.

**H3 (Method Patterns):** Different memory methods (tools, filesystem, compression) will show distinct performance patterns. These patterns may differ from expectations based on static retrieval benchmarks.

**H4 (Retrieval Gating):** Memory benefits will be modulated by retrieval quality. In the "Failed" stratum (Recall@10 = 0), memory tools cannot help. In the "Excellent" stratum (Recall@10 > 0.8), agent quality becomes the bottleneck.

**H5 (Dynamic Memory):** Agent-controlled memory writes (BrowseComp paradigm)  provide additional benefits over read-only retrieval for long-horizon tasks requiring intermediate state.

**H6 (Horizon Length):** Task horizon length will modulate the benefit of memory 
tools, with longer tasks potentially benefiting more from structured memory 
compared to shorter tasks. This is displayed in BrowseComp

## Method / Approach (high-level)

### Experimental Design

We introduce **LME+**, a novel agentic benchmark that converts LongMemEval from a direct retrieval task to an agentic task. In LongMemEval, the system retrieves relevant context and provides it directly to the model. In LME+, an agent must actively decide when to search, what to search for, and how to use retrieved information—mirroring real-world agent memory usage.

**Comparison framework (Table 1 — Agent Memory / Storage Comparison):**

| ID | Agent | Retrieval / Memory | File System | Compression | What it Tests |
|----|-------|-------------------|-------------|-------------|---------------|
| A  | ReAct | Built-in Memory MCP | ❌ | ❌ | baseline MCP |
| B  | ReAct | Memory MCP-2 (Stella v5) | ❌ | ❌ | SOTA retrieval as MCP |
| C  | ReAct | Built-in Memory MCP | ✅ | ❌ | MCP + filesystem |
| D  | ReAct | Memory MCP-2 | ✅ | ❌ | SOTA + filesystem |
| E  | ReAct | ❌ | ❌ | Compression v1 | in-context compression |
| F  | ReAct | ❌ | ❌ | Compression v2 | alternative compression |
| O  | ReAct | Oracle (gold after 1 query) | ❌ | ❌ | judge sanity check |

**Memory MCP-2:** Stella v5 1.5B, Round-based, K=V+fact (best round config from LME paper)

**LME Published Baselines (Static Retrieval, for comparison):**

| ID | Config | Value | Key Design | QA@5 | QA@10 | Notes |
|----|--------|-------|------------|------|-------|-------|
| L1 | Stella V5 | Round | K = V | 0.615 | 0.670 | baseline |
| L2 | Stella V5 | Round | K = V + fact | 0.657 | **0.720** | best round config |
| L3 | Stella V5 | Session | K = V | 0.670 | 0.676 | session baseline |
| L4 | Stella V5 | Session | K = V + fact | **0.714** | 0.700 | best overall |

**Key Question:** Does agentic retrieval (LME+) match or beat LME's best static config (L4 = 0.714)?

### Agent Architecture
Following ReAct (Yao et al., 2023), at each step the agent:
1. Receives observation (question + any retrieved context)
2. Reasons about what information is needed
3. Takes action (query memory tool, or answer)

### Evaluation Strategy
- Use identical questions from LongMemEval
- Same LLM judge methodology (GPT-5.2) for answer correctness
- Compare Recall@K for retrieval quality where applicable
- Analyze tool call patterns and efficiency

## Implementation (what is actually built)

### LME+ Benchmark Construction (M1 Deliverable)
**This is a critical first step that must be completed before evaluation can begin.**

LME+ converts LongMemEval from a retrieval benchmark to an **agentic benchmark** where agents must actively search for information.

1. **Environment-Per-Question Structure**

   For each of the 500 LongMemEval_S questions, create an isolated environment:
   ```
   lme_plus/
   ├── question_001/
   │   ├── README.md          # Explains what the chat history files contain
   │   ├── session_01.txt     # Chat messages from session 1
   │   ├── session_02.txt     # Chat messages from session 2
   │   └── ...
   ├── question_002/
   │   ├── README.md
   │   ├── session_01.txt
   │   └── ...
   ```

   Each environment is self-contained with:
   - Chat history stored as files (by session or turn)
   - README explaining the file structure
   - No direct context provided to agent - must search files or query memory

2. **Data Loading Pipeline**
   - Download and parse LongMemEval dataset (LME_S level) from https://github.com/xiaowu0162/LongMemEval
   - Extract chat history sessions and questions
   - Create 500 isolated environments
   - Validate data integrity

3. **Three Memory Methods**
   The LME+ benchmark compares three approaches to memory:
   - **Tool-based (Memory MCP)**: Conversations ingested into memory system, agent queries via MCP tools
   - **Filesystem-based**: Conversations stored as files, agent searches files directly
   - **In-context compression**: Conversations compressed and provided in context (no external tools)

   This allows testing which memory method works best for agentic retrieval.

4. **Memory Ingestion**
   - For memory-based modes: ingest chat history from files into memory systems at turn-level granularity
   - Test both approaches: pre-processing (all at once) vs. tool-calling (during execution)

5. **Agent-Memory Integration**
   - Agent receives only the question (no context provided directly)
   - Agent must navigate environment to find relevant information using:
     - File system tools (read files, search)
     - Memory query tools
     - Or both
   - Agent generates final answer based on retrieved context

### Components to Build

1. **LME+ Benchmark Infrastructure** (M1 priority)
   - Data loading and preprocessing pipeline
   - Evaluation harness that runs agents on tasks
   - Result collection and storage system

2. **Memory system adapters:** Unified interface for each memory system
   - `ingest(sessions)` - load chat history
   - `search(query)` - retrieve relevant context
   - `reset()` - clear for next experiment

3. **ReAct agent:** LangChain-based or custom implementation
   - Tool: `search_memory(query)` → returns relevant turns/sessions
   - Tool (ablation): `search_files(query)` → filesystem search

4. **Evaluation pipeline:**
   - Run agent on LME+ questions
   - Log all tool calls, tokens, latency
   - Score answers with LLM judge (GPT-5.2)

5. **Analysis scripts:**
   - Compare LME vs LME+ performance per memory system
   - Analyze retrieval patterns and failure modes

### Repository Structure
```
memory-systems-in-action/
├── src/
│   ├── memory_adapters/      # Unified interface for each system
│   ├── agents/               # ReAct agent implementation
│   ├── evaluation/           # LLM judge, metrics
│   └── benchmarks/           # LME+ data loading
├── experiments/
│   ├── configs/              # Experiment configurations
│   └── scripts/              # Run scripts
├── results/                  # Experiment outputs
└── analysis/                 # Notebooks for analysis
```

## Evaluation (benchmarks + metrics)

### Benchmarks & Memory Paradigms

| Paradigm | Benchmark | Memory Ops | Agent | Metric | What It Tests |
|----------|-----------|------------|-------|--------|---------------|
| **Retrieval** | LME | Read (static) | ❌ | Recall@k, NDCG@k | Can we find the right evidence? |
| **End-to-End QA** | LME | Read (static) | ❌ | QA Accuracy | Can LLM answer given retrieved context? |
| **Agentic QA** | LME+ | Read (dynamic) | ✅ | QA Accuracy | Does iterative search improve QA? |
| **Agentic + Memory Writes** | BrowseComp | Read + Write | ✅ | QA Accuracy | Does memory management improve QA? |

**Paradigm Differences:**

| Paradigm | Query Strategy | # Queries | Query Reformulation | Memory Write | Agent Loop |
|----------|----------------|-----------|---------------------|--------------|------------|
| **Retrieval (LME)** | Single | 1 | ❌ | ❌ | ❌ |
| **E2E QA (LME)** | Single | 1 | ❌ | ❌ | ❌ |
| **Agentic QA (LME+)** | Multiple | 1+ | ✅ Agent reformulates | ❌ | ✅ ReAct |
| **Agentic + Memory (BrowseComp)** | Multiple | 1+ | ✅ Agent reformulates | ✅ Agent writes | ✅ ReAct |

**Benchmark Details:**

- **LongMemEval_S:** 500 tasks, ~115k tokens/task, 7 question types
  - Dataset: https://github.com/xiaowu0162/LongMemEval
- **LME+:** Same 500 tasks, agentic retrieval with three memory methods
- **BrowseComp:** 1,266 web browsing tasks with dynamic memory add + retrieve
  - Dataset: https://github.com/openai/simple-evals
  - Key difference: agent actively writes AND reads memories during the task

### Metrics
| Metric | Description | Source |
|--------|-------------|--------|
| Accuracy | Answer correctness via LLM judge | LME methodology |
| Recall@K | Retrieval quality (where applicable) | LME methodology |
| Tool calls | Number of memory queries per task | Logged |
| Tokens | Total tokens consumed | Logged |
| Latency | Time per task | Logged |
| Cost | API cost per task | Calculated |

### Analysis Approach

The analysis combines quantitative performance metrics with stratified analysis to identify when and how memory tools help (or hurt) in agentic contexts:

1. **Translation Analysis (Table 3):** Per-sample comparison of retrieval gains vs. agent gains:
   - ✅ Translation: Δretrieval ↑ **and** Δagent score ↑
   - ❌ No translation: Δretrieval ↑ **but** Δagent score ≈ 0
   - ⚠️ Negative: Δretrieval ↑ **but** agent worsens (overhead/misuse)

2. **Retrieval-Gated Stratification (Table 4):** Stratify samples by LME retrieval quality, then compare LME vs LME+ scores:
   - **Failed** (Recall@10 = 0): retrieval bottleneck — gold evidence not retrieved
   - **Partial** (Recall@10 ∈ (0, 0.5]): partial retrieval — some evidence, low rank
   - **Good** (Recall@10 ∈ (0.5, 0.8]): decent retrieval — agent quality matters
   - **Excellent** (Recall@10 > 0.8): agent bottleneck — retrieval solved, agent fumbles

3. **Method Comparison:** Compare tool-based, filesystem-based, and compression-based approaches across all metrics.

4. **Cost Analysis:** Document the latency/cost tax of agenticity (time, tokens, API cost per task).

5. **Negative Results:** Document cases where memory tools provide no benefit or hurt performance—these findings are equally important.

6. **Cross-Benchmark Validation:** Test whether patterns identified on LME+ generalize to BrowseComp (dynamic memory add + retrieve paradigm).

### Statistical Approach
- Report mean ± standard deviation (with multiple runs in later milestones)
- Paired comparisons where appropriate
- Standard ML paper practices for significance

## Implementation Timeline


1. **Phase 1: Foundation (M1-M2)** - Build LME+ benchmark and validate with Built-in Memory MCP
2. **Phase 2: System Integration (M3-M6)** - Integrate Memory MCP-2 (Stella v5), compression methods, filesystem, oracle
3. **Phase 3: LME+ Complete Analysis (M7-M10)** - Full LME+ evaluation, translation analysis, retrieval-gated stratification, statistical validity
4. **Phase 4: BrowseComp and Synthesis (M11-M13)** - BrowseComp setup (dynamic memory writes), evaluation, trend analysis

**Key Design Decisions:**
- Starting with Built-in Memory MCP (M2) ensures early validation of the pipeline with the easiest-to-setup system
- Memory MCP-2 (Stella v5, K=V+fact) integration (M3) enables direct comparison with LME baselines using the same underlying retrieval method
- **All LME+ experiments (M1-M10) completed before BrowseComp** - This ensures thorough understanding of memory tool performance before extending to dynamic memory writes
- Consistent logging system tracks time, tokens, cost per sample for latency/cost tax analysis
- Translation analysis and retrieval-gated stratification are core outputs

## Resources Required

### Hardware
- MacBook Pro M4 Max, 64GB RAM
- No GPU required (API-based inference)

### APIs and Keys
- OpenAI API (GPT-4o-mini, GPT-5.2 for judge)
- Anthropic API (Claude models)
- HuggingFace (embeddings, open models)

### Software Dependencies
- Python 3.11+, uv package manager
- LangChain (agent framework)
- Memory systems:
  - Built-in Memory MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
  - Stella V5 1.5B embeddings (for Memory MCP-2)
  - Context compression (LLMLingua or similar)
- MCP filesystem server
- Web browsing tools: Puppeteer or Selenium
- Datasets:
  - LongMemEval: https://github.com/xiaowu0162/LongMemEval
  - BrowseComp: https://github.com/openai/simple-evals

### Budget
| Milestone Phase | Budget | Description |
|----------------|--------|-------------|
| Phase 1: M1-M2 (Foundation) | $5 | LME+ creation + Built-in MCP on 50 tasks |
| Phase 2: M3-M6 (System Integration) | $11 | All 5 memory systems validated |
| Phase 3: M7-M10 (LME+ Complete) | $227 | Full evaluation + ablations + stats (500 tasks × multiple conditions × 3 runs) |
| Phase 4: M11-M13 (BrowseComp + Synthesis) | $105 | BrowseComp setup + evaluation + trend analysis |
| **Total** | **$348** | Across 13 milestones |

**Budget Breakdown by Milestone:**
- M1: $0, M2: $5, M3: $3, M4: $3, M5: $3, M6: $2
- M7: $25, M8: $2, M9: $80, M10: $120
- M11: $5, M12: $100, M13: $0

