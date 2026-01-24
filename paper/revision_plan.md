# Paper Revision Plan Based on ICML Review

## Review Summary
**Overall Score**: 3 (Weak Accept / Borderline)
**Confidence**: 4 (Confident)

**Main Issues**:
1. Limited scale (50/500 questions) without statistical analysis
2. Missing critical recent baselines (MemR3, Hindsight, proper BM25)
3. No mechanistic explanation for WHY embeddings fail
4. Potentially suboptimal implementations

---

## Priority 1: Essential Changes (Required for Acceptance)

### 1.1 Add Statistical Analysis
**Issue**: 50/500 questions insufficient for confident conclusions
**Action**:
- [ ] Calculate 95% confidence intervals for all accuracy scores
- [ ] Perform McNemar's test for pairwise method comparisons
- [ ] Add error bars to Figure 1 (cost-accuracy tradeoff)
- [ ] Add statistical significance markers to Table 1

**Files to modify**:
- `paper.tex` - Add confidence intervals to tables and text
- Need to calculate from existing results

---

### 1.2 Implement Proper BM25
**Issue**: Current implementation uses raw frequency counting, not proper BM25
**Action**:
- [ ] Implement BM25 with IDF weighting and length normalization
- [ ] Re-run experiments with proper BM25
- [ ] Compare frequency counting vs. proper BM25
- [ ] Update Section 3.2 to specify implementation details

**Expected Impact**: BM25 typically 5-15% better than raw frequency

---

### 1.3 Add Missing Literature
**Action**:
- [ ] Add citations to refs.bib:
  - MemR3 (Dec 2024) - arxiv 2512.20237
  - Hindsight (Dec 2024) - arxiv 2512.12818
  - Memory in Age of AI Agents survey (Dec 2024) - arxiv 2512.13564
  - Hybrid retrieval survey (2024) - arxiv 2507.18910
  - MTEB leaderboard discussion
- [ ] Update Related Work section with these papers
- [ ] Add comparison discussion in Results section

---

## Priority 2: Highly Recommended Changes

### 2.1 Test Additional Embedding Model
**Issue**: Only Stella V5 tested; unclear if findings generalize
**Action**:
- [ ] Implement BGE-large or E5-large embeddings
- [ ] Run on same 50 questions
- [ ] Compare results to Stella V5
- [ ] Update tables and discussion

**Expected Cost**: ~$1-2 for 50 questions

---

### 2.2 Error Analysis and Ablations
**Issue**: Four hypotheses stated but none tested
**Action**:
- [ ] **H1 (Session Length)**: Chunk sessions into 10-turn segments, compare performance
- [ ] **H3 (Lexical vs Semantic)**: Categorize failures by whether they involve:
  - Rare/specific terms (names, dates, technical terms)
  - vs. conceptual understanding
- [ ] Add new subsection: "Mechanistic Analysis" with ablation results
- [ ] Include failure case examples by category

---

### 2.3 Verify Baseline Assumptions
**Action**:
- [ ] Confirm Stella V5 achieves 71% on static LongMemEval
- [ ] Run Stella V5 on static retrieval (no agent) to verify model works correctly
- [ ] Report this validation in paper

---

### 2.4 Improve Hybrid Implementation
**Issue**: Current hybrid may be suboptimal
**Action**:
- [ ] Test alternative fusion method: Reciprocal Rank Fusion (RRF)
- [ ] Test: keyword + dense in parallel, then fuse (rather than cascade)
- [ ] Compare to current hybrid approach
- [ ] Clarify that results are for one specific hybrid design

---

## Priority 3: Recommended Changes

### 3.1 Clarify Letta Comparison
**Issue**: Misleading comparison to LoCoMo results
**Action**:
- [ ] Rewrite Related Work paragraph to clarify:
  - LoCoMo is structured extraction, different from our unstructured search
  - Letta used file-based context management, not filesystem search tools
  - Different datasets, agents, LLMs
- [ ] Remove direct 74% vs 32% comparison or explain differences

---

### 3.2 Add Retrieval Metrics
**Action**:
- [ ] Calculate retrieval precision/recall separately from end-to-end accuracy
- [ ] Report: what % of top-3 retrieved sessions contain the answer?
- [ ] This isolates retrieval quality from agent reasoning

---

### 3.3 Analyze Oracle Ceiling
**Action**:
- [ ] Categorize the 10% Oracle failures:
  - Agent reasoning errors
  - Judge strictness (rejected valid paraphrases)
  - Ambiguous/unanswerable questions
- [ ] Add analysis to Section 4.1

---

### 3.4 Minor Fixes
- [ ] Line 108: Specify keyword normalization (stop words, stemming, case)
- [ ] Line 122: Explain sampling strategy for 50/500 questions
- [ ] Add sample size to all table captions
- [ ] Revisit H1-H4 hypotheses in Conclusion/Future Work
- [ ] Add discussion of when embeddings DID work (if any cases)

---

## Text Changes Needed

### Abstract
- Add: "with 95% confidence intervals of ±X"
- Clarify: "simple frequency-based keyword search" (not BM25)

### Introduction
- Add confidence intervals to main results

### Section 3.2 (Memory Adapters)
- **MCP paragraph**: Specify full implementation details
  - Stop word removal? No
  - Stemming? No
  - Case normalization? Yes
  - IDF weighting? No (raw frequency)

### Section 4.2 (Analysis)
- Rename to "Analysis and Ablations"
- Add subsections for each tested hypothesis
- Add error analysis by question type

### Related Work
- Add new paragraph on "Recent Agent Memory Systems (2024)"
- Cite MemR3, Hindsight, Memory survey
- Clarify Letta/LoCoMo comparison

### Discussion
- Add paragraph: "When Do Embeddings Help?"
- Report any cases where Stella V5 succeeded but keyword failed

### Limitations
- Add: "Our keyword search uses frequency counting rather than proper BM25"
- Add: "Statistical analysis limited by 50-question sample size"

---

## Timeline Estimate

**Immediate (can do now)**:
- Statistical analysis: 1-2 hours (calculate from existing results)
- Literature additions: 1 hour
- Text clarifications: 2 hours
- **Total: 4-5 hours**

**Short-term (requires new experiments)**:
- BM25 implementation: 2-3 hours
- BGE/E5 embeddings: 2 hours setup + $1-2 + 1 hour analysis
- Session chunking ablation: 2-3 hours
- Error analysis: 2-3 hours
- **Total: 8-11 hours + ~$2**

**Optional (improves paper significantly)**:
- Scale to 200 questions: ~$30 + 4 hours analysis
- Alternative hybrid (RRF): 3-4 hours
- Retrieval metrics: 2-3 hours
- **Total: 9-11 hours + $30**

---

## Recommended Immediate Actions

1. **Statistical Analysis** (Priority 1.1) - No cost, immediate improvement
2. **Literature Updates** (Priority 1.3) - No cost, addresses critical gap
3. **Clarify Letta Comparison** (Priority 3.1) - No cost, fixes misrepresentation
4. **BM25 Implementation** (Priority 1.2) - Low cost, addresses major concern

After these, reassess whether paper is strong enough or needs:
- Additional embedding model (Priority 2.1)
- Session length ablation (Priority 2.2)
- Scale to 200 questions (optional but impactful)

---

## Success Criteria

**Minimum for acceptance**:
- ✓ Statistical analysis with confidence intervals
- ✓ Proper BM25 implementation
- ✓ Updated literature citations
- ✓ Clarified methodology details

**Strong accept**:
- Above + one additional embedding model
- Above + 2-3 ablations testing hypotheses
- Above + scaled to 200+ questions

