# Literature Review: Memory Systems for LLM Agents

## Stage 0 Output - AI Co-Scientist

**Date:** 2026-01-22
**Project:** LME+ - Evaluating Memory Systems on Agentic Tasks

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

## Summary

The literature reveals a critical tension:
- **Specialized memory tools** (MCP, knowledge graphs) promise sophisticated memory management
- **Simple approaches** (filesystem, basic RAG) achieve competitive results due to agent training optimization
- **The gap:** No systematic comparison of these methods when retrieval becomes agentic

This research (LME+) will directly address whether the complexity of memory tools is justified in agentic contexts.
