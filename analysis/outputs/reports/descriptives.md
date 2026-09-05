# Descriptive statistics and dimension separability (Phase 3)

## Consensus score distributions by domain

| Domain | Measure | N | Mean | Median | SD | IQR | Min | Max | Skew |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mental_health | OA | 660 | 4.317 | 4.200 | 0.490 | 0.800 | 1.800 | 5.000 | -0.02 |
| mental_health | E | 660 | 3.736 | 4.000 | 0.582 | 0.800 | 1.800 | 5.000 | -1.01 |
| mental_health | D | 660 | 2.093 | 2.000 | 0.760 | 1.250 | 1.000 | 4.200 | 0.15 |
| mental_health | F | 660 | 4.361 | 4.200 | 0.491 | 0.800 | 1.800 | 5.000 | -0.38 |
| mental_health | H | 660 | 0.050 | 0.051 | 0.022 | 0.029 | -0.020 | 0.129 | -0.10 |
| education | OA | 415 | 4.331 | 4.200 | 0.579 | 0.400 | 1.000 | 5.000 | -2.26 |
| education | E | 415 | 2.379 | 2.000 | 0.636 | 1.000 | 1.000 | 5.000 | 1.39 |
| education | D | 415 | 1.188 | 1.000 | 0.587 | 0.000 | 1.000 | 5.000 | 4.01 |
| education | F | 415 | 4.040 | 4.000 | 0.481 | 0.200 | 1.000 | 5.000 | -2.53 |
| education | H | 415 | 0.031 | 0.028 | 0.029 | 0.026 | -0.031 | 0.354 | 5.15 |
| health | OA | 415 | 4.852 | 5.000 | 0.402 | 0.200 | 1.800 | 5.000 | -5.36 |
| health | E | 415 | 2.516 | 2.200 | 0.888 | 1.000 | 1.200 | 5.000 | 1.27 |
| health | D | 415 | 1.286 | 1.200 | 0.636 | 0.200 | 1.000 | 5.000 | 3.61 |
| health | F | 415 | 4.181 | 4.200 | 0.692 | 1.000 | 1.800 | 5.000 | -0.56 |
| health | H | 415 | 0.031 | 0.033 | 0.023 | 0.033 | -0.037 | 0.094 | -0.13 |

## Ceiling and floor diagnostics

`pct_at_scale_max` counts responses whose five-rater consensus sits exactly on the top of the scale. A high value means the outcome has almost no variance left to explain.

| Domain | Measure | N | % at ceiling | % at floor | % >= 4.2 | SD | SD as % of range |
|---|---|---:|---:|---:|---:|---:|---:|
| mental_health | OA | 660 | 20.91 | 0.0 | 55.61 | 0.49 | 12.24 |
| mental_health | E | 660 | 1.97 | 0.0 | 20.76 | 0.582 | 14.56 |
| mental_health | D | 660 | 0.0 | 16.67 | 0.3 | 0.76 | 19.01 |
| mental_health | F | 660 | 23.18 | 0.0 | 63.03 | 0.491 | 12.28 |
| mental_health | H | 660 | - | - | - | 0.022 | 14.84 |
| education | OA | 415 | 21.93 | 0.24 | 80.48 | 0.579 | 14.47 |
| education | E | 415 | 0.24 | 0.48 | 0.24 | 0.636 | 15.91 |
| education | D | 415 | 0.72 | 87.23 | 0.96 | 0.587 | 14.67 |
| education | F | 415 | 5.78 | 0.24 | 25.78 | 0.481 | 12.04 |
| education | H | 415 | - | - | - | 0.0295 | 7.68 |
| health | OA | 415 | 63.86 | 0.0 | 96.14 | 0.402 | 10.06 |
| health | E | 415 | 1.69 | 0.0 | 7.71 | 0.888 | 22.21 |
| health | D | 415 | 0.48 | 49.4 | 1.2 | 0.636 | 15.9 |
| health | F | 415 | 21.45 | 0.0 | 53.49 | 0.692 | 17.31 |
| health | H | 415 | - | - | - | 0.0231 | 17.7 |

## Model profiles

| Domain | Model | N | OA | E | D | F | H |
|---|---|---:|---:|---:|---:|---:|---:|
| education | claude_opus_4_8 | 139 | 4.455 | 2.683 | 1.229 | 4.108 | 0.0315 |
| education | glm | 138 | 4.259 | 2.336 | 1.245 | 4.001 | 0.0325 |
| education | gpt_5_6 | 138 | 4.277 | 2.116 | 1.091 | 4.012 | 0.0279 |
| health | claude_opus_4_8 | 140 | 4.883 | 2.661 | 1.276 | 4.241 | 0.0364 |
| health | glm | 139 | 4.786 | 2.514 | 1.344 | 4.141 | 0.0291 |
| health | gpt_5_6 | 136 | 4.888 | 2.368 | 1.237 | 4.160 | 0.0261 |
| mental_health | claude_opus_4_8 | 220 | 4.133 | 3.873 | 2.254 | 4.170 | 0.0535 |
| mental_health | glm | 220 | 4.098 | 3.655 | 2.205 | 4.142 | 0.0553 |
| mental_health | gpt_5_6 | 220 | 4.720 | 3.682 | 1.819 | 4.770 | 0.0405 |

## Pairwise associations

Spearman rho with 95 per cent prompt-cluster bootstrap intervals and Benjamini-Hochberg corrected p-values.

| Domain | Pair | N | rho | 95% CI | FDR p | CI excludes 0 |
|---|---|---:|---:|---|---:|---|
| mental_health | H-OA | 660 | -0.167 | [-0.245, -0.088] | 0.0001 | yes |
| mental_health | H-E | 660 | 0.182 | [0.106, 0.258] | 0.0000 | yes |
| mental_health | H-D | 660 | 0.270 | [0.193, 0.346] | 0.0000 | yes |
| mental_health | H-F | 660 | -0.159 | [-0.240, -0.068] | 0.0001 | yes |
| mental_health | OA-E | 660 | 0.096 | [0.011, 0.178] | 0.0255 | yes |
| mental_health | OA-D | 660 | -0.159 | [-0.230, -0.083] | 0.0001 | yes |
| mental_health | OA-F | 660 | 0.694 | [0.649, 0.733] | 0.0000 | yes |
| mental_health | E-D | 660 | 0.341 | [0.264, 0.419] | 0.0000 | yes |
| mental_health | E-F | 660 | 0.037 | [-0.047, 0.117] | 0.4319 | no |
| mental_health | D-F | 660 | -0.162 | [-0.232, -0.088] | 0.0001 | yes |
| education | H-OA | 415 | -0.041 | [-0.156, 0.073] | 0.4620 | no |
| education | H-E | 415 | 0.085 | [-0.017, 0.192] | 0.1446 | no |
| education | H-D | 415 | 0.174 | [0.062, 0.279] | 0.0009 | yes |
| education | H-F | 415 | -0.049 | [-0.157, 0.055] | 0.4319 | no |
| education | OA-E | 415 | -0.042 | [-0.145, 0.067] | 0.4620 | no |
| education | OA-D | 415 | -0.039 | [-0.157, 0.100] | 0.4696 | no |
| education | OA-F | 415 | 0.219 | [0.086, 0.339] | 0.0000 | yes |
| education | E-D | 415 | 0.493 | [0.379, 0.581] | 0.0000 | yes |
| education | E-F | 415 | 0.075 | [-0.041, 0.185] | 0.2089 | no |
| education | D-F | 415 | -0.012 | [-0.129, 0.091] | 0.8385 | no |
| health | H-OA | 415 | -0.046 | [-0.152, 0.064] | 0.4319 | no |
| health | H-E | 415 | 0.301 | [0.195, 0.399] | 0.0000 | yes |
| health | H-D | 415 | 0.140 | [0.025, 0.252] | 0.0091 | yes |
| health | H-F | 415 | 0.034 | [-0.088, 0.152] | 0.5307 | no |
| health | OA-E | 415 | -0.066 | [-0.172, 0.041] | 0.2714 | no |
| health | OA-D | 415 | -0.074 | [-0.184, 0.040] | 0.2096 | no |
| health | OA-F | 415 | 0.060 | [-0.046, 0.174] | 0.3210 | no |
| health | E-D | 415 | 0.318 | [0.208, 0.419] | 0.0000 | yes |
| health | E-F | 415 | 0.131 | [0.006, 0.244] | 0.0152 | yes |
| health | D-F | 415 | 0.010 | [-0.115, 0.138] | 0.8468 | no |

## Construct relationship audit

Pearson and Spearman associations are shown together because concentrated ordinal scores and ties can produce materially different linear and rank relationships.

| Domain | Predictor vs OA | N | Spearman rho | 95% CI | Pearson r |
|---|---|---:|---:|---|---:|
| education | H | 415 | -0.041 | [-0.156, 0.073] | -0.349 |
| education | E | 415 | -0.042 | [-0.145, 0.067] | 0.015 |
| education | D | 415 | -0.039 | [-0.157, 0.100] | -0.186 |
| education | F | 415 | 0.219 | [0.086, 0.339] | 0.756 |
| health | H | 415 | -0.046 | [-0.152, 0.064] | -0.083 |
| health | E | 415 | -0.066 | [-0.172, 0.041] | -0.242 |
| health | D | 415 | -0.074 | [-0.184, 0.040] | -0.535 |
| health | F | 415 | 0.060 | [-0.046, 0.174] | 0.242 |
| mental_health | H | 660 | -0.167 | [-0.245, -0.088] | -0.184 |
| mental_health | E | 660 | 0.096 | [0.011, 0.178] | 0.136 |
| mental_health | D | 660 | -0.159 | [-0.230, -0.083] | -0.203 |
| mental_health | F | 660 | 0.694 | [0.649, 0.733] | 0.809 |

## F/OA disagreement audit

This post-analysis diagnostic applies the same fixed directional screens in every domain: F >= 4 with OA <= 3, or F <= 3 with OA >= 4. The absolute-gap column counts |F - OA| >= 2.

| Domain | N | High F / low OA | Low F / high OA | Absolute gap >= 2 | % directional | % gap >= 2 |
|---|---:|---:|---:|---:|---:|---:|
| mental_health | 660 | 0 | 1 | 0 | 0.15 | 0.00 |
| education | 415 | 0 | 0 | 0 | 0.00 | 0.00 |
| health | 415 | 1 | 42 | 33 | 10.36 | 7.95 |

## Collinearity among profile dimensions

| Domain | Dimension | N | R2 on the other three | VIF |
|---|---|---:|---:|---:|
| mental_health | H | 660 | 0.1207 | 1.137 |
| mental_health | E | 660 | 0.2238 | 1.288 |
| mental_health | D | 660 | 0.2564 | 1.345 |
| mental_health | F | 660 | 0.1007 | 1.112 |
| education | H | 415 | 0.1347 | 1.156 |
| education | E | 415 | 0.2674 | 1.365 |
| education | D | 415 | 0.2823 | 1.393 |
| education | F | 415 | 0.1697 | 1.204 |
| health | H | 415 | 0.1422 | 1.166 |
| health | E | 415 | 0.3287 | 1.49 |
| health | D | 415 | 0.2592 | 1.35 |
| health | F | 415 | 0.0555 | 1.059 |

## Condition number

Condition numbers are computed on z-scored `H`, `E`, `D`, and `F` within each domain. They are reported as a diagnostic, not as a pass/fail threshold.

| Domain | N | Condition number |
|---|---:|---:|
| mental_health | 660 | 1.838 |
| education | 415 | 1.835 |
| health | 415 | 1.964 |

## Figures

- `fig_distributions_by_domain.png` - consensus distributions for OA/E/D/F/H
- `fig_correlation_matrix.png` - separability matrix per domain
- `fig_h_vs_oa.png` - human-likeness against OA
- `fig_f_vs_oa.png` - domain fit against OA
