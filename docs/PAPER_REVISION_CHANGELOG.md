# Paper Revision Changelog

## 2026-08-25: Critical Issue 3, Reproducibility and Count Reconciliation

- Named the predictive estimator as ordinary least squares linear regression
  with an intercept.
- Documented that predictors enter on their recorded scales and that pooled
  models include domain indicators.
- Documented the absence of regularization, imputation, feature selection,
  hyperparameter tuning, and outcome transformation.
- Documented grouped five-fold cross-validation repeated 20 times, deterministic
  seeds 42--61, prompt-level grouping, 1,000 prompt-cluster bootstrap resamples,
  paired comparisons, and the primary scoring procedure.
- Established 415 as both the original released and final analysis response count
  for education and health; removed filtering and attrition language.
- Reduced each clean HuMT file to the 415 one-to-one records belonging to the
  released corpus, without changing any HuMT value used in analysis.
- Reconciled prompt structure: education has 139 clusters with sizes 138x3 and
  1x1; health has 140 clusters with sizes 136x3, 3x2, and 1x1.
- Clarified that grouped cross-validation keeps each prompt intact despite
  variable model coverage.
- Corrected provenance: education natural prompts were sourced and adapted from
  Bridge and MathDial, health natural prompts from HealthBench, and adversarial
  prompts were authored for this study.
- Added primary citations for Bridge, MathDial, and HealthBench.
- Updated domain READMEs, domain analyses, analysis documentation, claims
  boundaries, generated audits, and the older manuscript copy to remove stale
  filtering language.
- Preserved the released 1,490-response corpus and every analysis result.

## 2026-08-25: Critical Issue 2, H-Only Baseline Framing

- Replaced the old RQ wording with questions about human-likeness sufficiency,
  omitted appropriateness-relevant information, and domain-specific calibration.
- Reframed "predictive validity" as a grouped out-of-sample comparison that
  quantifies information omitted by an H-only evaluation.
- Replaced claims that the full profile "improves prediction" or "validates"
  PERSONA with claims about added explanatory performance and OA-associated
  information.
- Reordered Results so RQ1, RQ2, and RQ3 appear before reliability,
  distributional diagnostics, and model-level descriptives.
- Added a Results Overview subsection and explicit RQ labels.
- Preserved all model specifications, folds, estimates, confidence intervals,
  figures, tables, and generated analysis outputs unchanged.
- Added the agreed cautious health interpretation: D is the strongest
  single-dimension predictor within a restricted OA range, and the pattern is
  exploratory rather than a definitive reversal.
- Added a general future-work commitment to compare PERSONA with alternative
  response-level evaluation baselines and evaluator populations.
- Added an explicit non-claim to the claims audit: superiority over every
  alternative response-level baseline was not tested and is not claimed.
- Added the asymmetric-baseline concern to the reviewer risk register.
- Updated theory RQs and the paper argument to match the manuscript.
- Removed a stale commented-out abstract to prevent conflicting claims from
  persisting in the source.
- Fixed the missing space after "499 prompt clusters)."
- Created `docs/REBUTTAL.md` as the cumulative record of professor concerns,
  decisions, manuscript edits, supporting-document edits, and status.

## Internal Audit Before Editing

### A. Already strong

- The paper has a clear central argument: human-likeness is useful but not enough.
- The Group A / Group B split is already present and is the strongest methodological feature.
- The discussion already avoids a blanket anti-anthropomorphism stance.
- The manuscript already includes current dataset sizes and the broad mental-health/education/health hierarchy.

### B. Outdated

- Reliability values were stale relative to current `analysis/outputs/tables/reliability.csv`.
- Health H/OA Spearman and some ceiling/interaction values needed synchronization to current generated CSVs.
- RQ3 used "transfer" wording that could imply generalization to unseen domains.

### C. Scientifically vulnerable

- F/OA overlap needed explicit treatment near the ablation result.
- D needed clearer wording as misleading implication risk rather than intentional deception.
- Low VIF needed to be framed as statistical non-redundancy, not construct validation.
- Health needed stronger restricted-variance framing.

### D. Numerically inconsistent

- Prompt-supplied values differed from generated CSV outputs for several values. The manuscript now follows generated outputs as authoritative.

### E. Needed stronger CHI/HCI framing

- Added actual response-level examples.
- Added design implications focused on auditing, calibration, red-teaming, and post-hoc diagnosis.
- Added measurement architecture figure clarifying the independent OA pathway.

### F. Should not be changed

- The calibration framing should remain: human-likeness is not bad, it is insufficient alone.
- The profile `P=(H,E,D,F)` should remain central.
- `S` should remain absent from the main manuscript.
- The paper should not claim universal validation.

## Implemented Changes

- Rewrote the abstract with current predictive results.
- Added `Figure 1`, a measurement-architecture diagram showing HuMT, Group A, Group B, profile construction, and independent OA prediction.
- Added a response-level examples table using actual processed dataset excerpts and scores.
- Updated reliability text and table to current generated ICC(A,k) values.
- Updated H/OA Spearman values to current generated correlation CSV.
- Reframed RQ3 as domain variation rather than transfer.
- Reframed D as anthropomorphic deception/misleading implication risk.
- Reframed F results to avoid claiming F is identical to appropriateness.
- Added VIF/non-redundancy paragraph.
- Expanded design implications.
- Strengthened scope and boundaries without over-apologizing.
- Created `docs/CLAIMS_AUDIT.md`, `docs/RESULTS_GROUND_TRUTH.md`, `docs/REVIEWER_RISK.md`, and `docs/PAPER_TODOS.md`.

## Review Resolution Notes

- The post-revision spec review flagged differences between the prompt's pasted
  numeric list and the manuscript. The manuscript intentionally follows
  `analysis/outputs/tables/*.csv` because the prompt states that regenerated
  analysis outputs are authoritative.
- The standards review flagged remaining validation wording and exact-excerpt
  traceability. The manuscript now uses "primary empirical domain" and notes that
  response excerpts are shortened and lightly normalized for LaTeX notation.
