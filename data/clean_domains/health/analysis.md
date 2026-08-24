# Health Analysis

This domain-level summary is a pointer to the canonical Phase 1-5 pipeline.
Paper-facing numbers should be read from `analysis/outputs/`, not typed here by
hand.

## Current Release

| Check | Result |
|---|---:|
| Responses | 415 |
| Group A OA rows | 2,075 |
| Group B E/D/F rows | 2,075 |
| HuMT matched responses | 415 |
| Prompt groups | 140 |

The health release contains 415 responses with complete HuMT coverage. The HuMT
file lacks stable response IDs, so the pipeline uses documented one-to-one text
matching and reports the join tiers. The 140 prompt clusters include 136
clusters with three model responses, three with two responses, and one with one
response.

## Canonical Outputs

| Topic | File |
|---|---|
| Data audit | `analysis/outputs/reports/data_audit.md` |
| HuMT provenance | `analysis/outputs/reports/humt_provenance_audit.md` |
| Reliability | `analysis/outputs/reports/reliability.md` |
| Separability and descriptives | `analysis/outputs/reports/descriptives.md` |
| Predictive analysis | `analysis/outputs/reports/predictive.md` |
| Domain interactions | `analysis/outputs/reports/domain_interactions.md` |

## Interpretation

Health remains ceiling-heavy. Treat it as transfer and ceiling-case evidence,
not equal-strength validation beside mental health.
