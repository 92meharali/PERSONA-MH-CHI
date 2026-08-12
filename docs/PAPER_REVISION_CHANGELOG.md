# Paper Revision Changelog

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
