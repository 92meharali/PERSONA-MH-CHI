# Education Analysis

## Summary

Education extends PERSONA from mental-health support into tutoring and learning assistance. The domain supports the same central claim: human-likeness is not enough to explain appropriateness. The education signal is strongest around contextual fit and academic-boundary handling.

## Data Quality

| Check | Result |
|---|---:|
| Responses | 450 |
| Human annotation rows | 2,250 |
| Annotators per response | 5 |
| HuMT matched responses in quick text join | 385 |
| Invalid score entries | 0 |

The HuMT file has 450 rows, but exact response-text matching in the quick check matched 385 because some responses differ by truncation or character normalization. The dataset itself should be joined with a stable response key in downstream analysis.

## Reliability

| Measure | Reliability estimate |
|---|---:|
| OA | 0.947 |
| E | 0.997 |
| D | 0.965 |
| F | 0.960 |

Agreement is very high. This is useful for consensus scoring, but the strongest paper claim should describe it as high consensus rather than overstate rater independence without an audit.

## Score Distributions

| Measure | Mean | SD | Min | Max |
|---|---:|---:|---:|---:|
| OA | 4.313 | 0.591 | 1.0 | 5.0 |
| E | 2.369 | 0.622 | 1.0 | 5.0 |
| D | 1.174 | 0.565 | 1.0 | 5.0 |
| F | 4.034 | 0.496 | 1.0 | 5.0 |

Education produces lower empathy scores than mental health, which is expected because good tutoring often needs clarity, scaffolding, and boundaries more than intense emotional validation.

## Main Signal

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.072 |
| E with OA | -0.030 |
| D with OA | -0.028 |
| F with OA | 0.229 |

HuMT remains weak. F is the clearest single dimension associated with OA, which fits the tutoring domain: responses are judged most by whether they scaffold learning and respect academic boundaries.

## Predictive Check

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | 0.119 |
| HuMT + E + D + F | 0.592 |
| Increment | 0.472 |

PERSONA dimensions add substantial signal beyond human-likeness.

## Model Profiles

| Model/Condition | OA | E | D | F | HuMT |
|---|---:|---:|---:|---:|---:|
| adv_claude_opus_4_8 | 4.535 | 2.486 | 1.363 | 4.110 | 0.038 |
| adv_glm_5_2 | 4.176 | 2.416 | 1.608 | 3.780 | 0.041 |
| adv_gpt_5_6_sol | 4.150 | 2.223 | 1.242 | 3.796 | 0.045 |
| claude_opus_4_8 | 4.416 | 2.772 | 1.140 | 4.124 | 0.028 |
| glm_5_2 | 4.251 | 2.246 | 1.029 | 4.126 | 0.029 |
| gpt_5_6_sol | 4.268 | 2.044 | 1.000 | 4.064 | 0.020 |

Claude has the highest OA in both natural and adversarial education subsets. GLM and GPT are similar on OA, with GPT showing low D but not the highest fit.

## Interpretation

Education is a useful transfer domain. The contribution is not that tutoring requires the same empathy profile as mental health. The better claim is that each domain has its own appropriate profile: education rewards contextual fit, scaffolding, and boundary control, while high human-likeness is neither necessary nor sufficient.
