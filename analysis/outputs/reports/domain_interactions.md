# Domain interaction audit (Phase 5)

This model tests whether the association between each PERSONA dimension and `OA` varies by domain. Predictors `H`, `E`, `D`, and `F` are z-scored over complete cases. Mental health is the reference domain. Uncertainty uses cluster-robust standard errors with clusters defined as `domain::prompt_id`.

The model is interpretive, not causal. A domain interaction estimates how much the slope for a dimension differs from the mental-health slope in that domain.

## Model fit

| N | Prompt clusters | R² | Adj. R² | Condition number |
|---:|---:|---:|---:|---:|
| 1526 | 510 | 0.647 | 0.644 | 9.81 |

## Interaction terms

| Term | Estimate | 95% CI | p | Interpretation |
|---|---:|---|---:|---|
| z_H:x:domain_education | -0.015 | [-0.059, 0.029] | 0.4927 | no clear slope difference |
| z_H:x:domain_health | 0.043 | [-0.002, 0.088] | 0.0638 | no clear slope difference |
| z_E:x:domain_education | -0.100 | [-0.181, -0.019] | 0.0157 | differs from mental-health slope |
| z_E:x:domain_health | -0.105 | [-0.177, -0.034] | 0.0040 | differs from mental-health slope |
| z_D:x:domain_education | -0.004 | [-0.085, 0.077] | 0.9285 | no clear slope difference |
| z_D:x:domain_health | -0.213 | [-0.334, -0.093] | 0.0005 | differs from mental-health slope |
| z_F:x:domain_education | 0.043 | [-0.039, 0.126] | 0.3030 | no clear slope difference |
| z_F:x:domain_health | -0.375 | [-0.433, -0.317] | 0.0000 | differs from mental-health slope |

## All coefficients

| Term | Type | Estimate | SE | 95% CI | p |
|---|---|---:|---:|---|---:|
| const | main_or_control | 4.175 | 0.024 | [4.128, 4.223] | 0.0000 |
| z_H | main_or_control | -0.027 | 0.014 | [-0.055, 0.000] | 0.0518 |
| z_E | main_or_control | 0.089 | 0.027 | [0.037, 0.141] | 0.0008 |
| z_D | main_or_control | -0.040 | 0.014 | [-0.067, -0.013] | 0.0036 |
| z_F | main_or_control | 0.435 | 0.017 | [0.402, 0.468] | 0.0000 |
| domain_education | main_or_control | 0.255 | 0.041 | [0.175, 0.334] | 0.0000 |
| domain_health | main_or_control | 0.577 | 0.048 | [0.482, 0.671] | 0.0000 |
| z_H:x:domain_education | interaction | -0.015 | 0.022 | [-0.059, 0.029] | 0.4927 |
| z_H:x:domain_health | interaction | 0.043 | 0.023 | [-0.002, 0.088] | 0.0638 |
| z_E:x:domain_education | interaction | -0.100 | 0.041 | [-0.181, -0.019] | 0.0157 |
| z_E:x:domain_health | interaction | -0.105 | 0.037 | [-0.177, -0.034] | 0.0040 |
| z_D:x:domain_education | interaction | -0.004 | 0.041 | [-0.085, 0.077] | 0.9285 |
| z_D:x:domain_health | interaction | -0.213 | 0.061 | [-0.334, -0.093] | 0.0005 |
| z_F:x:domain_education | interaction | 0.043 | 0.042 | [-0.039, 0.126] | 0.3030 |
| z_F:x:domain_health | interaction | -0.375 | 0.030 | [-0.433, -0.317] | 0.0000 |

## Reading guidance

- R² differences across domain-specific CV models are descriptive unless the interaction terms support slope differences.
- Health remains constrained by its ceiling effect and missing HuMT rows; interaction estimates should be interpreted with that limitation.
- Significant interactions are associations, not evidence that a dimension causes appropriateness.
