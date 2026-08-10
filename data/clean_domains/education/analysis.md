# Education Analysis

## Summary

Education extends PERSONA into tutoring and teaching-assistant support. It supports the same central claim as mental health: human-likeness is not enough to explain appropriateness, and contextual fit matters a great deal.

## Data Quality

| Check | Result |
|---|---:|
| Responses | 450 |
| Rating rows | 2,250 |
| HuMT matched responses | 385 |

HuMT joins are by normalized response text in this quick runner; a stable response ID join would be preferable in a final pass.

## Reliability

| Measure | Reliability estimate |
|---|---:|
| OA | 0.947 |
| E | 0.997 |
| D | 0.965 |
| F | 0.960 |

Agreement is very high. The paper should describe this as strong consensus and avoid overclaiming independence without an annotation-process audit.

## Correlations

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.072 |
| E with OA | -0.030 |
| D with OA | -0.028 |
| F with OA | 0.229 |

HuMT remains weak. Contextual fit is the most interpretable appropriateness dimension because tutoring quality depends on scaffolding, academic boundaries, and fit to the learner's need.

## Predictive Check

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | 0.139 |
| HuMT + E + D + F | 0.577 |

## Interpretation

Education is a useful transfer domain. It shows that a response can be appropriate with relatively modest empathy if it is pedagogically clear, bounded, and fit to the learner's situation.
