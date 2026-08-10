# Health Analysis

## Summary

Health extends PERSONA into casual medical and health-assistance scenarios. The domain supports the rejection of HuMT as an appropriateness proxy, but the current response set is highly appropriate overall, which makes it less discriminative than mental health or education.

## Data Quality

| Check | Result |
|---|---:|
| Responses | 450 |
| Oversight/adjudication rows | 2,250 |
| Rating passes per response | 5 |
| HuMT matched responses in quick text join | 416 |
| Invalid score entries | 0 |

The HuMT file has 450 rows, but exact response-text matching in the quick check matched 416 because some responses differ by truncation or character normalization. The dataset itself should be joined with a stable response key in downstream analysis.

## Reliability

| Measure | Reliability estimate |
|---|---:|
| OA | 0.900 |
| E | 0.937 |
| D | 0.935 |
| F | 0.918 |

Agreement is strong across all measures. Because these files are oversight/adjudication passes, this should be interpreted as consistency of the adjudicated rating set rather than independent human inter-rater reliability.

## Score Distributions

| Measure | Mean | SD | Min | Max |
|---|---:|---:|---:|---:|
| OA | 4.854 | 0.390 | 1.8 | 5.0 |
| E | 2.496 | 0.878 | 1.2 | 5.0 |
| D | 1.281 | 0.612 | 1.0 | 5.0 |
| F | 4.190 | 0.682 | 1.8 | 5.0 |

OA is very high overall. This suggests the evaluated health responses are mostly safe and appropriate, so the current health set is better for domain-transfer evidence than for stress-testing failure modes.

## Main Signal

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.046 |
| E with OA | -0.060 |
| D with OA | -0.069 |
| F with OA | 0.043 |

HuMT is essentially unrelated to OA. E/D/F correlations are also weak because OA is compressed near the top of the scale.

## Predictive Check

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | -0.003 |
| HuMT + E + D + F | 0.242 |
| Increment | 0.245 |

PERSONA still improves over HuMT, but the increment is smaller than in mental health and education because the target has limited variation.

## Model Profiles

| Model/Condition | OA | E | D | F | HuMT |
|---|---:|---:|---:|---:|---:|
| adv_claude_opus_4_8 | 4.836 | 3.200 | 1.444 | 4.320 | 0.047 |
| adv_glm_5_2 | 4.552 | 3.156 | 1.732 | 4.148 | 0.045 |
| adv_gpt_5_6 | 4.840 | 2.840 | 1.380 | 4.244 | 0.035 |
| claude_opus_4_8 | 4.907 | 2.364 | 1.187 | 4.193 | 0.031 |
| glm_5_2 | 4.918 | 2.153 | 1.129 | 4.144 | 0.020 |
| gpt_5_6_sol | 4.916 | 2.091 | 1.153 | 4.112 | 0.021 |

All natural health model outputs score very high on OA. Adversarial GLM is the clearest lower-performing condition, mainly through higher D and lower F.

## Interpretation

Health is a useful domain-transfer check, but it should not be the main statistical proof. Its current value is showing that even in a domain where most responses are judged appropriate, HuMT still fails as a proxy and PERSONA exposes distinct domain profiles.
