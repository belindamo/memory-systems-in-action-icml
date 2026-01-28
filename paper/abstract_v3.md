# Revised ICML Abstracts - Stronger, Less Technical

---

## Version 1: Bold Ending

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embedding models consistently outperform sparse methods. But agents don't retrieve once—they query iteratively, reformulate based on results, and adapt to failures. We introduce LME+, an agentic benchmark where a ReAct agent actively queries memory tools to answer questions from long conversational histories. Our results reveal a striking reversal: simple keyword matching dramatically outperforms dense embeddings in agentic settings, despite the latter excelling on static benchmarks. Hybrid retrieval fares even worse, suggesting that embedding-based reranking actively harms performance by demoting lexically-relevant results. These findings challenge the assumption that retrieval improvements on static benchmarks translate to agent performance, and suggest practitioners building memory-augmented agents should reconsider their default retrieval choices.

**Word count: 131**

---

## Version 2: Problem-Focused Opening

The proliferation of memory-augmented LLM agents—from ChatGPT to Claude to open-source alternatives—has created urgent need to understand which retrieval methods actually help agents remember. Static benchmarks suggest dense embeddings are optimal, but agents don't retrieve statically: they issue iterative queries, reformulate on failure, and explore results dynamically. We introduce LME+, an agentic benchmark built on LongMemEval, and find that conventional wisdom is wrong. Simple keyword matching dramatically outperforms dense embeddings when agents control the retrieval process. More surprisingly, hybrid retrieval—combining sparse and dense methods—performs worse than keywords alone, suggesting embeddings actively interfere with agentic retrieval. Our results imply that static retrieval benchmarks may be misleading proxies for agent memory performance, with significant implications for how practitioners design and evaluate memory systems.

**Word count: 133**

---

## Version 3: Shortest, Punchiest

Dense embedding models dominate retrieval benchmarks, leading practitioners to adopt them for agent memory systems. We test whether this choice is justified. Using LME+, an agentic adaptation of LongMemEval where a ReAct agent iteratively queries memory tools, we find that simple keyword matching dramatically outperforms dense embeddings—and that adding embeddings to a hybrid system makes performance worse, not better. These results suggest that static benchmark rankings do not predict agentic performance: what works when you retrieve once may fail when agents retrieve iteratively. Practitioners building memory-augmented agents should evaluate retrieval methods in agentic settings rather than relying on static benchmark leaderboards.

**Word count: 102**

---

## Version 4: Narrative Arc

When building memory for LLM agents, practitioners typically reach for dense embedding models—they dominate retrieval benchmarks and power production RAG systems. But agents use memory differently than static retrieval: they query iteratively, reformulate on failure, and explore results before committing to an answer. We ask whether benchmark-winning retrieval methods remain optimal in this dynamic setting. Using LME+, an agentic benchmark built on LongMemEval, we find they do not. Simple keyword matching dramatically outperforms dense embeddings when an agent controls retrieval. Hybrid approaches fare even worse, suggesting that embeddings actively interfere with agentic search. Static retrieval benchmarks appear to be poor proxies for agent memory performance—a finding with immediate implications for practitioners and benchmark designers alike.

**Word count: 122**

---

## My Recommendation: Version 4

**Why:**
- Opens with practitioner behavior (relatable)
- Builds narrative tension ("we ask whether...")
- Strong finding clearly stated
- Ends with dual implications (practitioners AND benchmark designers)
- No statistical clutter
- 122 words = well under limit with room for expansion if needed

**Suggested title to match:**
"Static Retrieval Benchmarks Are Poor Proxies for Agent Memory Performance"

or keep the question format:
"Do Memory Tools Help Agents? Why Static Retrieval Benchmarks May Mislead"
