# PERSONA — research index

Entry point for the repository as a reproducible research archive. This file
routes; it does not contain findings. Every number lives in exactly one place and
is produced by a script.

**Research question:** When is anthropomorphic AI behaviour appropriate in
context?

**Framework:** `P = (H, E, D, F)`, evaluated against independently elicited
overall appropriateness `OA`. Definitions in
[`docs/theory/CONSTRUCT_DEFINITIONS.md`](docs/theory/CONSTRUCT_DEFINITIONS.md).

**Status: not validated.** Empirical evaluation is in progress. See
[`docs/theory/CLAIMS_AND_BOUNDARIES.md`](docs/theory/CLAIMS_AND_BOUNDARIES.md)
for the claim ledger.

---

## 1. Theory

[`docs/theory/`](docs/theory/README.md) — framework, construct definitions,
distinctions, literature map, research questions, hypotheses, annotation theory,
domain theory, limitations, paper argument, bibliography, citation matrix.

Start with [`PERSONA_THEORY.md`](docs/theory/PERSONA_THEORY.md).

Contains no empirical results, by design.

## 2. Constructs and annotation protocol

| What | Where |
|---|---|
| Construct definitions | [`docs/theory/CONSTRUCT_DEFINITIONS.md`](docs/theory/CONSTRUCT_DEFINITIONS.md) |
| Why two rating groups | [`docs/theory/ANNOTATION_THEORY.md`](docs/theory/ANNOTATION_THEORY.md) |
| Rubric, mental health | `data/clean_domains/mental_health/rubric.md` |
| Rubric, education | `data/clean_domains/education/rubric.md` |
| Rubric, health | `data/clean_domains/health/rubric.md` |

The mental-health rubric (v3.1) is the most fully specified and is the reference
document for the `D` severity ladder, the highest-severity-cue rule, and the
attribution rule.

## 3. Datasets

| Domain | Location | Responses | Prompts | Raters |
|---|---|---|---|---|
| Mental health | `data/clean_domains/mental_health/` | 660 | 220 | 5 |
| Education | `data/clean_domains/education/` | 450 | 150 | 5 |
| Health | `data/clean_domains/health/` | 450 | 150 | 5 |

Mental-health prompts derive from CounselBench. Dataset provenance for the other
domains is in `DOMAIN_DATASETS.md`.

Unified build: `analysis/processed/persona_all.csv` (response level) and
`analysis/processed/persona_ratings_long.csv` (rating level), both produced by
`python -m analysis.build_dataset`.

## 4. Analysis

[`analysis/README.md`](analysis/README.md) — how to reproduce every number.

```bash
pip install -r analysis/requirements.txt
python -m analysis.run_phases
```

| Phase | Module | Produces |
|---|---|---|
| 1 | `build_dataset.py` | Unified dataset, data audit, HuMT join provenance |
| 2 | `reliability.py` | Krippendorff ordinal alpha, ICC(A,1), ICC(A,k), bootstrap CIs |
| 3 | `descriptives.py` | Distributions, ceiling/floor diagnostics, separability, VIF |
| 4 | `predictive.py` | Prompt-grouped cross-validation, ablation, incremental validity |

The legacy mental-health-only pipeline (`python -m analysis`, writing to
`analysis_outputs/`) is retained for the existing manuscript.
`analysis/analysis_domains.py` is **retired** — see `analysis/README.md` for why.

## 5. Results

All results are generated artefacts. None should be transcribed by hand.

| What | Where |
|---|---|
| Data audit | `analysis/outputs/reports/data_audit.md` |
| HuMT provenance audit | `analysis/outputs/reports/humt_provenance_audit.md` |
| Reliability | `analysis/outputs/reports/reliability.md` |
| Descriptives and separability | `analysis/outputs/reports/descriptives.md` |
| Cross-validation, ablation, incremental validity | `analysis/outputs/reports/predictive.md` |
| Domain interactions | `analysis/outputs/reports/domain_interactions.md` |
| Final validation audit | `analysis/outputs/reports/final_validation_audit.md` |
| Tables (CSV) | `analysis/outputs/tables/` |
| Figures | `analysis/outputs/figures/` |
| Machine-readable results | `analysis/outputs/phase{1,2,3,4,5}_results.json` |

## 6. Limitations

[`docs/theory/CLAIMS_AND_BOUNDARIES.md`](docs/theory/CLAIMS_AND_BOUNDARIES.md).

Four that shape how everything else should be read:

- **Criterion independence is structural.** Group A produced holistic `OA`;
  Group B produced `E`, `D`, and `F`. `OA` is therefore separately elicited and
  not mathematically derived from the profile dimensions.
- **RQ4 is not answerable with this corpus.** The adversarial items target
  clinical failure modes, not anthropomorphic behaviour, and there is one
  system-prompt condition.
- **Restricted variance** in `H`, in `D`, and in `OA` in some domains bounds what
  any relationship can show.
- **Single-turn, English-only, five raters per domain**, none of them domain
  professionals.

## 7. Where things must not be duplicated

| Content | Canonical home |
|---|---|
| Theoretical claims | `docs/theory/` |
| Numbers | `analysis/outputs/` |
| Rubrics | `data/clean_domains/*/rubric.md` |
| Reproduction instructions | `analysis/README.md` |
| Routing | this file |

`RESEARCH_SUMMARY.md` predates this structure and contains hand-entered figures
that the Phase 1–4 pipeline supersedes. It should be reduced to a pointer or
removed once its content has been checked against `analysis/outputs/`.
