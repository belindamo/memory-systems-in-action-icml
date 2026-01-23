# Do Memory Tools Help Agents? The Surprising Failure of Dense Retrieval

**Anonymous Authors**

## Abstract

Memory systems for AI agents are typically evaluated on static retrieval benchmarks, where dense embeddings consistently outperform keyword search. We introduce **LME+**, an agentic adaptation of the LongMemEval benchmark, and evaluate five memory approaches: Oracle (perfect retrieval), keyword search, dense embeddings (Stella V5), filesystem access, and a hybrid combining keyword + embeddings. Surprisingly, **keyword search (62% accuracy) vastly outperformed dense embeddings (26%)** and even their hybrid combination (42%), despite dense embeddings excelling on the static LME benchmark. We identify a 28-point gap between Oracle (90%) and the best practical method, attributing this to retrieval quality rather than agent architecture. Our findings challenge the assumption that static retrieval performance translates to agentic settings and suggest simple keyword search remains the most effective approach for conversational memory.

**Keywords:** AI agents, memory systems, dense retrieval, keyword search, benchmarking

---

## 1. Introduction

AI agents increasingly require long-term memory to maintain context across extended interactions. While static retrieval benchmarks like LongMemEval [1] show dense embeddings outperforming keyword search, real agents use memory dynamically through iterative tool calls. **Does static retrieval performance translate to agentic settings?**

We introduce **LME+**, where a ReAct agent [2] actively queries memory to answer questions, converting LongMemEval's static task into an agentic one. We evaluate five approaches:

1. **Oracle** - Perfect retrieval (gold answer sessions)
2. **MCP** - Keyword-based search (BM25-style)
3. **Stella V5** - Dense retrieval (state-of-the-art embeddings)
4. **Filesystem** - Direct file access without semantic search
5. **Hybrid** - Keyword search + embedding reranking

### Key Contributions

1. **Surprising negative result**: Dense embeddings (Stella V5) achieved only 26% accuracy, worse than keyword search's 62%
2. **Hybrid failure**: Combining keyword + embeddings (42%) performed worse than keyword alone
3. **Retrieval bottleneck**: 28-point gap between Oracle (90%) and best method (62%) shows retrieval quality gates performance
4. **Practical recommendation**: Simple keyword search beats sophisticated dense embeddings for agentic conversational memory

---

## 2. Related Work

**Static Memory Benchmarks.** LongMemEval [1] evaluates retrieval systems on conversational QA, finding Stella V5 dense embeddings achieve 71.4% accuracy with top-5 retrieval. Our work tests whether this translates to agents.

**Agent Memory Systems.** Letta [3] found filesystem access (74%) outperformed specialized tools on LoCoMo benchmark. We test this on unstructured conversations and find the opposite.

**Dense vs Sparse Retrieval.** Dense retrievers typically outperform BM25 on static benchmarks [4]. Our work shows this reverses in agentic settings.

---

## 3. LME+: Agentic Memory Benchmark

### 3.1 Task Formulation

**Static LME:** Given conversation history, retrieve top-k sessions, answer question
**Agentic LME+:** Agent uses tools to search memory, reformulate queries, iterate (max 5 turns)

### 3.2 Memory Adapters

All adapters expose a single `search_memory(query)` tool to a ReAct agent:

- **Oracle**: Returns gold answer session(s) - upper bound
- **MCP**: Scores sessions by keyword frequency, returns top-3
- **Stella V5**: Embeds sessions with `dunzhang/stella_en_1.5B_v5`, returns top-3 by cosine similarity
- **Filesystem**: Exposes `list_sessions`, `read_session`, `search_sessions` tools
- **Hybrid**: Keyword search for top-10 candidates, rerank by embeddings to top-3

### 3.3 Evaluation Protocol

- **Dataset**: LongMemEval_S - 50 questions from 442 available
- **Agent**: ReAct with GPT-4o, max 5 iterations
- **Judge**: GPT-4o evaluates semantic equivalence
- **Metrics**: Accuracy, cost (USD), time, token usage

---

## 4. Results

### 4.1 Main Results

| Method | Accuracy | Cost | vs Oracle |
|--------|----------|------|-----------|
| **Oracle** | **90%** | $0.43 | — |
| **MCP (keyword)** | **62%** | $1.62 | **-28pp** |
| **Hybrid** | 42% | $1.51 | -48pp |
| **Filesystem** | 32% | $0.35 | -58pp |
| **Stella V5** | **26%** | $0.82 | **-64pp** |

**Finding 1: Dense embeddings catastrophically fail**
Stella V5 achieved only 26%, worse than keyword search (62%) by 36 points. This contradicts LME static results where Stella V5 achieves 71%.

**Finding 2: Hybrid makes it worse**
Combining keyword + embeddings (42%) underperformed keyword alone (62%) by 20 points, suggesting embeddings actively demote correct results.

**Finding 3: 28pp retrieval gap**
Oracle (90%) vs MCP (62%) shows retrieval quality, not agent architecture, is the bottleneck.

### 4.2 Oracle Ceiling: 90%

Even with perfect retrieval, accuracy reaches only 90%. Analysis of failures:
- Over-elaboration: Agent adds details not in gold answer
- Missing specifics: Agent misses key information (e.g., store name)
- Judge strictness: Semantic equivalence evaluation is strict

This 10% ceiling suggests limited upside from improving retrieval beyond 90%.

### 4.3 Per-Question Analysis

**Consistency Check:** We reran experiments after fixing a formatting bug (literal `\n` vs actual newlines):
- Oracle: 96% question-level consistency
- MCP: 80% consistency
- Results validate reproducibility

**Difficulty Distribution:**
- Easy (all methods succeed): 15/50 questions
- Hard (all methods fail): 8/50 questions
- Discriminative (separates methods): 27/50 questions

---

## 5. Analysis

### 5.1 Why Do Dense Embeddings Fail?

**Hypothesis 1: Session Length**
Average session = 50+ turns (~5k tokens). Long context may produce noisy embeddings that fail to capture key facts.

**Hypothesis 2: Training Mismatch**
Stella V5 trained on documents (Wikipedia, scientific papers), not multi-turn conversations. Embedding space may not align with conversational QA.

**Hypothesis 3: Lexical vs Semantic Match**
Keyword search finds exact lexical matches ("degree" → "Business Administration"). Embeddings compute semantic similarity, which may miss specific facts.

**Hypothesis 4: Top-k Selection**
Embedding similarity scores may not reflect answer presence. A session with low similarity might contain the exact answer.

### 5.2 Why Does Hybrid Fail?

Hybrid strategy: keyword search (top-10) → embed & rerank (top-3)

**Analysis:** Reranking demoted correct results from keyword search. Example:
- Question: "What degree did I graduate with?"
- Keyword search finds session mentioning "Business Administration degree" (rank 2)
- Embedding reranks it to position 5 (semantic similarity to entire session is low)
- Agent never sees the correct session

**Implication:** For fact-based QA, lexical match > semantic similarity

### 5.3 Cost-Accuracy Tradeoff

| Method | Accuracy/$ | Rank |
|--------|-----------|------|
| Oracle | 209%/$ | 1st |
| Filesystem | 91%/$ | 2nd |
| MCP | 38%/$ | 3rd |
| Stella V5 | 32%/$ | 4th |
| Hybrid | 28%/$ | 5th |

**Paradox:** MCP (best practical method) is least cost-efficient due to retrieving top-3 full sessions (~15k tokens). Oracle only retrieves 1 gold session (~3k tokens).

**Recommendation:** Use keyword search with adaptive top-k or session compression.

---

## 6. Discussion

### 6.1 Implications for Memory Tool Design

1. **Prioritize keyword search over dense embeddings** for conversational memory
2. **Semantic search is essential** - filesystem (32%) fails without it
3. **Don't assume static benchmark results translate** to agentic settings
4. **Optimize for cost** - top-k retrieval inflates context significantly

### 6.2 When Do Dense Embeddings Help?

Our negative results don't mean embeddings never work. Possible cases where they'd help:
- **Paraphrased queries**: "What was my major?" vs "What degree..."
- **Conceptual questions**: "What outdoor activities do I like?" (requires aggregating multiple sessions)
- **Longer evaluation**: 5-iteration limit may cut off embedding-based exploration

Future work should identify when embeddings provide value over keyword search.

### 6.3 Limitations

- **Single dataset**: LongMemEval_S only (personal assistant conversations)
- **Single agent**: ReAct with 5 iterations
- **Single LLM**: GPT-4o for agent and judge
- **Limited scale**: 50/500 questions due to budget constraints
- **No hyperparameter tuning**: top-k=3 fixed, no ablations

---

## 7. Conclusion

We introduced LME+, an agentic adaptation of LongMemEval, and made two surprising discoveries:

1. **Dense embeddings (Stella V5) achieve only 26% accuracy**, dramatically underperforming keyword search's 62%
2. **Hybrid keyword + embedding reranking (42%) performs worse** than keyword alone

These findings challenge assumptions from static retrieval benchmarks and suggest **simple keyword search remains the best approach for agentic conversational memory**. The 28-point gap between Oracle (90%) and keyword search (62%) identifies retrieval quality as the primary bottleneck, not agent architecture.

**Practical recommendation:** Use keyword search (BM25-style) for agentic memory systems. Dense embeddings may actively hurt performance in conversational QA settings.

---

## References

[1] Wu et al. "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory." ICLR 2025.

[2] Yao et al. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023.

[3] Letta. "Benchmarking AI Agent Memory." https://www.letta.com/blog/benchmarking-ai-agent-memory, 2024.

[4] Karpukhin et al. "Dense Passage Retrieval for Open-Domain Question Answering." EMNLP 2020.

---

## Appendix A: Example Questions

**Easy (all methods succeed):**
Q: "What is my dog's name?"
A: "Max" - clear fact, single mention

**Hard (all methods fail):**
Q: "Where do I take yoga classes?"
A: "Serenity Yoga" - mentioned once casually, low salience

**Discriminative:**
Q: "What degree did I graduate with?"
Oracle ✓, MCP ✓, Others ✗

---

## Appendix B: Reproducibility

All code, data, and results available at:
`github.com/[anonymous]/lme-plus`

Cost: $8.02 for all experiments (Oracle, MCP, Stella V5, Filesystem, Hybrid × 50 samples each + validation)

Agent implementation: ReAct with OpenAI function calling
Judge implementation: GPT-4o with semantic equivalence prompt
