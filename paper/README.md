# ICML Paper Submission Package

## Title
**Do Memory Tools Help Agents? The Surprising Failure of Dense Retrieval**

## Files Included

- `paper.tex` - Main LaTeX source
- `refs.bib` - Bibliography
- `figures/` - All 3 figures (PNG format)
  - `cost_accuracy_tradeoff.png`
  - `method_comparison.png`
  - `per_question_heatmap.png`

## Compilation Instructions

### Option 1: Overleaf (Easiest)
1. Go to https://www.overleaf.com
2. Create new project → Upload Project
3. Upload this entire `paper/` directory
4. Compile (should work out of the box)

### Option 2: Local LaTeX
```bash
cd paper
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

### Option 3: Online Compilers
- https://latexbase.com
- https://www.latex4technics.com
- Upload paper.tex and refs.bib

## Paper Statistics

- **Pages**: ~6-7 (with figures)
- **Figures**: 3 (all included)
- **References**: 10 citations
- **Word Count**: ~2,500 words

## Submission Checklist

- [x] LaTeX source (paper.tex)
- [x] Bibliography (refs.bib)
- [x] All figures in high resolution
- [x] Anonymized (no author names)
- [x] ICML format compliance
- [ ] Compile to PDF
- [ ] Check page limit (8 pages for ICML)
- [ ] Add supplementary materials if needed

## Key Contributions

1. **LME+ benchmark**: Agentic adaptation of LongMemEval
2. **Surprising negative results**: Dense embeddings fail (26% vs 62% keyword)
3. **Hybrid failure**: Combining approaches makes it worse (42%)
4. **Retrieval bottleneck**: 28pp gap identifies core limitation

## Contact

For questions about this submission, see the anonymous repository or contact through ICML submission system.
