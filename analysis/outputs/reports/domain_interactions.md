# Domain interaction audit (Phase 5)

This model tests whether the association between each PERSONA dimension and `OA` varies by domain. Predictors `H`, `E`, `D`, and `F` are z-scored over complete cases. Mental health is the reference domain. Uncertainty uses cluster-robust standard errors with clusters defined as `domain::prompt_id`.

The model is interpretive, not causal. A domain interaction estimates how much the slope for a dimension differs from the mental-health slope in that domain.

## Model fit

| N | Prompt clusters | R² | Adj. R² | Condition number |
|---:|---:|---:|---:|---:|
| 1490 | 499 | 0.651 | 0.648 | 9.68 |

## Interaction terms

| Term | Estimate | 95% CI | p | Interpretation |
|---|---:|---|---:|---|
| z_H:x:domain_education | -0.015 | [-0.060, 0.029] | 0.4988 | no clear slope difference |
| z_H:x:domain_health | 0.043 | [-0.002, 0.088] | 0.0639 | no clear slope difference |
| z_E:x:domain_education | -0.100 | [-0.183, -0.017] | 0.0177 | differs from mental-health slope |
| z_E:x:domain_health | -0.105 | [-0.178, -0.033] | 0.0041 | differs from mental-health slope |
| z_D:x:domain_education | -0.007 | [-0.088, 0.074] | 0.8714 | no clear slope difference |
| z_D:x:domain_health | -0.215 | [-0.336, -0.093] | 0.0005 | differs from mental-health slope |
| z_F:x:domain_education | 0.052 | [-0.032, 0.135] | 0.2262 | no clear slope difference |
| z_F:x:domain_health | -0.378 | [-0.437, -0.319] | 0.0000 | differs from mental-health slope |

## All coefficients

| Term | Type | Estimate | SE | 95% CI | p |
|---|---|---:|---:|---|---:|
| const | main_or_control | 4.177 | 0.024 | [4.130, 4.224] | 0.0000 |
| z_H | main_or_control | -0.027 | 0.014 | [-0.055, 0.000] | 0.0518 |
| z_E | main_or_control | 0.089 | 0.027 | [0.037, 0.141] | 0.0008 |
| z_D | main_or_control | -0.040 | 0.014 | [-0.068, -0.013] | 0.0036 |
| z_F | main_or_control | 0.439 | 0.017 | [0.405, 0.472] | 0.0000 |
| domain_education | main_or_control | 0.263 | 0.041 | [0.182, 0.345] | 0.0000 |
| domain_health | main_or_control | 0.570 | 0.049 | [0.475, 0.666] | 0.0000 |
| z_H:x:domain_education | interaction | -0.015 | 0.023 | [-0.060, 0.029] | 0.4988 |
| z_H:x:domain_health | interaction | 0.043 | 0.023 | [-0.002, 0.088] | 0.0639 |
| z_E:x:domain_education | interaction | -0.100 | 0.042 | [-0.183, -0.017] | 0.0177 |
| z_E:x:domain_health | interaction | -0.105 | 0.037 | [-0.178, -0.033] | 0.0041 |
| z_D:x:domain_education | interaction | -0.007 | 0.041 | [-0.088, 0.074] | 0.8714 |
| z_D:x:domain_health | interaction | -0.215 | 0.062 | [-0.336, -0.093] | 0.0005 |
| z_F:x:domain_education | interaction | 0.052 | 0.043 | [-0.032, 0.135] | 0.2262 |
| z_F:x:domain_health | interaction | -0.378 | 0.030 | [-0.437, -0.319] | 0.0000 |

## Reading guidance

- R² differences across domain-specific CV models are descriptive unless the interaction terms support slope differences.
- Health remains constrained by its ceiling effect; interaction estimates should be interpreted with that limitation.
- Significant interactions are associations, not evidence that a dimension causes appropriateness.
