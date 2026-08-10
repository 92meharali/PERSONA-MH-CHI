# PERSONA Data

The canonical multi-domain data release is:

```text
data/clean_domains/
```

This folder contains the final cleaned datasets for:

- mental health
- education
- health

Each domain folder includes five annotator CSVs, a frozen rubric, a README, and an analysis summary.

The remaining top-level files in `data/` support the original mental-health analysis pipeline:

| File | Role |
|---|---|
| `responses.csv` | Mental-health response metadata and HuMT |
| `ratings_long.csv` | Mental-health long-format ratings |
| `annotation_protocol.md` | Mental-health protocol |
| `annotation_sheet.csv` | Original mental-health annotation template |
| `annotation_key.csv` | Mental-health model/HuMT join key |
| `responses_build_report.csv` | Mental-health response build diagnostics |
| `raw_annotations/` | Mental-health per-annotator source sheets |
| `CORPUS.md` | Mental-health corpus notes |

For the paper-facing multi-domain release, start with `clean_domains/README.md`.
