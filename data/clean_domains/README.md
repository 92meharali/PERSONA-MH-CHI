# Clean Domain Datasets

This directory is the canonical multi-domain data release for PERSONA.

PERSONA evaluates whether anthropomorphic AI behavior is appropriate in high-stakes human-support settings. The shared profile is:

```text
P = (H, E, D, F)
```

- `H`: HuMT automated human-likeness score.
- `E`: empathic appropriateness.
- `D`: anthropomorphic deception risk.
- `F`: domain fit.
- `OA`: independent overall appropriateness target.

## Domains

| Folder | Domain | Rating files | HuMT file | Rubric |
|---|---|---:|---|---|
| `mental_health/` | online mental-health support | 1 OA file + 5 E/D/F files | embedded in Group B files | `rubric.md` |
| `education/` | tutoring and learning support | 1 OA file + 5 E/D/F files | `humt_education.csv` | `rubric.md` |
| `health/` | casual health assistance | 1 OA file + 5 E/D/F files | `humt_health.csv` | `rubric.md` |

`oa_group_a.csv` contains holistic Group A `OA` ratings. The anonymous
annotator CSVs contain Group B `E`, `D`, and `F` ratings only.

## File Conventions

- Group B annotator files are anonymized as `anonymous_annotator_1.csv` through
  `anonymous_annotator_5.csv`.
- Domain rubrics are frozen with each dataset.
- HuMT files retain `source_file` so rows remain traceable to their model and condition export.
- Human scores are 1-5 integers.
- Missing metadata should be treated as unavailable, not inferred.

## Analysis Summaries

Each domain folder contains an `analysis.md` summary with data quality checks, reliability estimates, main correlations, model profile patterns, and interpretation guidance.
