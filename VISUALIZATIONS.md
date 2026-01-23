# Results Visualizations

## Overview

Three key visualizations summarizing the LME+ experiment results:

---

## 1. Method Comparison: Accuracy & Cost

**File:** `results/method_comparison.png`

**Shows:**
- Accuracy comparison across all 4 methods (Oracle, MCP, Filesystem, Stella V5)
- Cost comparison (USD for 50 questions)
- Target threshold (67%) marked with red dashed line

**Key Insights:**
- Oracle achieves 90% accuracy at lowest cost ($0.44)
- MCP (keyword search) reaches 62% at highest cost ($1.62)
- Stella V5 (dense retrieval) catastrophically fails at 26%
- Filesystem without search achieves 32%

---

## 2. Per-Question Correctness Heatmap

**File:** `results/per_question_heatmap.png`

**Shows:**
- Green = Correct answer
- Red = Incorrect answer
- Each row = one method
- Each column = one question (1-50)

**Key Insights:**
- Oracle has consistent green (few failures)
- MCP shows patchy green (moderate success)
- Filesystem and Stella V5 are mostly red (high failure rates)
- Some questions are hard for all methods (vertical red bands)
- Some questions are easy for all methods (vertical green bands)

**Pattern Analysis:**
- Questions 1-20: Oracle and MCP perform well
- Questions 21-40: Performance degrades across all methods
- Questions 41-50: Slight recovery for Oracle/MCP

---

## 3. Cost-Accuracy Tradeoff

**File:** `results/cost_accuracy_tradeoff.png`

**Shows:**
- X-axis: Cost (USD for 50 questions)
- Y-axis: Accuracy (%)
- Each point = one method
- Ideal position: Top-left (high accuracy, low cost)

**Key Insights:**
- **Oracle (top-left)**: Winner! 90% accuracy @ $0.44
- **MCP (top-right)**: Good accuracy (62%) but expensive ($1.62)
- **Filesystem (bottom-left)**: Cheap ($0.35) but poor (32%)
- **Stella V5 (bottom-middle)**: Worst performer - 26% @ $0.82

**Efficiency Ranking:**
1. Oracle: 204% accuracy per dollar
2. Filesystem: 91% accuracy per dollar
3. MCP: 38% accuracy per dollar
4. Stella V5: 32% accuracy per dollar

---

## Recommendations from Visualizations

### For Memory Tool Designers

1. **Prioritize keyword search over dense embeddings**
   - MCP (62%) vastly outperforms Stella V5 (26%)
   - Dense retrieval is NOT a silver bullet

2. **Optimize for cost efficiency**
   - MCP is 3.7x more expensive than Oracle
   - Consider compression or adaptive top-k

3. **Semantic search is essential**
   - Both Filesystem (32%) and Stella V5 (26%) fail
   - Even simple keyword search (MCP 62%) is far better

### For Researchers

1. **Focus on retrieval quality**
   - 28pp gap between Oracle (90%) and MCP (62%)
   - This is the main bottleneck, not agent architecture

2. **Test on actual use cases**
   - Stella V5 excels on static benchmarks
   - But fails catastrophically on agentic retrieval
   - Domain and task matter!

3. **Consider cost-accuracy tradeoffs**
   - Higher cost doesn't guarantee better performance
   - MCP costs 3.7x Oracle for 28pp less accuracy

---

## Reproduction

All visualizations generated from raw results in `results/` directory:
- `results/node_4_oracle_50/`
- `results/node_6_builtin_mcp_50/`
- `results/node_5_filesystem_50/`
- `results/node_10_stella_v5_50/`

To regenerate, run:
```bash
python3 scripts/create_visualizations.py
```

Or use the inline matplotlib code in git commit history.
