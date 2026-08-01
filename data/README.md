# Final human annotations

## v1 (original system prompt)

- `responses.csv`: 660 blinded items joined to model, prompt, dataset, and HuMT provenance.
- `ratings_long.csv`: five independent ratings per item (3,300 rows).
- `annotation_protocol.md`: frozen PERSONA-MH protocol used for the final ratings.

## v2 (relaxed system prompt)

See `README_v2.md`. Canonical files: `responses_v2.csv`, `ratings_long_v2.csv`.

Overall Appropriateness (OA) was completed and locked before E/D/F. OA uses protocol v2; E and F retain the v2 definitions; Deception Risk uses the final v3.1 highest-severity, AI-attributable-cue rule. Shared evidence spans are intentionally excluded. Raw individual scores and reasons are preserved.

E uses a second, independent blind annotation round after annotators were asked to reapply the unchanged empathy rubric carefully. Annotators did not see OA, prior E scores, or analysis results.

Analyses aggregate five raters at response level while retaining `ratings_long.csv` for reliability and rater-aware checks.
