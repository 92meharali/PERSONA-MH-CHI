# Paper Revision Changelog

## 2026-09-01: EIRB Approval Status

- Received and reviewed the signed university EIRB approval dated 12 February
  2026.
- Recorded the research team's confirmation that PERSONA is a sub-study within
  the broader approved project.
- Updated the active and retained manuscript drafts, ethics provenance record,
  rebuttals, and submission checklist to replace the obsolete pending status.
- Preserved the scope distinction that the letter names the parent project
  rather than PERSONA separately.
- Kept the signed document out of the anonymous public repository because it
  contains project and investigator identities and committee signatures.
- Changed no dataset, annotation, analysis, result, figure, or table.

## 2026-08-25: Major Issue 4.2, D Scope and Professional-Role Boundary

- Retained the name Anthropomorphic Deception/Misleading-Implication Risk.
- Narrowed D so standalone authority, expertise, certainty, unsafe advice, and
  factual error do not count without anthropomorphic self-presentation.
- Clarified that false professional-role language counts only when the AI
  presents itself as a human professional or enacts a professional relationship
  or continuity it does not possess.
- Mapped the clarified scope to DeVrio et al.'s expressions of understanding,
  identity, relationships, emotions, intention, and anticipation/recall.
- Added the scope clarification to the compact protocol and all three domain
  rubrics while explicitly preserving every released v3.1 score.
- Added a reproducible post-analysis D-scope audit covering all 23 health
  responses with consensus D >= 3.
- Recorded 22 affective/relational-led responses and one
  clinician-identity/continuity-led response.
- Added D-only sensitivity checks: full health R2=.241; excluding the sole
  clinician-role response .208; excluding its prompt cluster .192; excluding
  all `other` scenarios .022.
- Revised the manuscript's health interpretation to state that the D result is
  not primarily driven by standalone authority and is concentrated in a small
  relational adversarial subset.
- Removed confirmed junk synthetic-annotation text from `annotator_notes` in
  all five health files while retaining the shared column and CSV schema.
- Left score-template rationales unchanged, as approved.
- Updated theory, claims, reviewer risks, results ground truth, analysis
  documentation, rebuttal, and TODO tracking.
- Changed no response, prompt, identifier, E/D/F/OA rating, rationale, HuMT
  score, prompt group, model field, or pre-existing statistical result.

## 2026-08-25: Critical Issue 4, F and OA Construct Relationship

- Added a reproducible Phase 3 construct-relationship table containing
  Spearman correlations, prompt-cluster bootstrap intervals, and Pearson
  correlations for every H/E/D/F association with OA in every domain.
- Added transparent post-analysis F/OA disagreement diagnostics using three fixed screens:
  F >= 4 with OA <= 3, F <= 3 with OA >= 4, and |F - OA| >= 2.
- Added a trace table containing the strongest available response example for
  each observed directional disagreement pattern and domain.
- Added a manuscript table with all 12 profile-dimension/OA relationships.
- Reported F/OA Spearman/Pearson associations of .694/.809 in mental health,
  .219/.756 in education, and .060/.242 in health.
- Explained the education rank/linear divergence cautiously as consistent with
  concentrated tied ratings and separation among infrequent lower-score cases,
  without claiming that this explanation is proven.
- Reported one directional disagreement in mental health, none in education,
  and 43 in health; health also contains 33 absolute gaps of at least two points.
- Added two health response summaries showing disagreement in both directions:
  unsafe-antibiotic refusal (F=2.6, OA=5.0) and emergency-headache response
  (F=4.0, OA=2.6).
- Clarified throughout that these results support operational distinction,
  domain-dependent alignment, and low statistical redundancy, not complete
  psychometric discriminant validity.
- Replaced generic F/OA discussion with evidence-backed interpretation and
  removed confirmatory-factor-analysis language that is unsuitable for the
  current single-item dimensions.
- Updated the analysis README, results ground truth, construct definitions,
  claims boundaries, claims audit, reviewer-risk register, rebuttal, and TODO
  list to match the manuscript and generated outputs.
- Preserved all datasets, predictive specifications, reliability estimates,
  cross-validation results, ablations, domain interactions, and pre-existing
  Phase 3 tables and figures unchanged.

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
