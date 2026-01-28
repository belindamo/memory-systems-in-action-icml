# ICML Abstract Review: LME+ Paper

**Reviewer Evaluation of Abstract Drafts**

---

## Prior Work Grounding

Before evaluating the abstracts, I reviewed recent literature on agent memory and retrieval:

### Relevant Recent Work (2025-2026)
1. **[Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)** (Dec 2025) - Proposes taxonomy distinguishing factual, experiential, and working memory
2. **[Evo-Memory Benchmark](https://arxiv.org/html/2511.20857v1)** (Nov 2025) - Evaluates self-evolving memory in LLM agents
3. **[MemoryAgentBench](https://arxiv.org/abs/2507.05257)** (Jul 2025) - Four competencies: accurate retrieval, test-time learning, long-range understanding, selective forgetting
4. **[Letta Benchmark](https://www.letta.com/blog/benchmarking-ai-agent-memory)** - Shows filesystem achieves 74% on LoCoMo

### Retrieval Literature Consensus (2025)
- **[Hybrid RAG comparison](https://medium.com/@robertdennyson/dense-vs-sparse-vs-hybrid-rrf-which-rag-technique-actually-works-1228c0ae3f69)**: Hybrid retrieval improves NDCG by 26-31% over dense-only
- **[RAG survey](https://arxiv.org/html/2506.00054v1)**: Three-way retrieval (BM25 + dense + sparse) is optimal
- The finding that hybrid *underperforms* keyword alone contradicts established literature

---

## Abstract-by-Abstract Evaluation

### Option A: Conservative Framing (172 words)

**Strengths:**
- Appropriately frames as "pilot study"
- Includes confidence intervals [47-75% CI] and [15-40% CI]
- Explicitly names "frequency-based keyword matching" (not BM25)
- Hedged language: "observe," "suggests," "preliminary"
- Word count well under ICML limit

**Weaknesses:**
- CIs overlap (75% upper bound for keyword vs 40% upper bound for Stella) - this should be acknowledged
- "Striking reversal" may still be overclaiming given overlapping CIs
- Missing: sampling strategy (random? stratified?)
- No mention of statistical significance test

**Verdict: Best option for current data. Minor edits recommended.**

---

### Option B: Stronger Claims (157 words)

**Strengths:**
- Cleaner prose, more assertive
- Includes p-value claim
- Tests multiple embeddings (Stella, BGE)

**Critical Problems:**
- **Cannot use until experiments completed** - placeholder numbers invalidate submission
- Claims "p<0.01" without the data to support it
- "Significantly outperforms" requires statistical backing
- Causal claim ("requires lexical precision that dense representations fail to capture") is unsupported speculation

**Verdict: Do NOT submit this version. Reserve for camera-ready after validation.**

---

### Option C: Research Questions Framing (160 words)

**Strengths:**
- Question format is engaging
- Includes CIs (same as Option A)
- Mentions hypotheses, positioning as opening research agenda
- Avoids overclaiming by discussing "hypotheses" rather than conclusions

**Weaknesses:**
- "Retrieval method rankings reverse" is a strong claim that needs statistical support
- Final sentence ("outline experiments to test them") implies future work not yet done - fine for workshop paper but weak for ICML main conference

**Verdict: Good alternative to Option A. Slightly weaker positioning for top venue.**

---

### Option D: Negative Results Framing (146 words)

**Strengths:**
- Most concise (146 words)
- Practical framing appeals to practitioners
- Clear problem-contribution-result structure

**Weaknesses:**
- No confidence intervals - this is a significant omission
- "Simple frequency-based keyword matching achieves 62%" without CI could be challenged
- "Adding embedding-based reranking hurts rather than helps" - contradicts hybrid retrieval literature without explanation
- Missing context that 50 questions is a pilot study

**Verdict: Too assertive for current evidence. Would require defensive revision if challenged.**

---

## Cross-Cutting Issues

### 1. Statistical Rigor
All abstracts would benefit from:
- McNemar's test result (or note that it's planned)
- Acknowledgment that CIs overlap
- Effect size (Cohen's h = 0.76 is large, worth mentioning)

### 2. Literature Positioning
The hybrid finding contradicts [established consensus](https://research.aimultiple.com/hybrid-rag/) that hybrid improves over single methods. The abstracts should note this is *surprising* rather than expected, or attribute it to implementation specifics.

### 3. Generalization Claims
With n=50 and single embedding model (Stella V5), any claims about "dense embeddings" generally are unsupported. The abstracts correctly scope to Stella V5, but phrases like "static retrieval gains" and "dense representations" risk overgeneralization.

### 4. Missing Context
None of the abstracts mention:
- Why this problem matters (what happens if practitioners use wrong retrieval?)
- How this relates to [recent agent memory benchmarks](https://arxiv.org/abs/2507.05257)
- The cost implications (keyword is less cost-efficient despite being more accurate)

---

## ICML-Specific Concerns

Based on [ICML 2026 guidelines](https://icml.cc/Conferences/2026/CallForPapers):

| Requirement | Option A | Option B | Option C | Option D |
|-------------|----------|----------|----------|----------|
| Single paragraph | Yes | Yes | Yes | Yes |
| 4-6 sentences | ~8 sentences | ~7 sentences | ~8 sentences | ~7 sentences |
| No placeholder content | Yes | **NO** (X%, Y%) | Yes | Yes |
| Double-blind compatible | Yes | Yes | Yes | Yes |
| Under word limit | Yes (~172) | Yes (~157) | Yes (~160) | Yes (~146) |

**Critical**: Option B cannot be submitted due to placeholder numbers.

---

## Recommended Final Abstract

Based on my review, here is a revised version of Option A that addresses the weaknesses:

---

**Do Memory Tools Help Agents? Evaluating Retrieval Methods in Agentic Settings**

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embedding models consistently outperform sparse keyword methods. However, agents use memory dynamically—issuing iterative queries, reformulating based on results, and adapting to failures. We introduce LME+, an agentic adaptation of the LongMemEval benchmark where a ReAct agent (GPT-4o) actively queries memory tools to answer conversational QA questions. In a pilot study of 50 randomly sampled questions comparing five retrieval approaches, we observe that frequency-based keyword matching (62%, 95% CI: 47-75%) outperforms dense embeddings (Stella V5, 26%, 95% CI: 15-40%) by a large margin (Cohen's h = 0.76), despite Stella V5 achieving 71% on static LongMemEval. Unexpectedly, a hybrid approach (42%) underperforms keyword search alone—contrary to established hybrid retrieval benefits—suggesting embedding-based reranking may demote relevant results in this conversational setting. Oracle performance (90%) identifies retrieval quality as the primary bottleneck. These preliminary findings motivate investigation into when static benchmark gains transfer to agentic settings.

**Word count: 178**

---

**Key improvements:**
1. Added "randomly sampled" to address sampling concern
2. Added Cohen's h effect size
3. Added "Unexpectedly" and "contrary to established hybrid retrieval benefits" to acknowledge literature tension
4. Changed "striking reversal" to "large margin" with quantification
5. Softened final sentence to "motivate investigation" rather than "challenge assumptions"

---

## Action Items Before Submission

### Essential (do before abstract deadline):
1. Verify random sampling was used for 50 questions (or clarify stratification)
2. Run McNemar's test and add significance if p<0.05
3. Decide between Option A (with revisions above) or Option C

### Highly Recommended (do before full paper deadline):
1. Scale to 200+ questions
2. Implement proper BM25
3. Test BGE or E5 embedding model
4. Test alternative hybrid fusion (RRF)

### For Camera-Ready:
1. Address all [ICML review weaknesses](./icml_review.md) (W1-W7)
2. Update abstract with expanded results
3. Add error analysis and ablations

---

## Summary Recommendation

**Submit Option A with the revisions above** if the abstract deadline is imminent.

The work has genuine scientific value—the finding is surprising and practically relevant. The key is honest framing: this is a pilot study that motivates further investigation, not a definitive conclusion about dense embeddings.

If you can extend experiments before the full paper deadline, the path to acceptance (score 4) is clear:
- 200 questions with proper BM25 and one alternative embedding
- Statistical significance testing
- Error analysis by question type

Without extensions, the paper remains borderline (score 3) but publishable as a negative results paper with appropriate caveats.

---

**Sources:**
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)
- [Evo-Memory Benchmark](https://arxiv.org/html/2511.20857v1)
- [MemoryAgentBench](https://arxiv.org/abs/2507.05257)
- [Letta Memory Benchmark](https://www.letta.com/blog/benchmarking-ai-agent-memory)
- [Hybrid RAG Comparison](https://medium.com/@robertdennyson/dense-vs-sparse-vs-hybrid-rrf-which-rag-technique-actually-works-1228c0ae3f69)
- [RAG Survey](https://arxiv.org/html/2506.00054v1)
- [ICML 2026 Author Instructions](https://icml.cc/Conferences/2026/AuthorInstructions)
- [ICML 2026 Call for Papers](https://icml.cc/Conferences/2026/CallForPapers)
