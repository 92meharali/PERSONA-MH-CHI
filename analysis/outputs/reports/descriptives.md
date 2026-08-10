# Descriptive statistics and dimension separability (Phase 3)

## Consensus score distributions by domain

| Domain | Measure | N | Mean | Median | SD | IQR | Min | Max | Skew |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mental_health | OA | 660 | 4.317 | 4.200 | 0.490 | 0.800 | 1.800 | 5.000 | -0.02 |
| mental_health | E | 660 | 3.736 | 4.000 | 0.582 | 0.800 | 1.800 | 5.000 | -1.01 |
| mental_health | D | 660 | 2.093 | 2.000 | 0.760 | 1.250 | 1.000 | 4.200 | 0.15 |
| mental_health | F | 660 | 4.361 | 4.200 | 0.491 | 0.800 | 1.800 | 5.000 | -0.38 |
| mental_health | H | 660 | 0.050 | 0.051 | 0.022 | 0.029 | -0.020 | 0.129 | -0.10 |
| education | OA | 450 | 4.313 | 4.200 | 0.592 | 0.400 | 1.000 | 5.000 | -2.26 |
| education | E | 450 | 2.369 | 2.000 | 0.623 | 1.000 | 1.000 | 5.000 | 1.42 |
| education | D | 450 | 1.174 | 1.000 | 0.566 | 0.000 | 1.000 | 5.000 | 4.21 |
| education | F | 450 | 4.034 | 4.000 | 0.496 | 0.200 | 1.000 | 5.000 | -2.53 |
| education | H | 447 | 0.030 | 0.028 | 0.029 | 0.027 | -0.031 | 0.354 | 5.08 |
| health | OA | 450 | 4.854 | 5.000 | 0.390 | 0.200 | 1.800 | 5.000 | -5.44 |
| health | E | 450 | 2.496 | 2.100 | 0.879 | 1.000 | 1.200 | 5.000 | 1.30 |
| health | D | 450 | 1.281 | 1.200 | 0.613 | 0.200 | 1.000 | 5.000 | 3.74 |
| health | F | 450 | 4.190 | 4.200 | 0.683 | 1.000 | 1.800 | 5.000 | -0.57 |
| health | H | 419 | 0.031 | 0.032 | 0.023 | 0.032 | -0.037 | 0.094 | -0.12 |

## Ceiling and floor diagnostics

`pct_at_scale_max` counts responses whose five-rater consensus sits exactly on the top of the scale. A high value means the outcome has almost no variance left to explain.

| Domain | Measure | N | % at ceiling | % at floor | % >= 4.2 | SD | SD as % of range |
|---|---|---:|---:|---:|---:|---:|---:|
| mental_health | OA | 660 | 20.91 | 0.0 | 55.61 | 0.49 | 12.24 |
| mental_health | E | 660 | 1.97 | 0.0 | 20.76 | 0.582 | 14.56 |
| mental_health | D | 660 | 0.0 | 16.67 | 0.3 | 0.76 | 19.01 |
| mental_health | F | 660 | 23.18 | 0.0 | 63.03 | 0.491 | 12.28 |
| mental_health | H | 660 | - | - | - | 0.022 | 14.84 |
| education | OA | 450 | 20.89 | 0.22 | 80.22 | 0.592 | 14.79 |
| education | E | 450 | 0.22 | 0.44 | 0.22 | 0.623 | 15.58 |
| education | D | 450 | 0.67 | 88.22 | 0.89 | 0.566 | 14.14 |
| education | F | 450 | 5.56 | 0.22 | 27.11 | 0.496 | 12.41 |
| education | H | 447 | - | - | - | 0.029 | 7.55 |
| health | OA | 450 | 63.33 | 0.0 | 96.22 | 0.39 | 9.76 |
| health | E | 450 | 1.56 | 0.0 | 7.33 | 0.879 | 21.97 |
| health | D | 450 | 0.44 | 47.33 | 1.11 | 0.613 | 15.33 |
| health | F | 450 | 21.11 | 0.0 | 53.56 | 0.683 | 17.07 |
| health | H | 419 | - | - | - | 0.023 | 17.62 |

## Model profiles

| Domain | Model | N | OA | E | D | F | H |
|---|---|---:|---:|---:|---:|---:|---:|
| education | claude_opus_4_8 | 149 | 4.455 | 2.678 | 1.213 | 4.119 | 0.0309 |
| education | glm | 149 | 4.259 | 2.329 | 1.227 | 4.012 | 0.0323 |
| education | gpt_5_6 | 149 | 4.272 | 2.107 | 1.085 | 4.012 | 0.0267 |
| health | claude_opus_4_8 | 141 | 4.882 | 2.657 | 1.277 | 4.238 | 0.0364 |
| health | glm | 141 | 4.789 | 2.506 | 1.342 | 4.145 | 0.0290 |
| health | gpt_5_6 | 141 | 4.888 | 2.349 | 1.237 | 4.167 | 0.0261 |
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
| mental_health | OA-E | 660 | 0.096 | [0.011, 0.178] | 0.0272 | yes |
| mental_health | OA-D | 660 | -0.159 | [-0.230, -0.083] | 0.0001 | yes |
| mental_health | OA-F | 660 | 0.694 | [0.649, 0.733] | 0.0000 | yes |
| mental_health | E-D | 660 | 0.341 | [0.264, 0.419] | 0.0000 | yes |
| mental_health | E-F | 660 | 0.037 | [-0.047, 0.117] | 0.4796 | no |
| mental_health | D-F | 660 | -0.162 | [-0.232, -0.088] | 0.0001 | yes |
| education | H-OA | 447 | -0.035 | [-0.151, 0.074] | 0.5555 | no |
| education | H-E | 447 | 0.079 | [-0.015, 0.180] | 0.1555 | no |
| education | H-D | 447 | 0.175 | [0.069, 0.270] | 0.0005 | yes |
| education | H-F | 447 | -0.035 | [-0.137, 0.073] | 0.5555 | no |
| education | OA-E | 450 | -0.030 | [-0.137, 0.072] | 0.5785 | no |
| education | OA-D | 450 | -0.028 | [-0.144, 0.101] | 0.5948 | no |
| education | OA-F | 450 | 0.229 | [0.095, 0.348] | 0.0000 | yes |
| education | E-D | 450 | 0.479 | [0.372, 0.571] | 0.0000 | yes |
| education | E-F | 450 | 0.090 | [-0.021, 0.194] | 0.1020 | no |
| education | D-F | 450 | -0.015 | [-0.120, 0.083] | 0.7768 | no |
| health | H-OA | 419 | -0.045 | [-0.155, 0.067] | 0.4796 | no |
| health | H-E | 419 | 0.302 | [0.198, 0.402] | 0.0000 | yes |
| health | H-D | 419 | 0.140 | [0.018, 0.255] | 0.0089 | yes |
| health | H-F | 419 | 0.034 | [-0.081, 0.162] | 0.5653 | no |
| health | OA-E | 450 | -0.060 | [-0.161, 0.032] | 0.3030 | no |
| health | OA-D | 450 | -0.069 | [-0.181, 0.038] | 0.2306 | no |
| health | OA-F | 450 | 0.043 | [-0.061, 0.150] | 0.4796 | no |
| health | E-D | 450 | 0.292 | [0.184, 0.391] | 0.0000 | yes |
| health | E-F | 450 | 0.115 | [-0.003, 0.225] | 0.0281 | no |
| health | D-F | 450 | -0.006 | [-0.120, 0.104] | 0.8956 | no |

## Collinearity among profile dimensions

| Domain | Dimension | N | R2 on the other three | VIF |
|---|---|---:|---:|---:|
| mental_health | H | 660 | 0.1207 | 1.137 |
| mental_health | E | 660 | 0.2238 | 1.288 |
| mental_health | D | 660 | 0.2564 | 1.345 |
| mental_health | F | 660 | 0.1007 | 1.112 |
| education | H | 447 | 0.1277 | 1.146 |
| education | E | 447 | 0.2602 | 1.352 |
| education | D | 447 | 0.2765 | 1.382 |
| education | F | 447 | 0.1623 | 1.194 |
| health | H | 419 | 0.1427 | 1.166 |
| health | E | 419 | 0.3288 | 1.49 |
| health | D | 419 | 0.2594 | 1.35 |
| health | F | 419 | 0.0559 | 1.059 |

## Figures

- `fig_distributions_by_domain.png` - consensus distributions for OA/E/D/F/H
- `fig_correlation_matrix.png` - separability matrix per domain
- `fig_h_vs_oa.png` - human-likeness against OA
- `fig_f_vs_oa.png` - contextual fit against OA
