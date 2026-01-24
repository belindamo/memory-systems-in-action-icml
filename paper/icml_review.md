# ICML Review: "Do Memory Tools Help Agents? The Surprising Failure of Dense Retrieval"

---

## Summary

This paper introduces LME+, an agentic adaptation of the LongMemEval benchmark, to evaluate whether static retrieval performance translates to agentic settings. The authors evaluate five memory approaches (Oracle, keyword search, dense embeddings via Stella V5, filesystem access, and a hybrid approach) on 50 questions using a ReAct agent with GPT-4o. The main finding is that keyword search achieves 62% accuracy, dramatically outperforming dense embeddings (26%) and their hybrid combination (42%), contrary to static benchmark results where Stella V5 achieves 71% on LongMemEval.

---

## Strengths

1. **Important and Timely Research Question**: The paper addresses a critical gap between static retrieval evaluation and actual agent performance. This is highly relevant given the proliferation of agent systems with memory (ChatGPT, Claude, Letta) and aligns with recent survey work on agent memory mechanisms [Memory in the Age of AI Agents, Dec 2024](https://arxiv.org/abs/2512.13564).

2. **Clear Negative Result with Practical Value**: The 36-point gap between keyword search (62%) and dense embeddings (26%) is substantial and actionable for practitioners. Negative results are valuable when well-documented, and this finding challenges widespread assumptions about dense retrieval superiority.

3. **Reproducibility Validation**: The authors discovered a formatting bug and reran experiments, showing 80-96% per-question consistency. This demonstrates scientific rigor and transparency. Total cost ($8.02) makes replication feasible.

4. **Oracle Ceiling Analysis**: The 90% Oracle performance identifies a 28-point retrieval gap as the primary bottleneck, effectively isolating retrieval quality from agent architecture limitations.

5. **Cost-Accuracy Tradeoff**: Including cost analysis (Table \ref{tab:detailed}) is practical and important for real deployments. The paradox that keyword search is less cost-efficient despite being more accurate is well-documented.

---

## Weaknesses

### Critical Issues

**W1. Limited Scale Undermines Generalizability (50/500 questions = 10%)**

The paper evaluates only 50 of 500 available LongMemEval questions due to budget constraints. However:
- With total cost of $8.02 for all experiments, extending to 500 questions would cost ~$80
- Standard error analysis is missing: with 50 questions, 95% CI for 62% accuracy is approximately ±13pp
- The paper's main claims (keyword > dense embeddings) could reverse with different question samples
- Recent work on [LoCoMo benchmark](https://snap-research.github.io/locomo/) evaluates on full datasets (300+ turns per conversation)

**Impact**: This severely limits confidence in the generalizability of findings. A fundamental requirement for publication-quality experimental work is sufficient statistical power.

**Required Fix**: Either (1) scale to full 500 questions, or (2) provide confidence intervals and statistical significance tests (McNemar's test for paired accuracies), or (3) explicitly reframe as a pilot study with appropriate caveats.

---

**W2. Missing Critical Baselines from Recent Literature**

The paper omits several important baselines from 2024 literature:

1. **No comparison to recent agent memory systems**:
   - [MemR3 (Dec 2024)](https://arxiv.org/html/2512.20237v1): Reflective reasoning for memory retrieval in LLM agents, tested on LoCoMo
   - [Hindsight (Dec 2024)](https://arxiv.org/html/2512.12818v1): Agent memory with retain/recall/reflect mechanisms
   - Both papers use LoCoMo as their primary benchmark; comparing results would contextualize findings

2. **No BM25 implementation details**: The paper states "BM25-style" keyword search but implements simple frequency counting: `score(s,q) = Σ count(w,s)`. True BM25 includes IDF weighting and document length normalization, which typically improves performance by 5-15% over raw frequency. This is standard in [hybrid retrieval systems](https://mbrenndoerfer.com/writing/hybrid-retrieval-combining-sparse-dense-methods-effective-information-retrieval).

3. **No other embedding models**: The paper only tests Stella V5. Recent [MTEB leaderboard](https://modal.com/blog/mteb-leaderboard-article) models (e.g., BGE, E5, Jina) may perform differently on conversational QA.

4. **No reranker-only baseline**: Standard practice in [hybrid RAG systems](https://dev.to/kuldeep_paul/advanced-rag-from-naive-retrieval-to-hybrid-search-and-re-ranking-4km3) is keyword→reranker (skipping embedding retrieval). Testing this would isolate whether embeddings hurt during retrieval vs. reranking.

**Impact**: Without these baselines, readers cannot determine whether findings are specific to:
- Stella V5 vs. dense embeddings generally
- Frequency counting vs. proper BM25
- This hybrid approach vs. better-designed hybrid systems

**Required Fix**: Add at least (1) proper BM25 implementation, (2) one other embedding model (BGE or E5), and (3) cite/compare with MemR3 and Hindsight results.

---

**W3. Insufficient Analysis of WHY Dense Embeddings Fail**

Section 4.2 lists four hypotheses (H1-H4) but provides no empirical evidence for any:

- **H1 (Session Length)**: Not tested. Authors could ablate by chunking sessions into shorter segments
- **H2 (Training Mismatch)**: Not tested. Could evaluate on document-based QA to verify Stella V5 works there
- **H3 (Lexical vs Semantic)**: Not tested. Could analyze failure cases: do they involve rare terms or factual precision?
- **H4 (Reranking Failure)**: Partially supported by hybrid results but no quantitative analysis of rank movements

Recent work on [hybrid retrieval](https://21510208.fs1.hubspotusercontent-na1.net/hubfs/21510208/Hybrid_Retriever.pdf) shows 10-50% improvements by combining methods properly. Your hybrid approach gets -20pp, suggesting implementation issues rather than fundamental incompatibility.

**Impact**: The paper identifies an important problem but doesn't explain it, limiting scientific contribution and actionability.

**Required Fix**:
- Implement at least 2 ablations to test hypotheses (e.g., chunk sessions to test H1, analyze failure cases for H3)
- Compare your hybrid implementation to standard fusion techniques (RRF, weighted scoring)
- Provide error analysis: what types of questions does dense retrieval fail on?

---

**W4. Comparison to Letta's LoCoMo Results is Misleading**

Lines 76-77 state: "LoCoMo tests structured data extraction, where filesystem access (74%) outperforms specialized tools."

However, [Letta's actual finding](https://www.letta.com/blog/benchmarking-ai-agent-memory) was more nuanced:
- gpt-4o-mini with filesystem achieves 74% on LoCoMo
- This was on structured conversations (300 turns, 9K tokens, temporal event graphs)
- The finding was that "memory is more about how agents manage context than the exact retrieval mechanism"

Your paper states filesystem access achieves 32% (vs. Letta's 74%), but:
1. Different datasets (LongMemEval vs LoCoMo)
2. Different agent implementations
3. Different LLMs (GPT-4o vs gpt-4o-mini)
4. Letta used conversation files, not raw filesystem tools

This comparison in Related Work suggests the findings conflict, but they're testing different things.

**Impact**: Misrepresents prior work and confuses readers about reconciling findings.

**Required Fix**: Clarify that Letta tested structured extraction on LoCoMo with file-based context management, not filesystem tools for unstructured search.

---

### Moderate Issues

**W5. Single Agent Architecture Limits Generalizability**

The paper only tests ReAct with 5 iterations. Recent work shows:
- [AgentArch benchmark](https://arxiv.org/html/2509.10769v1) evaluates multiple agent architectures
- Iteration budget (5 turns) may disadvantage embedding-based methods that require exploration
- Temperature=0.7 introduces stochasticity but no multiple seeds reported

**Fix**: Test with at least one other agent architecture (e.g., planning-based) or justify why ReAct is representative.

---

**W6. GPT-4o Judge Evaluation May Introduce Bias**

Using GPT-4o as both agent and judge creates potential circularity:
- The agent may generate answers in a style the judge prefers
- No inter-annotator agreement with human judges reported
- Recent work on [LoCoMo](https://aclanthology.org/2024.acl-long.747.pdf) reports human ceiling of 87.9 F1

**Fix**: Include human evaluation on a subset (10-20 questions) to validate judge accuracy, or report correlation with human judgments.

---

**W7. Hybrid Implementation May Be Suboptimal**

Your hybrid (keyword top-10 → embedding rerank to top-3) differs from standard practice:
- [Reciprocal Rank Fusion](https://vizuara.substack.com/p/a-primer-on-re-ranking-for-retrieval) runs both retrievers independently, then fuses
- Weighted scoring combines similarity scores rather than cascading
- Neural rerankers (e.g., Cohere, Jina reranker) typically outperform embedding-based reranking

**Impact**: The "hybrid failure" finding may be specific to this implementation, not a general property.

**Fix**: Test alternative fusion methods or clarify that this is one specific hybrid approach.

---

## Questions for Authors

1. **Statistical Significance**: With 50 questions, what are the confidence intervals on accuracy? Is the 36-point gap between keyword (62%) and Stella V5 (26%) statistically significant (McNemar's test)?

2. **Baseline Verification**: Can you confirm that Stella V5 achieves expected performance on static LongMemEval (71%)? This would verify that the model is working correctly and the performance drop is due to agentic setting.

3. **Ablations**: What happens if you:
   - Chunk long sessions into 10-turn segments (test H1)?
   - Use proper BM25 instead of frequency counting?
   - Increase iteration budget to 10 or 15?
   - Test BGE or E5 embeddings instead of Stella V5?

4. **Error Analysis**: Can you provide per-category breakdown:
   - What % of errors involve rare/specific terms (supporting H3)?
   - What % involve temporal reasoning vs. factual extraction?
   - Do failure modes differ between keyword and embedding methods?

5. **Letta Comparison**: Have you tried replicating Letta's file-based approach on your dataset? The 32% filesystem result seems much lower than Letta's 74% on LoCoMo.

6. **Retrieval Metrics**: What are the retrieval precision/recall numbers? This would isolate whether embeddings fail at retrieval or agent reasoning.

7. **Oracle Analysis**: You report 90% Oracle accuracy. What causes the 10% failure? Is it agent reasoning, judge strictness, or ambiguous questions?

---

## Minor Issues

1. **Line 108**: "Scores sessions by keyword frequency" - specify if this includes stop word removal, stemming, or normalization
2. **Line 122**: "50 questions from 442 available" - explain sampling strategy (random? stratified by difficulty?)
3. **Table 1**: Add error bars or at least mention sample size in caption
4. **Figure 1**: Cost-accuracy plot would benefit from error bars and Pareto frontier line
5. **Section 4.2**: The four hypotheses are never revisited in conclusion or future work
6. **Missing**: No discussion of when embeddings DID work (were there any questions where Stella V5 succeeded but keyword failed?)

---

## Relation to Prior Work

### Well-Cited
- LongMemEval benchmark properly cited
- Dense retrieval work (DPR, ColBERT, BEIR) covered
- MemGPT and Letta systems mentioned

### Missing Citations

1. **Recent Agent Memory Surveys**:
   - [Memory in the Age of AI Agents (Dec 2024)](https://arxiv.org/abs/2512.13564) - comprehensive survey distinguishing agent memory from RAG
   - [Survey on Memory Mechanism of LLM-based Agents](https://dl.acm.org/doi/10.1145/3748302) - covers ReAct and memory retrieval

2. **Recent Agent Memory Systems (2024)**:
   - [MemR3 (Dec 2024)](https://arxiv.org/html/2512.20237v1) - reflective reasoning for memory retrieval
   - [Hindsight (Dec 2024)](https://arxiv.org/html/2512.12818v1) - agent memory with retain/recall/reflect
   - Both use LoCoMo benchmark and report results you could compare against

3. **Hybrid Retrieval Literature**:
   - [Systematic Review of RAG Systems (2024)](https://arxiv.org/html/2507.18910v1) - covers hybrid retrieval extensively
   - Standard fusion techniques (RRF, weighted scoring) not mentioned

4. **MTEB and Embedding Evaluation**:
   - [MTEB Leaderboard article](https://modal.com/blog/mteb-leaderboard-article) - context for Stella V5 performance
   - [Jasper and Stella distillation paper (Dec 2024)](https://arxiv.org/html/2412.19048v2)

---

## Overall Assessment

### Contribution
The paper makes an important empirical observation: keyword search dramatically outperforms dense embeddings in an agentic conversational memory setting. This challenges assumptions from static benchmarks and has immediate practical value.

However, the contribution is weakened by:
1. **Limited scale** (50/500 questions) without statistical analysis
2. **Missing baselines** from 2024 literature (MemR3, Hindsight, proper BM25)
3. **No mechanistic understanding** of WHY embeddings fail
4. **Potentially suboptimal implementation** (frequency counting, hybrid approach)

### Originality
**Moderate**. The idea of evaluating static retrieval methods in agentic settings is relatively novel, and the negative result on dense embeddings is surprising. However:
- LongMemEval benchmark already exists (paper extends it to agentic setting)
- Letta already showed filesystem approaches can work (74% on LoCoMo)
- MemR3 and Hindsight (both Dec 2024) are concurrent work on agent memory evaluation

The contribution is more empirical than conceptual.

### Clarity
**Good**. Paper is well-written and easy to follow. Figures are clear. Limitations section is honest. Main results are unambiguous.

### Soundness
**Weak**. Major concerns:
- Sample size too small for confident conclusions
- Missing critical baselines (proper BM25, other embeddings, recent agent memory systems)
- No statistical significance testing
- Hypotheses stated but not tested
- Hybrid implementation may not represent best practices

### Significance
**Moderate-to-High IF issues are addressed**. The finding could influence how practitioners design agent memory systems. However, without understanding WHY embeddings fail and testing proper baselines, the takeaway is unclear:
- Is it dense embeddings generally, or Stella V5 specifically?
- Is it hybrid approaches generally, or this implementation?
- Is it 50 questions representative, or sampling noise?

---

## Recommendation: **3 (Weak Accept / Borderline)**

### Reasoning
This paper tackles an important problem (evaluating memory for agents) and reports a striking empirical finding (keyword >> dense embeddings). The experimental setup is reasonable and results are clearly presented.

However, **critical weaknesses prevent a strong accept**:
1. Sample size (50/500 questions) is too small without statistical analysis
2. Missing recent baselines (MemR3, Hindsight, proper BM25)
3. No mechanistic explanation for the findings
4. Potential implementation issues (frequency counting vs. BM25, hybrid approach)

**Path to acceptance:**
- **Essential**: Scale to at least 200 questions OR add confidence intervals + significance tests
- **Essential**: Implement proper BM25 (not frequency counting)
- **Highly recommended**: Test one other embedding model (BGE or E5)
- **Highly recommended**: Add 2-3 ablations to test hypotheses (session chunking, error analysis)
- **Recommended**: Compare/cite MemR3 and Hindsight results

With these changes, this would be a solid accept (4). As written, it's a borderline paper with valuable findings but incomplete evaluation.

### Positioning
This is a **negative result** paper that challenges conventional wisdom. Such papers have high value when:
1. The finding is robust (needs more data)
2. Alternative explanations are ruled out (needs more baselines)
3. The mechanism is understood (needs ablations)

Currently, point 1 is questionable and points 2-3 are missing. With revisions, this could be a strong contribution to the agent memory literature.

---

## Confidence: **4 (Confident)**

I am familiar with recent work on agent memory systems (LongMemEval, LoCoMo, MemR3, Hindsight), retrieval evaluation (MTEB, BEIR), and hybrid retrieval systems. I have high confidence in identifying the missing baselines and methodological concerns. I am slightly less confident about the statistical requirements (borderline whether 50 questions with proper analysis would suffice), but the other concerns are clear.

---

## Suggestions for Improvement

### Short-term (for revision):
1. Scale to 200 questions (~$30 additional cost based on current spend)
2. Implement proper BM25 with IDF weighting
3. Add confidence intervals to all results
4. Test BGE-large or E5-large embedding model
5. Provide detailed error analysis by question type
6. Cite and compare with MemR3/Hindsight

### Long-term (for follow-up work):
1. Test multiple agent architectures (ReAct, Plan-and-Solve, Tree-of-Thoughts)
2. Ablate session length, chunking strategies
3. Test with Claude, Gemini, open-source LLMs
4. Evaluate on LoCoMo for cross-benchmark validation
5. Implement and test alternative hybrid fusion methods
6. Study when embeddings DO help (paraphrased queries, conceptual questions)

---

## Sources Cited in Review

### Agent Memory Systems:
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)
- [MemR3: Memory Retrieval via Reflective Reasoning](https://arxiv.org/html/2512.20237v1)
- [Hindsight: Agent Memory that Retains, Recalls, and Reflects](https://arxiv.org/html/2512.12818v1)
- [Survey on Memory Mechanism of LLM-based Agents](https://dl.acm.org/doi/10.1145/3748302)

### Benchmarks:
- [LongMemEval: Benchmarking Chat Assistants on Long-Term Memory (ICLR 2025)](https://arxiv.org/abs/2410.10813)
- [LoCoMo: Evaluating Very Long-Term Conversational Memory](https://snap-research.github.io/locomo/)
- [Letta's Benchmarking AI Agent Memory](https://www.letta.com/blog/benchmarking-ai-agent-memory)
- [AgentArch: Comprehensive Benchmark for Agent Architectures](https://arxiv.org/html/2509.10769v1)

### Retrieval Methods:
- [Hybrid Retrieval: Combining Sparse and Dense Methods](https://mbrenndoerfer.com/writing/hybrid-retrieval-combining-sparse-dense-methods-effective-information-retrieval)
- [Advanced RAG: Hybrid Search and Re-ranking](https://dev.to/kuldeep_paul/advanced-rag-from-naive-retrieval-to-hybrid-search-and-re-ranking-4km3)
- [Systematic Review of RAG Systems](https://arxiv.org/html/2507.18910v1)
- [MTEB Leaderboard and Stella V5 Performance](https://modal.com/blog/mteb-leaderboard-article)
- [Jasper and Stella: Distillation of SOTA Embedding Models](https://arxiv.org/html/2412.19048v2)

---

**End of Review**
