# Mental Health Analysis

## Summary

Mental health is the strongest empirical validation domain for PERSONA. It shows that automated human-likeness is not a reliable proxy for overall appropriateness, while the PERSONA dimensions add substantial explanatory signal.

## Data Quality

| Check | Result |
|---|---:|
| Responses | 660 |
| Human annotation rows | 3,300 |
| Annotators per response | 5 |
| HuMT matched responses | 660 |
| Invalid score entries | 0 |

## Reliability

Reliability was high enough for response-level consensus analysis.

| Measure | Reliability estimate |
|---|---:|
| OA | 0.852 |
| E | 0.949 |
| D | 0.960 |
| F | 0.864 |

## Score Distributions

| Measure | Mean | SD | Min | Max |
|---|---:|---:|---:|---:|
| OA | 4.317 | 0.489 | 1.8 | 5.0 |
| E | 3.736 | 0.582 | 1.8 | 5.0 |
| D | 2.093 | 0.760 | 1.0 | 4.2 |
| F | 4.361 | 0.491 | 1.8 | 5.0 |

Consensus D is mostly low to moderate, but there is enough D2-D4 variance to study anthropomorphic deception risk.

## Main Signal

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.167 |
| E with OA | 0.096 |
| D with OA | -0.159 |
| F with OA | 0.694 |

HuMT is weakly negative with OA. Domain fit is the strongest single correlate of appropriateness, and deception risk moves in the expected negative direction.

## Predictive Check

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | 0.008 |
| HuMT + E + D + F | 0.657 |
| Increment | 0.648 |

This is the clearest evidence that PERSONA captures normative information beyond human-likeness.

## Model Profiles

| Model | OA | E | D | F | HuMT |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.8 | 4.133 | 3.873 | 2.254 | 4.170 | 0.054 |
| GLM | 4.098 | 3.655 | 2.205 | 4.142 | 0.055 |
| GPT-5.6-Sol | 4.720 | 3.682 | 1.819 | 4.770 | 0.041 |

GPT-5.6-Sol has the highest OA and F and the lowest D. Claude and GLM are more human-like by HuMT but do not score higher on overall appropriateness.

## Interpretation

Mental health should remain the primary validation study. It supports the core CHI contribution: human-likeness is a poor proxy for appropriateness, and the right object of measurement is a contextual profile balancing empathy, deception risk, and fit.
