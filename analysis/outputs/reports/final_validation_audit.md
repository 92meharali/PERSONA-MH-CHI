# Final validation, documentation, and analysis audit

Generated during the targeted audit pass after the Phase 1-5 analysis and theory
documentation branches were stacked.

## A. Fixed

| Area | Correction |
|---|---|
| Annotator-group documentation | Corrected theory and index files to state that Group A rated holistic `OA`, while Group B rated `E`, `D`, and `F`. Removed stale claims that collapsed the criterion and predictor pools. |
| Clean data layout | Split `OA` into `oa_group_a.csv` in each domain and removed `OA_score`, `OA_reason`, and `OA_review_flag` from the Group B annotator CSVs. Group B files are anonymized as `anonymous_annotator_1.csv` through `anonymous_annotator_5.csv`. |
| Phase 1 builder | Updated `analysis/build_dataset.py` to read Group A and Group B pools separately, preserve `rater_group`, and report separate OA and E/D/F row counts. |
| Reliability framing | Made ICC(A,k) the primary reliability statistic. ICC(A,1) and Krippendorff's ordinal alpha remain supplementary diagnostics. |
| Repository routing docs | Updated `README.md`, `RESEARCH_INDEX.md`, `RESEARCH_SUMMARY.md`, and `analysis/README.md` for the Phase 1-5 pipeline and canonical generated outputs. |
| Claims ledger | Updated `docs/theory/CLAIMS_AND_BOUNDARIES.md` with claim categories and evidence boundaries. |
| Corrected-location audit | Corrected stale Group A / Group B descriptions in `docs/theory/ANNOTATION_THEORY.md`, `docs/theory/CLAIMS_AND_BOUNDARIES.md`, `docs/theory/CONSTRUCT_DEFINITIONS.md`, `docs/theory/PERSONA_THEORY.md`, `docs/theory/PAPER_ARGUMENT.md`, `docs/theory/README.md`, `RESEARCH_INDEX.md`, `README.md`, `RESEARCH_SUMMARY.md`, `analysis/README.md`, and the domain data READMEs. `docs/theory/RESEARCH_QUESTIONS.md` and `docs/theory/HYPOTHESES.md` were audited and required no wording change. |

## B. Already Correct

| Area | Audit result |
|---|---|
| HuMT joins | The existing join is deterministic and ambiguity-aware: exact normalized text, shrinking prefixes, then mutually-best fuzzy matching. Unmatched rows remain unmatched and are reported in `humt_provenance_audit.md`. |
| HuMT provenance reporting | Phase 1 reports mental health 660/660 matched, education 415/415 matched, and health 415/415 matched, with zero ambiguous keys accepted in the released corpus. |
| Construct separability | Phase 3 already reported pairwise correlations, FDR-adjusted p-values, cluster-bootstrap intervals, and VIF. |
| ICC implementation | `reliability.py` computes absolute-agreement ICC(A,1) and ICC(A,k) from ANOVA mean squares; ICC(A,k) is now primary and alpha supplementary. |
| Ablation coverage | Phase 4 already covers `H`, `H+E`, `H+D`, `H+F`, `H+E+D`, `H+E+F`, `H+D+F`, `E+D+F`, and `H+E+D+F`, plus single-dimension specifications. Phase 4 outputs were regenerated only because the canonical rating-long input changed from combined rows to separate Group A and Group B rows; the predictive implementation was not redesigned. |
| Grouped CV | Phase 4 uses prompt-grouped 5-fold CV, repeated 20 times, with paired prompt-cluster bootstrap intervals for comparisons. |
| Health uncertainty | The health full-profile improvement over `H_only` remains positive as a point estimate, but its interval crosses zero. This limitation is preserved. |

## C. New Analyses

| Analysis | Output |
|---|---|
| Condition-number diagnostic for profile collinearity | `analysis/outputs/tables/collinearity_condition.csv`; summarized in `analysis/outputs/reports/descriptives.md` |
| HuMT provenance audit | `analysis/outputs/tables/humt_provenance_audit.csv`, `analysis/outputs/reports/humt_provenance_audit.md`, and `analysis/outputs/humt_provenance_audit.json` |
| Domain interaction audit | `analysis/outputs/tables/domain_interactions.csv`, `analysis/outputs/tables/domain_interaction_model_fit.csv`, `analysis/outputs/reports/domain_interactions.md`, and `analysis/outputs/phase5_results.json` |

## D. Current Interpretation Boundaries

- `OA` is structurally separate from the Group B dimensions, but it remains a
  small-pool human judgment rather than objective ground truth.
- ICC(A,k) is the primary agreement statistic because the analysis uses averaged
  multi-rater scores.
- `F` is a major contributor in mental health and education, but this is an
  association and should not be phrased causally.
- Health is weaker evidence because of ceiling effects and uncertainty that
  crosses zero for the main increment.
- RQ4 remains not answerable without an anthropomorphic elicitation condition or
  paired responses holding content constant.
