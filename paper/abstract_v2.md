# Revised Abstract Options

## Option 1: Conservative Framing (Recommended for abstract deadline)

**Do Memory Tools Help Agents? Evaluating Retrieval Methods in Agentic Settings**

Memory systems for AI agents are typically evaluated on static retrieval benchmarks, where dense embeddings consistently outperform keyword search. But do these gains transfer when agents iteratively query memory tools? We introduce **LME+**, an agentic adaptation of the LongMemEval benchmark, where a ReAct agent (GPT-4o) actively queries memory tools to answer conversational QA questions. In a pilot study of 50 questions, we compare five retrieval approaches: Oracle (perfect retrieval), frequency-based keyword matching, dense embeddings (Stella V5), filesystem browsing, and a keyword-then-embedding hybrid.

Our results reveal a striking reversal: **frequency-based keyword matching (62% [47-75% CI]) substantially outperformed dense embeddings (26% [15-40% CI])**, despite Stella V5 achieving 71% on the static LongMemEval benchmark. The hybrid approach (42%) performed worse than keyword search alone, suggesting embedding-based reranking may demote relevant results in this setting. Oracle performance (90%) identifies retrieval quality as the primary bottleneck over agent architecture.

**Limitations and future work:** Our pilot study uses 50 of 500 available questions, frequency counting rather than full BM25, and a single embedding model. We report 95% confidence intervals but acknowledge overlapping ranges due to sample size. Ongoing work scales to 200+ questions, implements proper BM25, tests additional embedding models (BGE, E5), and adds statistical significance testing. These results motivate deeper investigation into why dense embeddings underperform in agentic retrieval settings.

---

## Option 2: Methodology-Focused Framing

**LME+: A Benchmark for Evaluating Memory Systems in Agentic Settings**

Static retrieval benchmarks evaluate memory systems by measuring whether relevant documents appear in top-k results. However, AI agents use memory dynamically—issuing multiple queries, reformulating based on results, and iterating until success. We introduce **LME+**, an agentic benchmark that evaluates memory tools by measuring end-to-end question-answering accuracy when a ReAct agent actively queries them.

Using LME+ on 50 LongMemEval questions, we find that **retrieval method rankings reverse in agentic settings**: frequency-based keyword matching (62%) outperformed dense embeddings (26%) and their hybrid combination (42%), despite dense embeddings achieving state-of-the-art performance on static benchmarks. Oracle analysis (90% accuracy) confirms retrieval quality, not agent architecture, as the primary limitation.

We release LME+ as a framework for evaluating memory systems under realistic agent usage patterns. Our pilot results, while preliminary, suggest that static benchmark performance may not predict agentic performance, warranting further investigation with larger samples, additional retrieval methods, and mechanistic analysis.

---

## Option 3: Research Questions Framing

**Does Static Retrieval Performance Translate to Agentic Gains? A Pilot Study**

Dense embedding models dominate static retrieval benchmarks, with models like Stella V5 achieving 71% on LongMemEval. But when agents iteratively query these systems—reformulating queries, exploring results, and adapting to failures—do these advantages persist?

We present a pilot study using **LME+**, an agentic adaptation of LongMemEval where a ReAct agent queries memory tools to answer conversational QA questions. Across 50 questions, we evaluate Oracle retrieval, frequency-based keyword matching, dense embeddings (Stella V5), filesystem access, and a hybrid approach.

**Key findings:** (1) Keyword matching (62% [47-75% CI]) substantially outperformed dense embeddings (26% [15-40% CI]); (2) Hybrid retrieval (42%) performed worse than keyword alone; (3) Oracle (90%) establishes a 28-point gap between perfect retrieval and best practical method.

These preliminary results challenge the assumption that static retrieval gains transfer to agentic settings. We discuss limitations (sample size, implementation choices) and ongoing work to validate findings at larger scale with additional baselines.

---

## Key Changes from Original Abstract

| Aspect | Original | Revised |
|--------|----------|---------|
| Framing | Claims "vastly outperformed" | Uses "substantially outperformed" with explicit CIs |
| Scale | States "50 questions" without context | Frames as "pilot study of 50 questions" |
| Keyword method | Implies BM25 | Explicitly states "frequency-based keyword matching" |
| Confidence | Strong claims | Reports confidence intervals, acknowledges overlap |
| Limitations | Mentioned at end | Integrated throughout, dedicated section |
| Future work | Absent | Explicitly previewed (scaling, BM25, other embeddings) |

## Word Counts
- Option 1: 289 words
- Option 2: 227 words
- Option 3: 241 words
- Original: 196 words

## Recommendation

**Option 1** is most appropriate for abstract deadline because:
1. Most honest about what we actually did (frequency counting, not BM25)
2. Most explicit about limitations and ongoing work
3. Still conveys the interesting finding while being defensible
4. Previews improvements coming before full paper deadline

The key insight: frame this as "pilot results that motivate deeper investigation" rather than "definitive conclusion about dense embeddings."
