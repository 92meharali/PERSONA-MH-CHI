# PERSONA analysis pipeline

Two pipelines live in this folder.

| Pipeline | Entry point | Scope | Status |
|---|---|---|---|
| Phase pipeline (current) | `python -m analysis.run_phases` | All three domains, Phases 1-5 | Active |
| Mental-health pipeline (legacy) | `python -m analysis` | Mental health only, writes `analysis_outputs/` | Kept for the existing manuscript, superseded for anything multi-domain |
| Quick domain runner | `analysis/analysis_domains.py` | Education and health `analysis.md` | **Retired.** See "Why the quick runner was retired" |

## Reproducing every number

```bash
pip install -r analysis/requirements.txt
python -m analysis.run_phases
```

Runtime is about 50 seconds. Reruns are byte-identical: every random operation
draws from an explicitly seeded generator (`SEED = 42` in `persona_common.py`)
and the cross-validation splitter is implemented locally rather than taken from
scikit-learn, whose grouping heuristic changes between releases.

Individual phases can be run alone, in order:

```bash
python -m analysis.build_dataset   # Phase 1
python -m analysis.humt_provenance_audit # Phase 1b
python -m analysis.reliability     # Phase 2
python -m analysis.descriptives    # Phase 3
python -m analysis.predictive      # Phase 4
python -m analysis.domain_interactions # Phase 5
```

Phases 1b-5 read `analysis/processed/persona_all.csv`, so Phase 1 must run first.

## What each phase does

**Phase 1 - `build_dataset.py`.** Reads the Group A `oa_group_a.csv` file and
the five anonymous Group B E/D/F annotator CSVs per domain and
emits one rating-level file and one response-level file, plus a full data audit.
It repairs two structural gaps in the education and health exports, both
deterministically and both reported:

- `prompt_id` is absent, so it is reconstructed from normalised prompt text
  (each prompt has exactly three responses, one per model). Without it, grouped
  cross-validation degrades to ungrouped cross-validation and sibling responses
  leak across folds.
- `model` is absent, so it is recovered from the `source_file` column of the
  domain HuMT export through a cascading text join, then completed by
  elimination within prompt groups that are already partially identified.

The HuMT join runs full-text first, then shrinking prefixes, then a
mutually-best near-duplicate tier requiring similarity of at least 0.95 and a
margin of 0.05 over the runner-up. A candidate is accepted only when it
identifies exactly one response and exactly one HuMT row. Nothing is dropped:
unmatched rows are carried with explicit missing values and counted.

**Phase 1b - `humt_provenance_audit.py`.** Produces a read-only HuMT provenance
audit checking response-text uniqueness, HuMT-text duplication, stable-ID
availability, unmatched rows, and false-match risk. It does not recover missing
HuMT values.

**Phase 2 - `reliability.py`.** Primary reliability is two-way mixed-effects,
absolute-agreement, average-measures ICC(A,k), with percentile bootstrap
intervals over responses, reported per domain and per criterion/dimension and
additionally by scenario type. ICC(A,1) and Krippendorff's ordinal alpha are
reported as supplementary diagnostics. The ICC routine is computed from ANOVA
mean squares and matches `pingouin.intraclass_corr` to within 1e-8.

**Phase 3 - `descriptives.py`.** Distributions by domain and by model, explicit
ceiling and floor diagnostics, pairwise Spearman and Pearson associations with
prompt-cluster bootstrap intervals and Benjamini-Hochberg correction, and
variance inflation factors for the four profile dimensions.

**Phase 4 - `predictive.py`.** Twelve specifications per grouping, all fitted on
identical complete-case rows. Cross-validation is 5-fold grouped on `prompt_id`
and repeated 20 times with independently seeded fold assignments; the reported
figure is the mean with a standard deviation across repeats. Confidence
intervals come from 1000 prompt-cluster bootstrap resamples of the out-of-fold
predictions, and every comparison between specifications reuses the same
resamples so the differences are paired.

**Phase 5 - `domain_interactions.py`.** A targeted OLS audit tests whether the
association between each profile dimension and `OA` differs by domain:
`OA ~ z(H,E,D,F) * domain`. Uncertainty uses cluster-robust standard errors by
`domain::prompt_id`. This phase is interpretive, not causal.

## Outputs

```
analysis/processed/persona_ratings_long.csv   one row per (domain, response, rater)
analysis/processed/persona_all.csv            one row per response, consensus scores
analysis/outputs/tables/*.csv                 all paper-facing tables
analysis/outputs/figures/*.png                all figures
analysis/outputs/reports/*.md                 readable versions of each phase
analysis/outputs/phase{1,2,3,4,5}_results.json machine-readable results
analysis/outputs/run_manifest.json            environment and timings
```

The targeted final audit is recorded in
`analysis/outputs/reports/final_validation_audit.md`.

`cv_fold_assignments.csv` records the fold each response fell into on the first
repeat, and `cv_folds.csv` records every fold of every repeat, so any reported
aggregate can be traced back to the splits that produced it.

No paper-facing number should be typed by hand. If a figure appears in a
manuscript, it should be traceable to a file in `analysis/outputs/`.

## Why the quick runner was retired

`analysis/analysis_domains.py` produced the education and health `analysis.md`
files. Three problems make its output unusable for the paper:

1. It grouped cross-validation on `row.get("prompt_id", row.get("annotation_item_id", ""))`.
   Neither column exists in the education or health files, so groups fell back
   to the unique response id and the split was effectively ungrouped.
2. It read `row.get("model", "")` for the same files, which always returned an
   empty string, so it could not produce model profiles at all.
3. It used Cronbach's alpha while the mental-health pipeline used Krippendorff's
   alpha and ICC. Cronbach's alpha is an internal-consistency coefficient rather
   than an agreement coefficient, so the two were tabulated side by side in the
   summary documents without being comparable.

Phase 2 recomputes reliability with a single method for all three domains, and
the values differ substantially from the previously published ones. Any table
sourced from the old runner should be regenerated before submission.

## Known gaps

- The active education and health releases are filtered to 415 HuMT-complete
  responses each. Their committed HuMT exports still contain 450 provenance rows
  and still lack stable response IDs, so future exports should include
  `annotation_item_id`.
- Because 415 is not divisible by three, the filtered education and health
  releases contain a small number of prompt groups with fewer than three
  responses. Grouped cross-validation still groups by `prompt_id`.
- The corpus contains a single system-prompt condition, so the paired
  contrast of the same context under different anthropomorphic behaviour
  cannot be run. This is recorded as **NOT AVAILABLE - requires additional
  data** rather than approximated.
- Within each domain, the rate at which all five raters recorded the same
  rationale text is exactly equal to the rate at which they recorded the same
  score. Rationales are therefore a deterministic function of scores and are not
  independent evidence of independent annotation.
