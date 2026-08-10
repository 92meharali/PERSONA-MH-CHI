# Clean Domain Datasets

This directory is the canonical multi-domain data release for PERSONA.

PERSONA evaluates whether anthropomorphic AI behavior is appropriate in high-stakes human-support settings. The shared profile is:

```text
P = (H, E, D, F)
```

- `H`: HuMT automated human-likeness score.
- `E`: empathic appropriateness.
- `D`: anthropomorphic deception risk.
- `F`: contextual fit.
- `OA`: independent overall appropriateness target.

## Domains

| Folder | Domain | Rating files | HuMT file | Rubric |
|---|---|---:|---|---|
| `mental_health/` | online mental-health support | 5 | embedded in annotator files | `rubric.md` |
| `education/` | tutoring and learning support | 5 | `humt_education.csv` | `rubric.md` |
| `health/` | casual health assistance | 5 oversight/adjudication files | `humt_health.csv` | `rubric.md` |

Each annotator CSV contains one row per model response. Education and health combine Phase 1 `OA` ratings with Phase 2 `E/D/F` ratings by `annotation_item_id` and `presentation_order`.

## File Conventions

- Annotator files are named by annotator id.
- Domain rubrics are frozen with each dataset.
- HuMT files retain `source_file` so rows remain traceable to their model and condition export.
- Human scores are 1-5 integers.
- Missing metadata should be treated as unavailable, not inferred.

## Analysis Summaries

Each domain folder contains an `analysis.md` summary with data quality checks, reliability estimates, main correlations, model profile patterns, and interpretation guidance.
