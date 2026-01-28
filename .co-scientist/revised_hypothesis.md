# Revised Hypothesis - Iteration 2

## Original Claims (Pre-Review)
- "keyword search (62%) **vastly outperformed** dense embeddings (26%)"
- Implied: This is a robust, generalizable finding

## Revised Claims (Post-Review)

### Primary Finding (Softened)
**H1-Revised:** In this pilot evaluation of 50 LongMemEval questions, frequency-based keyword search (62% [47-75%]) substantially outperformed dense embeddings (Stella V5, 26% [15-40%]), though the effect requires validation at larger scale.

### Statistical Framing
- Report 95% Wilson confidence intervals (already done)
- Add McNemar's test for paired comparison
- Report effect size (Cohen's h)
- Acknowledge overlapping CIs due to sample size

### Key Limitations to Emphasize
1. **Sample size:** 50/500 questions (10%) - pilot study
2. **Keyword implementation:** Frequency counting, not proper BM25
3. **Single embedding model:** Stella V5 only
4. **Single agent architecture:** ReAct with 5 iterations

### What We CAN Claim
1. In this setting, keyword search outperformed dense embeddings
2. The effect size is large (36 percentage points, Cohen's h = 0.76)
3. Static benchmark performance (71%) did not translate to agentic setting (26%)
4. Retrieval quality is the bottleneck (Oracle 90% vs best practical 62%)

### What We CANNOT Claim
1. This generalizes to all conversational QA
2. Dense embeddings universally fail in agentic settings
3. Proper BM25 would perform similarly to our frequency counting
4. Other embedding models (BGE, E5) would fail similarly

## Success Criteria for Revised Paper
- Abstract accurately reflects limitations
- Claims are qualified with confidence intervals
- Methodology section clearly describes frequency counting (not BM25)
- Discussion acknowledges this as pilot study requiring replication
