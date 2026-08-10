# PERSONA

PERSONA evaluates when human-like AI behavior is appropriate in high-stakes human-support settings.

The project argues that human-likeness is not a sufficient measure of appropriateness. A response can sound warm or human while being unsafe, misleading, or poorly matched to the user's situation. PERSONA therefore separates human-likeness from normative dimensions of interaction quality.

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

`OA` is rated independently. It is not computed from `E`, `D`, or `F`.

The optional secondary score is:

```text
S = (H + E - D + F) / 4
```

`S` is useful for transparent ranking, but the paper treats `OA` as the target judgment.

## Canonical Data

The final cleaned multi-domain release is in:

```text
data/clean_domains/
```

| Domain | Folder | Responses | Rating rows | HuMT |
|---|---|---:|---:|---|
| Mental health | `data/clean_domains/mental_health/` | 660 | 3,300 | embedded |
| Education | `data/clean_domains/education/` | 450 | 2,250 | `humt_education.csv` |
| Health | `data/clean_domains/health/` | 450 | 2,250 oversight/adjudication rows | `humt_health.csv` |

Each domain folder contains:

- five annotator CSVs
- `rubric.md`
- `README.md`
- `analysis.md`

## Key Result

Across domains, HuMT is weakly or negatively related to overall appropriateness:

| Domain | HuMT-OA Spearman rho | PERSONA gain over HuMT-only CV R2 |
|---|---:|---:|
| Mental health | -0.167 | +0.648 |
| Education | -0.072 | +0.472 |
| Health | -0.046 | +0.245 |

Mental health is the strongest validation domain. Education and health support cross-domain transfer, with domain-specific interpretation.

## Analysis

The current detailed mental-health analysis pipeline remains in `analysis/` and writes outputs to `analysis_outputs/`.

```bash
pip install -r analysis/requirements.txt
python -m analysis
```

The per-domain summaries in `data/clean_domains/*/analysis.md` provide compact multi-domain checks for data quality, reliability, score distributions, HuMT/OA relationships, and model profiles.

## Paper Direction

The strongest CHI framing is:

> Human-likeness is the wrong proxy for appropriateness. AI behavior in human-support settings should be evaluated as a contextual profile balancing empathy, deception risk, and fit.

Mental health provides the primary empirical validation. Education and health show that the profile transfers, but the meaning of "appropriate" changes by domain.
