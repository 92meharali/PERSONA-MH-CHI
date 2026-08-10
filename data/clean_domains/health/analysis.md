# Health Analysis

## Summary

Health extends PERSONA into casual health-assistance contexts. This domain is treated as oversight/adjudication evidence rather than independently verified human annotation, so the interpretation should stay explicit about provenance.

## Data Quality

| Check | Result |
|---|---:|
| Responses | 450 |
| Rating rows | 2,250 |
| HuMT matched responses | 416 |

HuMT joins are by normalized response text in this quick runner; a stable response ID join would be preferable in a final pass.

## Reliability

| Measure | Reliability estimate |
|---|---:|
| OA | 0.900 |
| E | 0.937 |
| D | 0.935 |
| F | 0.918 |

Agreement is strong across all measures. Because these files are oversight/adjudication passes, this should be interpreted as consistency of the adjudicated rating set rather than independent human inter-rater reliability.

## Correlations

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.046 |
| E with OA | -0.060 |
| D with OA | -0.069 |
| F with OA | 0.043 |

HuMT is essentially unrelated to OA. The low variance in OA makes this domain better for transfer evidence than for stress-testing failure modes.

## Predictive Check

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | -0.014 |
| HuMT + E + D + F | 0.199 |

## Interpretation

Health supports the rejection of HuMT as an appropriateness proxy, but it should be treated as a ceiling-heavy transfer domain unless we later re-export a cleaner adversarial health set.
