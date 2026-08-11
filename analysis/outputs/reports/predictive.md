# Cross-validated prediction, ablation, incremental validity (Phase 4)

Cross-validation is 5-fold, grouped on `prompt_id`, repeated 20 times with independently seeded fold assignments (base seed 42). Confidence intervals come from 1000 prompt-cluster bootstrap resamples of the out-of-fold predictions; comparisons between specifications reuse the same resamples so the differences are paired.

## Sample

| Grouping | Responses | Complete cases | Excluded | Prompt groups |
|---|---:|---:|---:|---:|
| mental_health | 660 | 660 | 0 | 220 |
| education | 415 | 415 | 0 | 139 |
| health | 415 | 415 | 0 | 140 |
| pooled | 1490 | 1490 | 0 | 499 |

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
| education | H_only | 415 | 0.099 | 0.0144 | [-0.084, 0.224] | 0.029 | 0.316 | 0.367 | 0.549 | 0.122 |
| education | E_only | 415 | -0.020 | 0.0110 | [-0.048, -0.012] | -0.118 | -0.161 | 0.366 | 0.584 | 0.000 |
| education | D_only | 415 | 0.001 | 0.0130 | [-0.048, 0.063] | -0.042 | 0.088 | 0.365 | 0.578 | 0.035 |
| education | F_only | 415 | 0.562 | 0.0044 | [0.284, 0.697] | 0.140 | 0.750 | 0.306 | 0.383 | 0.571 |
| education | H+E | 415 | 0.091 | 0.0154 | [-0.093, 0.217] | 0.016 | 0.303 | 0.368 | 0.551 | 0.122 |
| education | H+D | 415 | 0.093 | 0.0211 | [-0.074, 0.209] | 0.040 | 0.309 | 0.373 | 0.551 | 0.145 |
| education | H+F | 415 | 0.565 | 0.0057 | [0.288, 0.698] | 0.154 | 0.752 | 0.303 | 0.381 | 0.578 |
| education | H+E+D | 415 | 0.099 | 0.0207 | [-0.079, 0.215] | 0.030 | 0.320 | 0.377 | 0.549 | 0.154 |
| education | H+E+F | 415 | 0.564 | 0.0063 | [0.286, 0.698] | 0.157 | 0.751 | 0.302 | 0.382 | 0.579 |
| education | H+D+F | 415 | 0.564 | 0.0075 | [0.295, 0.697] | 0.150 | 0.751 | 0.303 | 0.382 | 0.582 |
| education | E+D+F | 415 | 0.559 | 0.0062 | [0.288, 0.692] | 0.135 | 0.748 | 0.306 | 0.384 | 0.576 |
| education | H+E+D+F | 415 | 0.562 | 0.0072 | [0.292, 0.695] | 0.147 | 0.749 | 0.304 | 0.383 | 0.582 |
| health | H_only | 415 | -0.007 | 0.0053 | [-0.052, 0.004] | -0.005 | 0.008 | 0.191 | 0.403 | 0.007 |
| health | E_only | 415 | 0.033 | 0.0103 | [-0.098, 0.075] | 0.048 | 0.191 | 0.196 | 0.395 | 0.059 |
| health | D_only | 415 | 0.241 | 0.0301 | [-0.099, 0.368] | 0.051 | 0.493 | 0.185 | 0.350 | 0.287 |
| health | F_only | 415 | 0.027 | 0.0160 | [-0.106, 0.074] | 0.043 | 0.177 | 0.197 | 0.397 | 0.058 |
| health | H+E | 415 | 0.031 | 0.0102 | [-0.101, 0.073] | 0.044 | 0.186 | 0.197 | 0.396 | 0.059 |
| health | H+D | 415 | 0.239 | 0.0300 | [-0.102, 0.369] | 0.060 | 0.492 | 0.185 | 0.350 | 0.288 |
| health | H+F | 415 | 0.029 | 0.0155 | [-0.124, 0.078] | 0.053 | 0.186 | 0.199 | 0.396 | 0.067 |
| health | H+E+D | 415 | 0.232 | 0.0310 | [-0.113, 0.364] | 0.055 | 0.486 | 0.186 | 0.352 | 0.288 |
| health | H+E+F | 415 | 0.083 | 0.0203 | [-0.166, 0.158] | 0.096 | 0.296 | 0.208 | 0.385 | 0.133 |
| health | H+D+F | 415 | 0.262 | 0.0297 | [-0.082, 0.394] | 0.084 | 0.515 | 0.189 | 0.345 | 0.319 |
| health | E+D+F | 415 | 0.258 | 0.0296 | [-0.081, 0.391] | 0.085 | 0.511 | 0.189 | 0.346 | 0.319 |
| health | H+E+D+F | 415 | 0.256 | 0.0294 | [-0.089, 0.390] | 0.083 | 0.510 | 0.190 | 0.347 | 0.320 |
| pooled | H_only | 1490 | 0.221 | 0.0024 | [0.162, 0.280] | 0.455 | 0.470 | 0.342 | 0.484 | 0.229 |
| pooled | E_only | 1490 | 0.180 | 0.0036 | [0.129, 0.236] | 0.362 | 0.424 | 0.345 | 0.496 | 0.188 |
| pooled | D_only | 1490 | 0.235 | 0.0050 | [0.189, 0.286] | 0.473 | 0.485 | 0.337 | 0.480 | 0.245 |
| pooled | F_only | 1490 | 0.471 | 0.0026 | [0.408, 0.527] | 0.673 | 0.686 | 0.305 | 0.399 | 0.479 |
| pooled | H+E | 1490 | 0.219 | 0.0031 | [0.157, 0.279] | 0.454 | 0.468 | 0.342 | 0.485 | 0.230 |
| pooled | H+D | 1490 | 0.255 | 0.0043 | [0.209, 0.297] | 0.482 | 0.505 | 0.336 | 0.473 | 0.270 |
| pooled | H+F | 1490 | 0.484 | 0.0022 | [0.418, 0.544] | 0.676 | 0.696 | 0.302 | 0.394 | 0.494 |
| pooled | H+E+D | 1490 | 0.269 | 0.0042 | [0.218, 0.316] | 0.496 | 0.519 | 0.336 | 0.469 | 0.284 |
| pooled | H+E+F | 1490 | 0.484 | 0.0023 | [0.418, 0.541] | 0.674 | 0.696 | 0.302 | 0.394 | 0.496 |
| pooled | H+D+F | 1490 | 0.500 | 0.0030 | [0.440, 0.552] | 0.678 | 0.707 | 0.299 | 0.388 | 0.511 |
| pooled | E+D+F | 1490 | 0.492 | 0.0037 | [0.437, 0.541] | 0.677 | 0.701 | 0.301 | 0.391 | 0.503 |
| pooled | H+E+D+F | 1490 | 0.499 | 0.0029 | [0.439, 0.552] | 0.678 | 0.706 | 0.299 | 0.388 | 0.512 |

## Incremental validity

| Grouping | Comparison | Baseline CV R² | Model CV R² | Δ | 95% CI | CI excludes 0 |
|---|---|---:|---:|---:|---|---|
| mental_health | H+E+D+F vs H_only | 0.026 | 0.659 | 0.632 | [0.567, 0.686] | yes |
| mental_health | E+D+F vs H_only | 0.026 | 0.658 | 0.632 | [0.564, 0.686] | yes |
| mental_health | H+F vs H_only | 0.026 | 0.651 | 0.625 | [0.556, 0.682] | yes |
| mental_health | F_only vs H_only | 0.026 | 0.651 | 0.625 | [0.555, 0.684] | yes |
| mental_health | H+E+D+F vs E+D+F | 0.658 | 0.659 | 0.001 | [-0.003, 0.005] | no |
| mental_health | H+E+D+F vs F_only | 0.651 | 0.659 | 0.008 | [-0.004, 0.020] | no |
| education | H+E+D+F vs H_only | 0.099 | 0.562 | 0.462 | [0.278, 0.598] | yes |
| education | E+D+F vs H_only | 0.099 | 0.559 | 0.460 | [0.267, 0.600] | yes |
| education | H+F vs H_only | 0.099 | 0.565 | 0.466 | [0.280, 0.601] | yes |
| education | F_only vs H_only | 0.099 | 0.562 | 0.463 | [0.267, 0.604] | yes |
| education | H+E+D+F vs E+D+F | 0.559 | 0.562 | 0.003 | [-0.008, 0.015] | no |
| education | H+E+D+F vs F_only | 0.562 | 0.562 | -0.000 | [-0.014, 0.020] | no |
| health | H+E+D+F vs H_only | -0.007 | 0.256 | 0.264 | [-0.053, 0.400] | no |
| health | E+D+F vs H_only | -0.007 | 0.258 | 0.266 | [-0.051, 0.401] | no |
| health | H+F vs H_only | -0.007 | 0.029 | 0.036 | [-0.083, 0.087] | no |
| health | F_only vs H_only | -0.007 | 0.027 | 0.034 | [-0.072, 0.087] | no |
| health | H+E+D+F vs E+D+F | 0.258 | 0.256 | -0.002 | [-0.008, 0.003] | no |
| health | H+E+D+F vs F_only | 0.027 | 0.256 | 0.230 | [-0.031, 0.348] | no |
| pooled | H+E+D+F vs H_only | 0.221 | 0.499 | 0.278 | [0.204, 0.339] | yes |
| pooled | E+D+F vs H_only | 0.221 | 0.492 | 0.271 | [0.196, 0.335] | yes |
| pooled | H+F vs H_only | 0.221 | 0.484 | 0.263 | [0.195, 0.321] | yes |
| pooled | F_only vs H_only | 0.221 | 0.471 | 0.250 | [0.180, 0.311] | yes |
| pooled | H+E+D+F vs E+D+F | 0.492 | 0.499 | 0.007 | [-0.003, 0.018] | no |
| pooled | H+E+D+F vs F_only | 0.471 | 0.499 | 0.028 | [0.010, 0.046] | yes |

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
| education | H_only | E+D+F | 0.099 | -0.462 | [-0.598, -0.278] | yes |
| education | E_only | H+D+F | -0.020 | -0.582 | [-0.724, -0.321] | yes |
| education | D_only | H+E+F | 0.001 | -0.560 | [-0.705, -0.286] | yes |
| education | F_only | H+E+D | 0.562 | 0.000 | [-0.020, 0.014] | no |
| education | H+E | D+F | 0.091 | -0.471 | [-0.607, -0.287] | yes |
| education | H+D | E+F | 0.093 | -0.469 | [-0.597, -0.281] | yes |
| education | H+F | E+D | 0.565 | 0.003 | [-0.011, 0.012] | no |
| education | H+E+D | F | 0.099 | -0.462 | [-0.587, -0.283] | yes |
| education | H+E+F | D | 0.564 | 0.003 | [-0.007, 0.010] | no |
| education | H+D+F | E | 0.564 | 0.002 | [-0.000, 0.005] | no |
| education | E+D+F | H | 0.559 | -0.003 | [-0.015, 0.008] | no |
| education | H+E+D+F | nothing | 0.562 | 0.000 | [0.000, 0.000] | no |
| health | H_only | E+D+F | -0.007 | -0.264 | [-0.400, 0.053] | no |
| health | E_only | H+D+F | 0.033 | -0.223 | [-0.344, 0.016] | no |
| health | D_only | H+E+F | 0.241 | -0.015 | [-0.050, 0.047] | no |
| health | F_only | H+E+D | 0.027 | -0.230 | [-0.348, 0.031] | no |
| health | H+E | D+F | 0.031 | -0.226 | [-0.346, 0.010] | no |
| health | H+D | E+F | 0.239 | -0.017 | [-0.050, 0.042] | no |
| health | H+F | E+D | 0.029 | -0.228 | [-0.341, 0.012] | no |
| health | H+E+D | F | 0.232 | -0.024 | [-0.056, 0.034] | no |
| health | H+E+F | D | 0.083 | -0.174 | [-0.276, -0.007] | yes |
| health | H+D+F | E | 0.262 | 0.006 | [0.002, 0.012] | no |
| health | E+D+F | H | 0.258 | 0.002 | [-0.003, 0.008] | no |
| health | H+E+D+F | nothing | 0.256 | 0.000 | [0.000, 0.000] | no |
| pooled | H_only | E+D+F | 0.221 | -0.278 | [-0.339, -0.204] | yes |
| pooled | E_only | H+D+F | 0.180 | -0.319 | [-0.390, -0.230] | yes |
| pooled | D_only | H+E+F | 0.235 | -0.264 | [-0.335, -0.187] | yes |
| pooled | F_only | H+E+D | 0.471 | -0.028 | [-0.046, -0.010] | yes |
| pooled | H+E | D+F | 0.219 | -0.280 | [-0.342, -0.202] | yes |
| pooled | H+D | E+F | 0.255 | -0.244 | [-0.301, -0.180] | yes |
| pooled | H+F | E+D | 0.484 | -0.015 | [-0.031, 0.002] | no |
| pooled | H+E+D | F | 0.269 | -0.230 | [-0.285, -0.170] | yes |
| pooled | H+E+F | D | 0.484 | -0.015 | [-0.028, -0.000] | yes |
| pooled | H+D+F | E | 0.500 | 0.001 | [-0.001, 0.002] | no |
| pooled | E+D+F | H | 0.492 | -0.007 | [-0.018, 0.003] | no |
| pooled | H+E+D+F | nothing | 0.499 | 0.000 | [0.000, 0.000] | no |

## Figures

- `fig_cv_model_comparison.png`
- `fig_ablation.png`
