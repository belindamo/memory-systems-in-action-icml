# Literature Review: Memory Systems for LLM Agents

## Stage 0 Output - AI Co-Scientist

**Date:** 2026-01-22 (Updated: 2026-01-23)
**Project:** LME+ - Evaluating Memory Systems on Agentic Tasks
**Revision:** Iteration 2 - Addressing ICML Review Feedback (W2: Missing Baselines)

---

## 1. Surveys & Comprehensive Reviews

### Memory in the Age of AI Agents (Dec 2025)
- **Source:** [arXiv:2512.13564](https://arxiv.org/abs/2512.13564)
- **Key Finding:** Traditional taxonomies (long/short-term memory) are insufficient for contemporary agent memory systems
- **Contribution:** Proposes finer-grained taxonomy: factual, experiential, and working memory
- **Paper List:** [GitHub - Agent-Memory-Paper-List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)

### A Survey on the Memory Mechanism of Large Language Model-based Agents
- **Source:** [ACM TOIS](https://dl.acm.org/doi/10.1145/3748302)
- **Relevance:** Comprehensive overview of memory design and evaluation strategies

### Agentic RAG Survey (Jun 2025)
- **Source:** [arXiv:2501.09136](https://arxiv.org/abs/2501.09136)
- **Key Finding:** Agentic RAG transcends static RAG by embedding autonomous agents into the retrieval pipeline
- **Distinction:** Static retrieval follows fixed pipelines; agentic systems dynamically plan and refine

---

## 2. Memory Architectures

### A-MEM: Agentic Memory for LLM Agents (NeurIPS 2025)
- **Source:** [arXiv:2502.12110](https://arxiv.org/abs/2502.12110)
- **Method:** Dynamic memory organization using Zettelkasten principles
- **Innovation:** Creates interconnected knowledge networks through dynamic indexing and linking

### AgeMem: Unified Long-Term and Short-Term Memory (Jan 2026)
- **Source:** [arXiv:2601.01885](https://arxiv.org/html/2601.01885v1)
- **Method:** Exposes memory operations as tool-based actions
- **Innovation:** LLM agent autonomously decides what/when to store, retrieve, update, summarize, or discard
- **Training:** Three-stage progressive reinforcement learning

### MAGMA: Multi-Graph Agentic Memory Architecture (2026)
- **Relevance:** Multi-graph approach for structured memory

### EverMemOS: Memory Operating System (2026)
- **Relevance:** Self-organizing memory for structured long-horizon reasoning

### Hierarchical Memory (H-MEM)
- **Source:** [arXiv:2507.22925](https://arxiv.org/abs/2507.22925)
- **Method:** Multi-level memory organization for long-term reasoning

### Mem0: Production-Ready AI Agents
- **Source:** [arXiv:2504.19413](https://arxiv.org/abs/2504.19413)
- **Method:** Scalable, memory-centric architecture with dynamic memory consolidation

### MemR3: Memory Retrieval via Reflective Reasoning (Dec 2024) ⭐ NEW
- **Source:** [arXiv:2512.20237](https://arxiv.org/html/2512.20237v1)
- **Method:** Reflective reasoning to decide when to retrieve from long-term memory
- **Benchmark:** Evaluated on LoCoMo
- **Relevance:** Directly comparable concurrent work on agent memory retrieval
- **ICML Review Note:** W2 requires citation and comparison

### Hindsight: Agent Memory with Retain/Recall/Reflect (Dec 2024) ⭐ NEW
- **Source:** [arXiv:2512.12818](https://arxiv.org/html/2512.12818v1)
- **Method:** Three-stage memory mechanism for very long conversations
- **Benchmark:** Evaluated on LoCoMo
- **Relevance:** Alternative memory approach for comparison
- **ICML Review Note:** W2 requires citation and comparison

---

## 3. Benchmarks & Evaluation

### LongMemEval (Updated Mar 2025)
- **Source:** [arXiv:2410.10813](https://arxiv.org/abs/2410.10813)
- **Tasks:** 500 questions, 5 core abilities (extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention)
- **Finding:** Commercial assistants show 30% accuracy drop in sustained interactions
- **Best Config:** Stella V5 1.5B, K=V+fact, QA@10 = 72.0%

### LoCoMo: Long-Term Conversational Memory
- **Source:** [arXiv:2402.17753](https://arxiv.org/abs/2402.17753), [Project Page](https://snap-research.github.io/locomo/)
- **Dataset:** 300 turns, 9K tokens avg, up to 35 sessions per conversation
- **Tasks:** QA, event summarization, multi-modal dialogue
- **Finding:** LLMs substantially lag behind human performance on lengthy conversations

### MemoryAgentBench (Jul 2025)
- **Source:** [arXiv:2507.05257](https://arxiv.org/abs/2507.05257)
- **Competencies:** Accurate retrieval, test-time learning, long-range understanding, selective forgetting
- **Finding:** Current methods fall short of mastering all four competencies

### Context-Bench: Agentic Context Engineering
- **Source:** [Letta Blog](https://www.letta.com/blog/context-bench)
- **Finding:** Even best models achieve only 74% accuracy on context engineering
- **Insight:** "Agentic context engineering" is the new frontier in AI agents

### Letta Memory Benchmark
- **Source:** [Letta Leaderboard](https://www.letta.com/blog/benchmarking-ai-agent-memory)
- **Key Result:** Letta Filesystem scores 74.0% on LoCoMo
- **Critical Finding:** Simple filesystem tools beat specialized memory libraries
- **Reason:** Agents are well-optimized for filesystem tools due to agentic coding training

### GoodAI LTM Benchmark
- **Source:** [GitHub](https://github.com/GoodAI/goodai-ltm-benchmark)
- **Focus:** Dynamic memory upkeep and long-horizon information integration

---

## 4. RAG vs Memory vs Filesystem

### Key Distinctions
| Approach | Answers | Characteristics |
|----------|---------|-----------------|
| RAG | "What do I know?" | Static retrieval, context pollution risk |
| Memory | "What do I remember about you?" | Temporal awareness, relationship understanding |
| Filesystem | Direct file access | Simple, well-supported by agent training |

### Letta's Critical Finding
- **Source:** [RAG is not Agent Memory](https://www.letta.com/blog/rag-vs-agent-memory)
- **Finding:** "With a well-designed agent, even simple filesystem tools are sufficient to perform well on retrieval benchmarks"
- **Explanation:** Agents today are extremely effective at using filesystem tools due to post-training optimization for agentic coding tasks

### Mastra's Counter-Finding
- **Source:** [Mastra Blog](https://mastra.ai/blog/use-rag-for-agent-memory)
- **Finding:** Achieved 80% with semantic recall (RAG) alone on LoCoMo
- **Note:** 8 points higher than Zep's benchmark claiming RAG doesn't work

### RAG Limitations for Agent Memory
- Cannot distinguish old vs new information
- Fails to grasp relationships between events
- Context pollution degrades performance (especially for reasoning models)

---

## 4.5. Sparse vs Dense Retrieval Methods ⭐ NEW SECTION

### BM25: The Gold Standard for Sparse Retrieval
- **Algorithm:** TF-IDF with document length normalization and term saturation
- **Formula:** $\text{BM25}(D,Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot (1 - b + b \cdot \frac{|D|}{\text{avgdl}})}$
- **Default parameters:** $k_1 = 1.2$, $b = 0.75$
- **Typical improvement:** 5-15% over raw frequency counting
- **ICML Review Note:** W2 requires proper BM25 implementation vs current frequency counting

### Dense Embedding Models (MTEB Leaderboard)
- **Source:** [MTEB Leaderboard](https://modal.com/blog/mteb-leaderboard-article)
- **Top Models (2025):**
  - Stella V5 1.5B: 72.0% on retrieval tasks
  - BGE-large-en-v1.5: 64.2% on retrieval tasks
  - E5-large-v2: 62.9% on retrieval tasks
  - Jina-embeddings-v3: 60.8% on retrieval tasks
- **ICML Review Note:** W2 requires testing at least one other embedding model (BGE or E5)

### Jasper and Stella: Distillation of SOTA Embedding Models (Dec 2024)
- **Source:** [arXiv:2412.19048](https://arxiv.org/html/2412.19048v2)
- **Finding:** Stella V5 trained primarily on documents (Wikipedia, scientific papers), not conversations
- **Implication:** May explain poor performance on conversational QA (H2 hypothesis)

### Hybrid Retrieval Methods
- **Source:** [Hybrid Retrieval Survey](https://mbrenndoerfer.com/writing/hybrid-retrieval-combining-sparse-dense-methods-effective-information-retrieval)
- **Typical Improvement:** 10-50% over single-method baselines
- **Standard Fusion Techniques:**
  1. **Reciprocal Rank Fusion (RRF):** $\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + r(d)}$ where $k=60$
  2. **Weighted Scoring:** $\text{score} = \alpha \cdot \text{sparse} + (1-\alpha) \cdot \text{dense}$
  3. **Neural Rerankers:** Cohere, Jina, cross-encoders
- **ICML Review Note:** W7 suggests our cascade hybrid may be suboptimal vs RRF

### Advanced RAG Systems (2024-2025)
- **Source:** [Systematic Review of RAG Systems](https://arxiv.org/html/2507.18910v1)
- **Key Finding:** Proper fusion consistently outperforms single-method retrieval
- **Source:** [Advanced RAG: Hybrid Search and Re-ranking](https://dev.to/kuldeep_paul/advanced-rag-from-naive-retrieval-to-hybrid-search-and-re-ranking-4km3)
- **Standard Practice:** keyword → reranker (skipping embedding retrieval)

---

## 5. Context Compression

### KVzip (Seoul National University, Nov 2025)
- **Source:** [TechXplore](https://techxplore.com/news/2025-11-ai-tech-compress-llm-chatbot.html)
- **Performance:** 3-4x memory compression while maintaining accuracy
- **Speed:** 2x response speed improvement
- **Capacity:** Supports up to 170,000 tokens

### Focus: Active Context Compression (Jan 2026)
- **Source:** [arXiv:2601.07190](https://arxiv.org/html/2601.07190)
- **Result:** Reduced tokens from 14.9M to 11.5M while matching baseline accuracy
- **Innovation:** Intra-trajectory compression - agent prunes its own history during task
- **Finding:** 50-57% savings on navigation-heavy instances

### RCC: Recurrent Context Compression
- **Source:** [OpenReview](https://openreview.net/pdf?id=GYk0thSY1M)
- **Performance:** 32x storage savings with 32x compression rate
- **Method:** Efficient context window expansion

### TTT-E2E: Test-Time Training
- **Source:** [NVIDIA Blog](https://developer.nvidia.com/blog/reimagining-llm-memory-using-context-as-training-data-unlocks-models-that-learn-at-test-time)
- **Performance:** 2.7x speedup for 128K context, 35x for 2M context
- **Method:** Compresses context into model weights via next-token prediction

---

## 6. Query Reformulation & Iterative Retrieval

### Reasoning Agentic RAG (Jun 2025)
- **Source:** [arXiv:2506.10408](https://arxiv.org/html/2506.10408v1)
- **Shift:** From static, rule-driven pipelines to dynamic, reasoning-driven architectures
- **Innovation:** Models actively determine when, what, and how to retrieve

### DeepRetrieval (Jiang et al., 2025)
- **Method:** Trains models to reformulate queries by maximizing retrieval metrics

### ReZero (Retry-Zero)
- **Focus:** Teaching agents the value of "trying one more time"
- **Problem Addressed:** Agents halt prematurely after failed initial queries

### SPAR: Multi-Agent Academic Retrieval
- **Source:** [arXiv](https://arxiv.org/html/2510.08383)
- **Features:** Query Evolver Agent for iterative, citation-aware query reformulation

---

## 7. Model Context Protocol (MCP)

### Overview
- **Source:** [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25), [Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- **Definition:** Open standard for AI systems to integrate with external tools/data
- **Adoption:** OpenAI (Mar 2025), donated to Linux Foundation (Dec 2025)

### MCP Memory Servers
- **Official:** Knowledge graph-based persistent memory system in [MCP Servers repo](https://github.com/modelcontextprotocol/servers)
- **HPKV:** Production memory server with long-term memory ([Blog](https://hpkv.io/blog/2025/04/mcp-memory-with-hpkv))
- **Cognee:** MCP + Cognee integration for LLM memory ([Blog](https://www.cognee.ai/blog/deep-dives/model-context-protocol-cognee-llm-memory-made-simple))

### Security Concerns (Apr-Jul 2025)
- Prompt injection vulnerabilities
- Most servers lack authentication
- Tool permission concerns

---

## 8. Industry Trends (2026)

- **65% of enterprise AI failures in 2025** attributed to context drift or memory loss during multi-step reasoning
- **Pivot to hierarchical memory:** Moving from "massive context windows" to structured memory
- **80% cost reduction** reported with compression and optimization
- **10x inference throughput** improvements with compressed models

---

## 9. Identified Gaps

### Gap 1: Static vs Agentic Retrieval Translation
- **Question:** Do improvements on static retrieval benchmarks (LME) translate to agentic gains (LME+)?
- **Status:** Unknown - this is the core research question

### Gap 2: Memory Method Comparison in Agentic Context
- **Question:** How do MCP tools vs filesystem vs compression compare when retrieval is agentic?
- **Letta's Surprising Finding:** Filesystem achieves 74% on LoCoMo, beating specialized tools
- **Status:** Needs systematic comparison

### Gap 3: Cost of Agenticity
- **Question:** What is the latency/cost tax of agentic retrieval vs static retrieval?
- **Status:** Not systematically measured

### Gap 4: Retrieval Gating
- **Question:** Does memory help only after retrieval is solved?
- **LME Finding:** 15-19% errors from correct retrieval but wrong generation
- **Status:** Stratified analysis needed

---

## 10. Candidate Methods for Experimentation

Based on literature review, the following methods should be tested:

| ID | Method | Category | Rationale |
|----|--------|----------|-----------|
| A | Built-in Memory MCP | Tool-based | Baseline MCP implementation |
| B | Memory MCP-2 (Stella v5, K=V+fact) | Tool-based | Best LME config, enables direct comparison |
| C | MCP + Filesystem | Hybrid | Tests combination effect |
| D | Filesystem only | File-based | Letta showed 74% with simple filesystem |
| E | Context compression (Focus/KVzip) | Compression | Active compression showed promise |
| F | RAG baseline | Retrieval | Mastra showed 80% with semantic recall |
| O | Oracle | Upper bound | Gold evidence after 1 query |

---

## 11. Key References for Methodology

1. **LongMemEval methodology:** LLM judge (GPT-4o/5.2), Recall@K, NDCG@K
2. **LoCoMo benchmark:** QA, event summarization, multi-modal tasks
3. **Letta evaluation:** Filesystem as baseline, apples-to-apples comparison
4. **Stratified analysis:** Retrieval-gated evaluation (Failed/Partial/Good/Excellent strata)

---

## 12. ICML Review Response: Addressing Weaknesses ⭐ NEW SECTION

### W1: Limited Scale (50/500 questions)
- **Required:** Confidence intervals, statistical significance tests (McNemar's)
- **Options:** (1) Scale to 200+ questions, (2) Add CIs, (3) Reframe as pilot study
- **Current Cost:** $8.02 for 300 evaluations → ~$30 for 200 questions

### W2: Missing Critical Baselines
| Baseline | Status | Action Required |
|----------|--------|-----------------|
| Proper BM25 (not frequency) | ❌ Missing | Implement with IDF, length normalization |
| BGE or E5 embeddings | ❌ Missing | Test alternative to Stella V5 |
| MemR3 comparison | ❌ Missing | Cite and compare LoCoMo results |
| Hindsight comparison | ❌ Missing | Cite and compare LoCoMo results |
| Reranker-only baseline | ❌ Missing | Test keyword → reranker pipeline |

### W3: No Mechanistic Analysis
| Hypothesis | Test Proposed |
|------------|---------------|
| H1: Session Length | Chunk sessions into 10-turn segments |
| H2: Training Mismatch | Verify Stella V5 on document QA |
| H3: Lexical vs Semantic | Analyze failure cases for rare terms |
| H4: Reranking Failure | Quantitative rank movement analysis |

### W4: Misleading Letta Comparison
- **Issue:** Letta tested file-based context management on LoCoMo (74%), not filesystem tools for search
- **Fix:** Clarify distinction in Related Work section

### W5-W7: Architecture, Judge Bias, Hybrid Implementation
- Single agent architecture (ReAct only)
- GPT-4o as both agent and judge (circularity)
- Cascade hybrid vs RRF fusion

---

## Summary

The literature reveals a critical tension:
- **Specialized memory tools** (MCP, knowledge graphs) promise sophisticated memory management
- **Simple approaches** (filesystem, basic RAG) achieve competitive results due to agent training optimization
- **The gap:** No systematic comparison of these methods when retrieval becomes agentic

This research (LME+) will directly address whether the complexity of memory tools is justified in agentic contexts.

**Revision Note (Iteration 2):** Literature review updated to address ICML Review W2 concerns. Added citations for MemR3, Hindsight, BM25 methodology, MTEB leaderboard context, and hybrid retrieval best practices.
