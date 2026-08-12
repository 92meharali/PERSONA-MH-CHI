# PERSONA CHI 2027 Manuscript Draft

This folder contains a CHI-style LaTeX rewrite of the PERSONA paper.

## Files

- `persona_chi2027.tex`: main anonymous-review manuscript draft.
- `persona_chi2027.bib`: bibliography used by the draft.
- `acmart.cls` and `ACM-Reference-Format.bst`: copied from the uploaded ACM Primary Article Template.
- `figures/`: copied analysis figures used by the draft.

## Format Assumptions

- CHI 2027 initial submissions use the ACM Primary Article Template in one-column review format.
- The draft uses `\documentclass[manuscript,review,anonymous]{acmart}` for anonymous review.
- The paper intentionally frames human-likeness as insufficient rather than incorrect: `H` remains a useful descriptive signal, but the empirical test asks whether `E`, `D`, and `F` add appropriateness-relevant information.

## Evidence Base

The manuscript is grounded in the current repository theory docs and generated analysis outputs:

- `docs/theory/`
- `analysis/outputs/reports/`
- `analysis/outputs/tables/`
- `analysis/processed/persona_all.csv`
- `analysis/processed/persona_ratings_long.csv`
