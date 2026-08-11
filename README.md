# PERSONA

PERSONA evaluates when human-like AI behavior is appropriate in high-stakes human-support settings.

The project argues that human-likeness is not a sufficient measure of appropriateness. A response can sound warm or human while being misleading, overconfident, or poorly matched to the user's situation. PERSONA therefore separates human-likeness from contextual, relational, and boundary-related properties.

For the full research archive, start with [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md).

## Framework

```text
P = (H, E, D, F)
```

| Dimension | Meaning |
|---|---|
| `H` / HuMT | automated human-likeness |
| `E` | empathic appropriateness |
| `D` | anthropomorphic deception risk |
| `F` | contextual fit |
| `OA` | independent overall appropriateness target |

`OA` is elicited as a holistic target judgment. It is not computed from `E`,
`D`, or `F`.

The optional secondary score is:

```text
S = (H + E - D + F) / 4
```

`S` is useful only as a transparent secondary projection. The multidimensional
profile `P` remains the contribution.

## Research Documentation

| Area | Canonical location |
|---|---|
| Research index | [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md) |
| Theory and construct definitions | [`docs/theory/`](docs/theory/README.md) |
| Literature map and citation status | [`docs/theory/LITERATURE_MAP.md`](docs/theory/LITERATURE_MAP.md), [`docs/theory/CITATION_MATRIX.md`](docs/theory/CITATION_MATRIX.md) |
| Research questions and hypotheses | [`docs/theory/RESEARCH_QUESTIONS.md`](docs/theory/RESEARCH_QUESTIONS.md), [`docs/theory/HYPOTHESES.md`](docs/theory/HYPOTHESES.md) |
| Claim boundaries and limitations | [`docs/theory/CLAIMS_AND_BOUNDARIES.md`](docs/theory/CLAIMS_AND_BOUNDARIES.md) |
| Analysis reproduction | [`analysis/README.md`](analysis/README.md) |

## Canonical Data

The final cleaned multi-domain release is in:

```text
data/clean_domains/
```

| Domain | Folder | Responses | Rating rows | HuMT |
|---|---|---:|---:|---|
| Mental health | `data/clean_domains/mental_health/` | 660 | 3,300 | embedded |
| Education | `data/clean_domains/education/` | 415 | 2,075 | `humt_education.csv` |
| Health | `data/clean_domains/health/` | 415 | 2,075 oversight/adjudication rows | `humt_health.csv` |

Each domain folder contains:

- `oa_group_a.csv` with Group A holistic `OA` ratings
- five anonymous Group B annotator CSVs with `E`, `D`, and `F` ratings
- `rubric.md`
- `README.md`
- `analysis.md`

## Analysis

The current multi-domain analysis pipeline is in `analysis/` and writes
generated outputs to `analysis/outputs/`.

```bash
pip install -r analysis/requirements.txt
python -m analysis.run_phases
```

The legacy mental-health-only pipeline is retained for continuity, but the
Phase 1-5 pipeline is the canonical multi-domain analysis.

Generated reports:

| Report | Location |
|---|---|
| Data audit | `analysis/outputs/reports/data_audit.md` |
| HuMT provenance audit | `analysis/outputs/reports/humt_provenance_audit.md` |
| Reliability | `analysis/outputs/reports/reliability.md` |
| Descriptives and separability | `analysis/outputs/reports/descriptives.md` |
| Predictive analysis | `analysis/outputs/reports/predictive.md` |
| Domain interaction audit | `analysis/outputs/reports/domain_interactions.md` |

## Paper Direction

The strongest CHI framing is:

> Human-likeness alone is insufficient for judging appropriateness. AI behavior in human-support settings should be evaluated as a contextual profile balancing empathy, deception risk, and fit.

Mental health is the strongest empirical domain in the current archive. Education
and health are domain-transfer evidence and should be interpreted with the
limitations documented in [`docs/theory/CLAIMS_AND_BOUNDARIES.md`](docs/theory/CLAIMS_AND_BOUNDARIES.md).
