# Results Ground Truth for CHI Manuscript

This file records the final numbers used by `paper/persona_chi2027.tex`.
Generated outputs in `analysis/outputs/` are authoritative. Values below are
read from the current CSV outputs on this branch.

## Dataset Counts

| Domain | Responses | Prompt clusters | OA rating rows | E/D/F rating rows | HuMT complete |
|---|---:|---:|---:|---:|---:|
| Mental health | 660 | 220 | 3,300 | 3,300 | 660/660 |
| Education | 415 | 139 | 2,075 | 2,075 | 415/415 |
| Health | 415 | 140 | 2,075 | 2,075 | 415/415 |
| Pooled | 1,490 | 499 | 7,450 | 7,450 | 1,490/1,490 |

Source: `analysis/outputs/tables/data_audit.csv`,
`analysis/outputs/tables/cv_performance.csv`.

## Reliability: ICC(A,k)

| Domain | OA | E | D | F |
|---|---:|---:|---:|---:|
| Mental health | 0.851 | 0.948 | 0.959 | 0.864 |
| Education | 0.916 | 0.997 | 0.963 | 0.954 |
| Health | 0.907 | 0.939 | 0.942 | 0.922 |

Source: `analysis/outputs/tables/reliability.csv`.

## H/OA Spearman Correlations

| Domain | Spearman rho | 95% CI |
|---|---:|---|
| Mental health | -0.167 | [-0.245, -0.088] |
| Education | -0.041 | [-0.156, 0.073] |
| Health | -0.046 | [-0.152, 0.064] |

Source: `analysis/outputs/tables/correlations.csv`.

## Grouped Cross-Validated Prediction

| Domain | H-only R2 | Full P R2 | Gain | 95% CI for gain |
|---|---:|---:|---:|---|
| Mental health | 0.026 | 0.659 | 0.632 | [0.567, 0.686] |
| Education | 0.099 | 0.562 | 0.462 | [0.278, 0.598] |
| Health | -0.007 | 0.256 | 0.264 | [-0.053, 0.400] |
| Pooled | 0.221 | 0.499 | 0.278 | [0.204, 0.339] |

Source: `analysis/outputs/tables/cv_performance.csv`,
`analysis/outputs/tables/incremental_validity.csv`.

## F-Only Ablation

| Domain | F-only R2 | Full P R2 | Full minus F-only | 95% CI |
|---|---:|---:|---:|---|
| Mental health | 0.651 | 0.659 | 0.008 | [-0.004, 0.020] |
| Education | 0.562 | 0.562 | -0.000 | [-0.014, 0.020] |
| Health | 0.027 | 0.256 | 0.230 | [-0.031, 0.348] |
| Pooled | 0.471 | 0.499 | 0.028 | [0.010, 0.046] |

Source: `analysis/outputs/tables/ablation.csv`,
`analysis/outputs/tables/incremental_validity.csv`.

## Ceiling/Floor Diagnostics

| Domain | OA mean | OA ceiling | D floor |
|---|---:|---:|---:|
| Mental health | 4.317 | 20.91% | 16.67% |
| Education | 4.327 | 21.93% | 87.23% |
| Health | 4.860 | 63.86% | 49.40% |

Source: `analysis/processed/persona_all.csv`,
`analysis/outputs/tables/ceiling_floor.csv`.

## Domain Interaction Model

Model: `OA ~ z(H,E,D,F) * domain`

| Quantity | Value |
|---|---:|
| N | 1,490 |
| Prompt clusters | 499 |
| R2 | 0.651 |
| Adjusted R2 | 0.648 |
| Condition number | 9.68 |

| Interaction | Estimate | 95% CI | p |
|---|---:|---|---:|
| H x Education | -0.015 | [-0.060, 0.029] | 0.499 |
| H x Health | 0.043 | [-0.002, 0.088] | 0.064 |
| E x Education | -0.100 | [-0.183, -0.017] | 0.018 |
| E x Health | -0.105 | [-0.178, -0.033] | 0.004 |
| D x Education | -0.007 | [-0.088, 0.074] | 0.871 |
| D x Health | -0.215 | [-0.336, -0.093] | 0.001 |
| F x Education | 0.052 | [-0.032, 0.135] | 0.226 |
| F x Health | -0.378 | [-0.437, -0.319] | <0.001 |

Source: `analysis/outputs/tables/domain_interaction_model_fit.csv`,
`analysis/outputs/tables/domain_interactions.csv`.

## VIF

| Domain | Max VIF |
|---|---:|
| Mental health | 1.345 |
| Education | 1.393 |
| Health | 1.490 |

Source: `analysis/outputs/tables/collinearity_vif.csv`.

## Notes on Prompt-Supplied Numbers

The revision prompt included some values that differ slightly from the current
generated CSV outputs, including health H/OA Spearman, education/health ICCs,
education OA ceiling, health OA ceiling, domain interaction estimates, and
condition number. The manuscript follows the generated CSV outputs because the
prompt instructs that regenerated analysis outputs are authoritative.
