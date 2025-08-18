# Paper build guide

This directory contains a LaTeX paper skeleton for the project on advanced numerical optimization.

## Compile (locally)
- Preferred: latexmk
  - `latexmk -pdf main.tex`
- Or, manual sequence:
  - `pdflatex main.tex`
  - `bibtex main`
  - `pdflatex main.tex`
  - `pdflatex main.tex`

If you do not have TeX Live installed, we recommend using Overleaf.

## Overleaf
Upload the contents of `paper/` into a new Overleaf project and click Recompile.

## Matching formatting requirements
The current template uses: 12pt, Times-like fonts, 1 inch margins, 1.5 line spacing, numeric citations. If `AdvPSE_Final_14032.pdf` specifies different properties (e.g., double spacing, specific bibliography style, page limits), update `main.tex` accordingly (geometry, setspace, bibliography style) and recompile.

## Structure
- `main.tex` includes all sections from `sections/`
- `references.bib` holds citations
- You can add figures under `figures/`

## Notes
- Replace author, title, and abstract with final versions
- Fill in or revise each section in `sections/` as needed
- Ensure all references in text are in `references.bib`