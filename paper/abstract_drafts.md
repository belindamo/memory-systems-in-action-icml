# Abstract Drafts for LME+ Paper

## Draft 1 (Conservative, no locked numbers)

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embedding models consistently outperform sparse keyword methods. However, agents use memory dynamically—issuing multiple queries, reformulating based on results, and iterating until success. We introduce LME+, an agentic benchmark built on LongMemEval where a ReAct agent actively queries memory tools to answer conversational questions. Surprisingly, we find that simple keyword-based retrieval substantially outperforms dense embeddings in this agentic setting, despite the latter achieving state-of-the-art performance on the underlying static benchmark. A hybrid approach combining both methods performs worse than keywords alone, suggesting that embedding-based reranking can demote relevant results. Oracle experiments with perfect retrieval establish that retrieval quality, not agent architecture, is the primary bottleneck. Our findings challenge the assumption that static retrieval gains translate to agentic settings and suggest that practitioners should reconsider default choices when building memory-augmented agents.

**Word count:** 153

---

## Draft 2 (Tighter)

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embeddings consistently outperform keyword search. We ask whether these gains transfer when agents iteratively query memory tools. We introduce LME+, an agentic adaptation of LongMemEval where a ReAct agent dynamically queries memory to answer conversational questions. Our experiments reveal a striking reversal: simple frequency-based keyword matching significantly outperforms dense embeddings, despite the latter excelling on static benchmarks. Moreover, a hybrid approach combining keywords with embedding-based reranking underperforms keywords alone, suggesting embeddings actively demote relevant results in this setting. Oracle experiments confirm that retrieval quality—not agent reasoning—is the primary bottleneck. These findings challenge conventional wisdom about retrieval method selection and motivate further investigation into why dense representations underperform when retrieval becomes agentic.

**Word count:** 131

---

## Draft 3 (With filesystem finding)

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embeddings consistently outperform keyword search. We ask whether these gains transfer when agents iteratively query memory tools. We introduce LME+, an agentic adaptation of LongMemEval where a ReAct agent dynamically queries memory to answer conversational questions. We evaluate keyword search, dense embeddings, filesystem browsing, and hybrid approaches. Our experiments reveal a striking reversal: simple frequency-based keyword matching significantly outperforms both dense embeddings and filesystem access, despite embeddings excelling on static benchmarks and prior work showing strong filesystem performance on related tasks. A hybrid approach combining keywords with embedding reranking underperforms keywords alone, suggesting embeddings actively demote relevant results. Oracle experiments confirm that retrieval quality—not agent reasoning—is the primary bottleneck. These findings challenge conventional wisdom about retrieval method selection for memory-augmented agents.

**Word count:** 144

---

## Draft 4 (Letta contrast)

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embeddings outperform keyword search. Prior work suggests simple filesystem access may suffice for agent memory. We introduce LME+, an agentic benchmark built on LongMemEval, and evaluate keyword search, dense embeddings, filesystem browsing, and hybrid approaches. Surprisingly, keyword-based retrieval significantly outperforms both dense embeddings and filesystem access in our agentic setting—a reversal from static benchmark rankings. Hybrid retrieval combining keywords with embedding reranking performs worse than keywords alone. Oracle experiments establish retrieval quality as the primary bottleneck over agent architecture. Our results suggest static benchmark performance and filesystem-based approaches do not reliably predict agentic memory performance, motivating further investigation into retrieval method selection for memory-augmented agents.

**Word count:** 127

---

## Notes
- Saved: 2026-01-23
- Status: Pending revision after new experiments (BM25, BGE/E5, scale to 200 questions, filesystem fix)
- Will update numbers and claims based on expanded results
