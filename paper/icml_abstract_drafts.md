# ICML 2026 Abstract Drafts

**Paper Title Options:**
1. "Do Memory Tools Help Agents? Evaluating Retrieval Methods in Agentic Settings"
2. "When Dense Retrieval Fails: Memory Tool Evaluation for LLM Agents"
3. "LME+: Benchmarking Memory Systems Under Agentic Retrieval"

---

## Option A: Conservative Framing (Current 50-Question Results)

**Recommended if submitting with current data. Frames as pilot study.**

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embedding models consistently outperform sparse keyword methods. However, agents use memory dynamically—issuing iterative queries, reformulating based on results, and adapting to failures. We introduce LME+, an agentic adaptation of the LongMemEval benchmark where a ReAct agent (GPT-4o) actively queries memory tools to answer conversational QA questions. In a pilot study of 50 questions comparing five retrieval approaches—Oracle, frequency-based keyword matching, dense embeddings (Stella V5), filesystem access, and keyword-then-embedding hybrid—we observe a striking reversal: keyword matching (62% [47-75% CI]) substantially outperforms dense embeddings (26% [15-40% CI]), despite Stella V5 achieving 71% on static LongMemEval. The hybrid approach (42%) underperforms keyword search alone, suggesting embedding-based reranking may demote relevant results. Oracle performance (90%) identifies retrieval quality as the primary bottleneck over agent architecture. These preliminary findings challenge assumptions that static retrieval gains transfer to agentic settings and motivate investigation into retrieval method selection for memory-augmented agents.

**Word count:** 172

---

## Option B: Stronger Claims (If Scaling to 200+ Questions)

**Use this version ONLY after running expanded experiments with proper BM25 and additional embedding models.**

Memory systems for LLM agents are typically evaluated on static retrieval benchmarks, where dense embeddings consistently outperform keyword search. We ask whether these gains transfer when agents iteratively query memory tools. We introduce LME+, an agentic adaptation of LongMemEval where a ReAct agent dynamically retrieves from conversational memory. Evaluating BM25, dense embeddings (Stella V5, BGE), filesystem browsing, and hybrid approaches across 200 questions, we find a striking reversal: BM25 (X%) significantly outperforms dense embeddings (Y%, p<0.01), despite the latter excelling on static benchmarks. Hybrid retrieval combining sparse and dense methods also underperforms BM25 alone, suggesting embeddings actively demote relevant results in this setting. Analysis reveals that conversational QA requires lexical precision that dense representations—trained primarily on document retrieval—fail to capture. Oracle experiments (90%) confirm retrieval quality as the primary bottleneck. Our findings suggest practitioners should reconsider default retrieval choices when building memory-augmented agents.

**Word count:** 157 (placeholder numbers: X%, Y%)**

---

## Option C: Research Questions Framing

**Positions work as opening a research agenda rather than definitive conclusions.**

Dense embedding models dominate static retrieval benchmarks, with models like Stella V5 achieving 71% on LongMemEval. But when agents iteratively query these systems—reformulating queries, exploring results, and adapting to failures—do these advantages persist? We present LME+, an agentic benchmark adaptation where a ReAct agent queries memory tools to answer conversational QA questions. Across 50 questions evaluating Oracle, keyword matching, dense embeddings, filesystem access, and hybrid retrieval, we observe that retrieval method rankings reverse in agentic settings: frequency-based keyword matching (62% [47-75% CI]) substantially outperforms dense embeddings (26% [15-40% CI]). Hybrid retrieval (42%) performs worse than keywords alone. Oracle analysis (90% accuracy) establishes a 28-point gap between perfect retrieval and the best practical method, identifying retrieval—not agent reasoning—as the primary limitation. We discuss hypotheses for why dense representations underperform (session length, training mismatch, lexical precision requirements) and outline experiments to test them.

**Word count:** 160

---

## Option D: Negative Results Framing

**Emphasizes the practical value of the negative finding.**

Practitioners building memory-augmented LLM agents often default to dense embedding models based on their strong performance on static retrieval benchmarks. We test whether this choice is justified in agentic settings. Using LME+, an agentic adaptation of LongMemEval, we evaluate how a ReAct agent performs when equipped with different memory retrieval tools: keyword search, dense embeddings (Stella V5), filesystem access, and hybrid approaches. Despite Stella V5 achieving 71% on static LongMemEval, it achieves only 26% when an agent iteratively queries it—while simple frequency-based keyword matching achieves 62%. Adding embedding-based reranking to keywords (hybrid, 42%) hurts rather than helps. Oracle experiments (90%) show that retrieval quality, not agent architecture, is the primary bottleneck. Our results suggest that static benchmark performance does not predict agentic performance, and that simpler retrieval methods may be preferable for conversational memory applications.

**Word count:** 146

---

## Recommendation for ICML Deadline

### If submitting NOW (with current 50-question data):
Use **Option A** or **Option C**. These:
- Frame work as "pilot study" appropriately
- Include confidence intervals (addressing W1)
- Use hedged language ("observe," "suggests," "preliminary")
- Explicitly mention sample size
- Set up future work rather than making definitive claims

### If you can run more experiments before deadline:
1. Scale to 200+ questions (~$30 additional)
2. Implement proper BM25 (not frequency counting)
3. Test BGE or E5 embeddings
4. Then use **Option B** with real numbers

---

## Key Reviewer Concerns to Address

From the ICML review (Score 3: Weak Accept):

| Weakness | How Abstract Addresses It |
|----------|---------------------------|
| W1: Limited scale (50/500) | Frame as "pilot study," include CIs |
| W2: Missing BM25 | Explicitly say "frequency-based keyword matching" |
| W2: Single embedding | Note "Stella V5" specifically, not generalizing |
| W3: No mechanistic analysis | Mention hypotheses as future work |
| W4: Letta comparison | Don't claim conflict, focus on own findings |

---

## Abstract Submission Checklist

- [ ] Word count under 250 words (ICML limit)
- [ ] No citations in abstract (per ICML guidelines)
- [ ] Includes: problem, method, key result, implication
- [ ] Confidence intervals for main result
- [ ] Honest about limitations
- [ ] No overclaims (avoid "vastly," "dramatically" without statistical backing)

---

## Title Recommendation

**"Do Memory Tools Help Agents? Evaluating Retrieval Methods in Agentic Settings"**

Reasons:
1. Question format invites reader curiosity
2. Clearly signals this is about agent memory (timely topic)
3. Doesn't overclaim (doesn't say "failure" or "surprising")
4. Matches the main research question
