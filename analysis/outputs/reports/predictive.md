# Cross-validated prediction, ablation, incremental validity (Phase 4)

Cross-validation is 5-fold, grouped on `prompt_id`, repeated 20 times with independently seeded fold assignments (base seed 42). Confidence intervals come from 1000 prompt-cluster bootstrap resamples of the out-of-fold predictions; comparisons between specifications reuse the same resamples so the differences are paired.

## Sample

| Grouping | Responses | Complete cases | Excluded | Prompt groups |
|---|---:|---:|---:|---:|
| mental_health | 660 | 660 | 0 | 220 |
| education | 450 | 447 | 3 | 149 |
| health | 450 | 419 | 31 | 141 |
| pooled | 1560 | 1526 | 34 | 510 |

Rows excluded are responses with no HuMT value. Every specification within a grouping uses the identical complete-case rows, so performance differences reflect predictors only.

## Cross-validated performance

| Grouping | Specification | N | CV R² | SD across repeats | 95% CI | Spearman | Pearson | MAE | RMSE | In-sample R² |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| mental_health | H_only | 660 | 0.026 | 0.0029 | [-0.005, 0.055] | 0.152 | 0.164 | 0.417 | 0.483 | 0.034 |
| mental_health | E_only | 660 | 0.012 | 0.0033 | [-0.009, 0.031] | 0.064 | 0.112 | 0.426 | 0.486 | 0.019 |
| mental_health | D_only | 660 | 0.035 | 0.0038 | [0.000, 0.065] | 0.144 | 0.187 | 0.417 | 0.481 | 0.041 |
| mental_health | F_only | 660 | 0.651 | 0.0020 | [0.582, 0.704] | 0.673 | 0.807 | 0.220 | 0.289 | 0.654 |
| mental_health | H+E | 660 | 0.057 | 0.0036 | [0.019, 0.095] | 0.194 | 0.240 | 0.408 | 0.475 | 0.067 |
| mental_health | H+D | 660 | 0.048 | 0.0042 | [0.008, 0.088] | 0.184 | 0.220 | 0.412 | 0.477 | 0.058 |
| mental_health | H+F | 660 | 0.651 | 0.0021 | [0.583, 0.707] | 0.674 | 0.807 | 0.221 | 0.289 | 0.656 |
| mental_health | H+E+D | 660 | 0.114 | 0.0053 | [0.063, 0.165] | 0.275 | 0.338 | 0.393 | 0.460 | 0.127 |
| mental_health | H+E+F | 660 | 0.655 | 0.0026 | [0.589, 0.709] | 0.686 | 0.809 | 0.221 | 0.287 | 0.662 |
| mental_health | H+D+F | 660 | 0.651 | 0.0022 | [0.583, 0.707] | 0.674 | 0.807 | 0.221 | 0.289 | 0.657 |
| mental_health | E+D+F | 660 | 0.658 | 0.0025 | [0.596, 0.711] | 0.692 | 0.811 | 0.220 | 0.286 | 0.664 |
| mental_health | H+E+D+F | 660 | 0.659 | 0.0027 | [0.596, 0.711] | 0.690 | 0.812 | 0.220 | 0.286 | 0.666 |
| education | H_only | 447 | 0.087 | 0.0211 | [-0.054, 0.203] | 0.019 | 0.295 | 0.357 | 0.537 | 0.115 |
| education | E_only | 447 | -0.019 | 0.0108 | [-0.040, -0.011] | -0.118 | -0.153 | 0.355 | 0.567 | 0.000 |
| education | D_only | 447 | -0.008 | 0.0150 | [-0.050, 0.037] | -0.062 | 0.059 | 0.357 | 0.564 | 0.033 |
| education | F_only | 447 | 0.541 | 0.0187 | [0.277, 0.677] | 0.127 | 0.736 | 0.302 | 0.380 | 0.556 |
| education | H+E | 447 | 0.082 | 0.0210 | [-0.060, 0.200] | 0.010 | 0.286 | 0.359 | 0.538 | 0.115 |
| education | H+D | 447 | 0.071 | 0.0228 | [-0.053, 0.179] | 0.022 | 0.274 | 0.365 | 0.541 | 0.138 |
| education | H+F | 447 | 0.545 | 0.0157 | [0.288, 0.682] | 0.147 | 0.738 | 0.298 | 0.379 | 0.562 |
| education | H+E+D | 447 | 0.077 | 0.0215 | [-0.057, 0.184] | 0.012 | 0.284 | 0.368 | 0.540 | 0.146 |
| education | H+E+F | 447 | 0.545 | 0.0162 | [0.287, 0.683] | 0.148 | 0.738 | 0.298 | 0.379 | 0.564 |
| education | H+D+F | 447 | 0.543 | 0.0178 | [0.289, 0.679] | 0.141 | 0.737 | 0.299 | 0.380 | 0.566 |
| education | E+D+F | 447 | 0.538 | 0.0206 | [0.278, 0.674] | 0.122 | 0.734 | 0.302 | 0.382 | 0.560 |
| education | H+E+D+F | 447 | 0.541 | 0.0178 | [0.286, 0.678] | 0.137 | 0.736 | 0.299 | 0.380 | 0.566 |
| health | H_only | 419 | -0.007 | 0.0054 | [-0.047, 0.004] | 0.002 | 0.010 | 0.190 | 0.402 | 0.007 |
| health | E_only | 419 | 0.025 | 0.0136 | [-0.103, 0.065] | 0.042 | 0.176 | 0.196 | 0.395 | 0.059 |
| health | D_only | 419 | 0.231 | 0.0339 | [-0.147, 0.366] | 0.057 | 0.483 | 0.185 | 0.351 | 0.286 |
| health | F_only | 419 | 0.021 | 0.0135 | [-0.101, 0.068] | 0.049 | 0.166 | 0.195 | 0.396 | 0.058 |
| health | H+E | 419 | 0.023 | 0.0132 | [-0.105, 0.063] | 0.041 | 0.171 | 0.196 | 0.396 | 0.059 |
| health | H+D | 419 | 0.229 | 0.0335 | [-0.144, 0.365] | 0.062 | 0.481 | 0.185 | 0.351 | 0.287 |
| health | H+F | 419 | 0.023 | 0.0138 | [-0.118, 0.072] | 0.055 | 0.177 | 0.198 | 0.395 | 0.067 |
| health | H+E+D | 419 | 0.223 | 0.0335 | [-0.152, 0.360] | 0.055 | 0.475 | 0.186 | 0.353 | 0.287 |
| health | H+E+F | 419 | 0.071 | 0.0188 | [-0.158, 0.140] | 0.094 | 0.280 | 0.209 | 0.386 | 0.133 |
| health | H+D+F | 419 | 0.254 | 0.0302 | [-0.116, 0.387] | 0.086 | 0.506 | 0.188 | 0.346 | 0.318 |
| health | E+D+F | 419 | 0.250 | 0.0295 | [-0.128, 0.384] | 0.087 | 0.502 | 0.189 | 0.347 | 0.318 |
| health | H+E+D+F | 419 | 0.247 | 0.0296 | [-0.125, 0.383] | 0.084 | 0.500 | 0.190 | 0.347 | 0.319 |
| pooled | H_only | 1526 | 0.222 | 0.0033 | [0.165, 0.277] | 0.453 | 0.471 | 0.338 | 0.480 | 0.230 |
| pooled | E_only | 1526 | 0.182 | 0.0032 | [0.129, 0.238] | 0.354 | 0.427 | 0.342 | 0.492 | 0.190 |
| pooled | D_only | 1526 | 0.237 | 0.0041 | [0.192, 0.287] | 0.470 | 0.487 | 0.334 | 0.475 | 0.246 |
| pooled | F_only | 1526 | 0.469 | 0.0048 | [0.407, 0.524] | 0.672 | 0.685 | 0.303 | 0.397 | 0.478 |
| pooled | H+E | 1526 | 0.220 | 0.0041 | [0.159, 0.278] | 0.452 | 0.469 | 0.338 | 0.481 | 0.231 |
| pooled | H+D | 1526 | 0.256 | 0.0058 | [0.214, 0.301] | 0.480 | 0.506 | 0.333 | 0.469 | 0.270 |
| pooled | H+F | 1526 | 0.482 | 0.0045 | [0.416, 0.541] | 0.675 | 0.695 | 0.300 | 0.391 | 0.492 |
| pooled | H+E+D | 1526 | 0.269 | 0.0060 | [0.222, 0.319] | 0.494 | 0.519 | 0.333 | 0.465 | 0.284 |
| pooled | H+E+F | 1526 | 0.482 | 0.0048 | [0.416, 0.539] | 0.672 | 0.694 | 0.300 | 0.392 | 0.494 |
| pooled | H+D+F | 1526 | 0.497 | 0.0050 | [0.440, 0.550] | 0.676 | 0.705 | 0.297 | 0.386 | 0.509 |
| pooled | E+D+F | 1526 | 0.489 | 0.0049 | [0.435, 0.538] | 0.675 | 0.699 | 0.299 | 0.389 | 0.501 |
| pooled | H+E+D+F | 1526 | 0.496 | 0.0050 | [0.438, 0.551] | 0.675 | 0.705 | 0.298 | 0.386 | 0.510 |

## Incremental validity

| Grouping | Comparison | Baseline CV R² | Model CV R² | Δ | 95% CI | CI excludes 0 |
|---|---|---:|---:|---:|---|---|
| mental_health | H+E+D+F vs H_only | 0.026 | 0.659 | 0.632 | [0.567, 0.686] | yes |
| mental_health | E+D+F vs H_only | 0.026 | 0.658 | 0.632 | [0.564, 0.686] | yes |
| mental_health | H+F vs H_only | 0.026 | 0.651 | 0.625 | [0.556, 0.682] | yes |
| mental_health | F_only vs H_only | 0.026 | 0.651 | 0.625 | [0.555, 0.684] | yes |
| mental_health | H+E+D+F vs E+D+F | 0.658 | 0.659 | 0.001 | [-0.003, 0.005] | no |
| mental_health | H+E+D+F vs F_only | 0.651 | 0.659 | 0.008 | [-0.004, 0.020] | no |
| education | H+E+D+F vs H_only | 0.087 | 0.541 | 0.454 | [0.262, 0.575] | yes |
| education | E+D+F vs H_only | 0.087 | 0.538 | 0.451 | [0.248, 0.578] | yes |
| education | H+F vs H_only | 0.087 | 0.545 | 0.457 | [0.264, 0.579] | yes |
| education | F_only vs H_only | 0.087 | 0.541 | 0.454 | [0.250, 0.580] | yes |
| education | H+E+D+F vs E+D+F | 0.538 | 0.541 | 0.003 | [-0.008, 0.017] | no |
| education | H+E+D+F vs F_only | 0.541 | 0.541 | 0.000 | [-0.012, 0.019] | no |
| health | H+E+D+F vs H_only | -0.007 | 0.247 | 0.254 | [-0.088, 0.392] | no |
| health | E+D+F vs H_only | -0.007 | 0.250 | 0.257 | [-0.084, 0.394] | no |
| health | H+F vs H_only | -0.007 | 0.023 | 0.030 | [-0.080, 0.083] | no |
| health | F_only vs H_only | -0.007 | 0.021 | 0.028 | [-0.071, 0.082] | no |
| health | H+E+D+F vs E+D+F | 0.250 | 0.247 | -0.002 | [-0.009, 0.002] | no |
| health | H+E+D+F vs F_only | 0.021 | 0.247 | 0.226 | [-0.045, 0.348] | no |
| pooled | H+E+D+F vs H_only | 0.222 | 0.496 | 0.275 | [0.207, 0.341] | yes |
| pooled | E+D+F vs H_only | 0.222 | 0.489 | 0.267 | [0.199, 0.337] | yes |
| pooled | H+F vs H_only | 0.222 | 0.482 | 0.261 | [0.193, 0.322] | yes |
| pooled | F_only vs H_only | 0.222 | 0.469 | 0.247 | [0.178, 0.312] | yes |
| pooled | H+E+D+F vs E+D+F | 0.489 | 0.496 | 0.008 | [-0.003, 0.019] | no |
| pooled | H+E+D+F vs F_only | 0.469 | 0.496 | 0.028 | [0.011, 0.046] | yes |

## Ablation

Each specification is compared with the full profile on paired bootstrap resamples. `reliably worse` means the 95 per cent interval for the difference lies entirely below zero, which is the test of whether dropping a dimension actually costs predictive accuracy.

| Grouping | Specification | Dropped | CV R² | Δ vs full | 95% CI | Reliably worse |
|---|---|---|---:|---:|---|---|
| mental_health | H_only | E+D+F | 0.026 | -0.632 | [-0.686, -0.567] | yes |
| mental_health | E_only | H+D+F | 0.012 | -0.647 | [-0.703, -0.582] | yes |
| mental_health | D_only | H+E+F | 0.035 | -0.624 | [-0.679, -0.561] | yes |
| mental_health | F_only | H+E+D | 0.651 | -0.008 | [-0.020, 0.004] | no |
| mental_health | H+E | D+F | 0.057 | -0.601 | [-0.659, -0.534] | yes |
| mental_health | H+D | E+F | 0.048 | -0.611 | [-0.664, -0.543] | yes |
| mental_health | H+F | E+D | 0.651 | -0.007 | [-0.019, 0.004] | no |
| mental_health | H+E+D | F | 0.114 | -0.545 | [-0.608, -0.477] | yes |
| mental_health | H+E+F | D | 0.655 | -0.003 | [-0.010, 0.003] | no |
| mental_health | H+D+F | E | 0.651 | -0.008 | [-0.019, 0.004] | no |
| mental_health | E+D+F | H | 0.658 | -0.001 | [-0.005, 0.003] | no |
| mental_health | H+E+D+F | nothing | 0.659 | 0.000 | [0.000, 0.000] | no |
| education | H_only | E+D+F | 0.087 | -0.454 | [-0.575, -0.262] | yes |
| education | E_only | H+D+F | -0.019 | -0.560 | [-0.703, -0.317] | yes |
| education | D_only | H+E+F | -0.008 | -0.550 | [-0.702, -0.292] | yes |
| education | F_only | H+E+D | 0.541 | -0.000 | [-0.019, 0.012] | no |
| education | H+E | D+F | 0.082 | -0.459 | [-0.583, -0.267] | yes |
| education | H+D | E+F | 0.071 | -0.470 | [-0.583, -0.282] | yes |
| education | H+F | E+D | 0.545 | 0.003 | [-0.007, 0.011] | no |
| education | H+E+D | F | 0.077 | -0.465 | [-0.576, -0.285] | yes |
| education | H+E+F | D | 0.545 | 0.004 | [-0.004, 0.009] | no |
| education | H+D+F | E | 0.543 | 0.002 | [-0.000, 0.004] | no |
| education | E+D+F | H | 0.538 | -0.003 | [-0.017, 0.008] | no |
| education | H+E+D+F | nothing | 0.541 | 0.000 | [0.000, 0.000] | no |
| health | H_only | E+D+F | -0.007 | -0.254 | [-0.392, 0.088] | no |
| health | E_only | H+D+F | 0.025 | -0.222 | [-0.345, 0.037] | no |
| health | D_only | H+E+F | 0.231 | -0.016 | [-0.051, 0.036] | no |
| health | F_only | H+E+D | 0.021 | -0.226 | [-0.348, 0.045] | no |
| health | H+E | D+F | 0.023 | -0.224 | [-0.347, 0.032] | no |
| health | H+D | E+F | 0.229 | -0.018 | [-0.051, 0.030] | no |
| health | H+F | E+D | 0.023 | -0.224 | [-0.343, 0.024] | no |
| health | H+E+D | F | 0.223 | -0.025 | [-0.058, 0.024] | no |
| health | H+E+F | D | 0.071 | -0.176 | [-0.280, -0.013] | yes |
| health | H+D+F | E | 0.254 | 0.006 | [0.002, 0.011] | no |
| health | E+D+F | H | 0.250 | 0.002 | [-0.002, 0.009] | no |
| health | H+E+D+F | nothing | 0.247 | 0.000 | [0.000, 0.000] | no |
| pooled | H_only | E+D+F | 0.222 | -0.275 | [-0.341, -0.207] | yes |
| pooled | E_only | H+D+F | 0.182 | -0.315 | [-0.392, -0.229] | yes |
| pooled | D_only | H+E+F | 0.237 | -0.259 | [-0.331, -0.181] | yes |
| pooled | F_only | H+E+D | 0.469 | -0.028 | [-0.046, -0.011] | yes |
| pooled | H+E | D+F | 0.220 | -0.277 | [-0.344, -0.206] | yes |
| pooled | H+D | E+F | 0.256 | -0.240 | [-0.297, -0.179] | yes |
| pooled | H+F | E+D | 0.482 | -0.014 | [-0.032, 0.001] | no |
| pooled | H+E+D | F | 0.269 | -0.227 | [-0.282, -0.167] | yes |
| pooled | H+E+F | D | 0.482 | -0.014 | [-0.029, -0.001] | yes |
| pooled | H+D+F | E | 0.497 | 0.001 | [-0.001, 0.003] | no |
| pooled | E+D+F | H | 0.489 | -0.008 | [-0.019, 0.003] | no |
| pooled | H+E+D+F | nothing | 0.496 | 0.000 | [0.000, 0.000] | no |

## Figures

- `fig_cv_model_comparison.png`
- `fig_ablation.png`
