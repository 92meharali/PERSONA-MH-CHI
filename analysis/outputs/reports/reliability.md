# Annotation reliability (Phase 2)

The primary reliability statistic is `ICC(A,k)`: a two-way mixed-effects, absolute-agreement, average-measures intraclass correlation. This matches the annotation structure because multiple raters in the relevant pool scored the same responses and the analysis uses their averaged score. Confidence intervals are 95 per cent percentile intervals from a response-level bootstrap.

`ICC(A,1)` is reported as the single-rater counterpart. Krippendorff's ordinal alpha is retained as a supplementary ordinal diagnostic, not as the primary inter-rater reliability statistic.

| Domain | Dimension | N | Raters | Primary ICC(A,k) | 95% CI | ICC(A,1) | 95% CI | Supplementary alpha | 95% CI | Interpretation |
|---|---|---:|---:|---:|---|---:|---|---:|---|---|
| mental_health | OA | 660 | 5 | 0.851 | [0.830, 0.870] | 0.534 | [0.493, 0.573] | 0.566 | [0.528, 0.601] | strong agreement |
| mental_health | E | 660 | 5 | 0.948 | [0.939, 0.956] | 0.786 | [0.755, 0.812] | 0.792 | [0.759, 0.820] | strong agreement |
| mental_health | D | 660 | 5 | 0.959 | [0.954, 0.965] | 0.826 | [0.805, 0.846] | 0.840 | [0.818, 0.859] | strong agreement |
| mental_health | F | 660 | 5 | 0.864 | [0.839, 0.885] | 0.559 | [0.511, 0.607] | 0.569 | [0.533, 0.602] | strong agreement |
| education | OA | 415 | 5 | 0.916 | [0.878, 0.938] | 0.687 | [0.590, 0.752] | 0.479 | [0.409, 0.537] | strong agreement |
| education | E | 415 | 5 | 0.997 | [0.995, 0.999] | 0.985 | [0.976, 0.993] | 0.988 | [0.976, 0.996] | strong agreement |
| education | D | 415 | 5 | 0.963 | [0.934, 0.981] | 0.840 | [0.739, 0.910] | 0.843 | [0.777, 0.905] | strong agreement |
| education | F | 415 | 5 | 0.954 | [0.928, 0.969] | 0.806 | [0.721, 0.864] | 0.648 | [0.558, 0.717] | strong agreement |
| health | OA | 415 | 5 | 0.907 | [0.804, 0.945] | 0.662 | [0.451, 0.774] | 0.339 | [0.212, 0.457] | strong agreement |
| health | E | 415 | 5 | 0.939 | [0.928, 0.948] | 0.754 | [0.719, 0.785] | 0.667 | [0.612, 0.716] | strong agreement |
| health | D | 415 | 5 | 0.942 | [0.912, 0.959] | 0.765 | [0.675, 0.822] | 0.446 | [0.343, 0.531] | strong agreement |
| health | F | 415 | 5 | 0.922 | [0.908, 0.934] | 0.702 | [0.663, 0.738] | 0.702 | [0.661, 0.739] | strong agreement |

## Scenario-level reliability

Reported for scenario types with at least 20 responses. ICC(A,k) remains the primary statistic; alpha is supplementary.

| Domain | Scenario | Dimension | N | ICC(A,k) | 95% CI | alpha | 95% CI |
|---|---|---|---:|---:|---|---:|---|
| mental_health | boundary_authority | OA | 118 | 0.889 | [0.839, 0.919] | 0.636 | [0.543, 0.724] |
| mental_health | boundary_authority | E | 118 | 0.964 | [0.946, 0.975] | 0.854 | [0.789, 0.901] |
| mental_health | boundary_authority | D | 118 | 0.978 | [0.968, 0.985] | 0.900 | [0.855, 0.925] |
| mental_health | boundary_authority | F | 118 | 0.926 | [0.880, 0.951] | 0.692 | [0.608, 0.762] |
| mental_health | crisis_risk | OA | 110 | 0.860 | [0.794, 0.903] | 0.585 | [0.467, 0.683] |
| mental_health | crisis_risk | E | 110 | 0.960 | [0.929, 0.977] | 0.818 | [0.729, 0.884] |
| mental_health | crisis_risk | D | 110 | 0.956 | [0.933, 0.971] | 0.850 | [0.775, 0.900] |
| mental_health | crisis_risk | F | 110 | 0.918 | [0.875, 0.953] | 0.728 | [0.629, 0.810] |
| mental_health | general_distress | OA | 378 | 0.838 | [0.809, 0.867] | 0.553 | [0.498, 0.609] |
| mental_health | general_distress | E | 378 | 0.889 | [0.845, 0.918] | 0.585 | [0.503, 0.666] |
| mental_health | general_distress | D | 378 | 0.947 | [0.934, 0.958] | 0.808 | [0.765, 0.840] |
| mental_health | general_distress | F | 378 | 0.826 | [0.795, 0.858] | 0.523 | [0.475, 0.576] |
| mental_health | psychoeducation | OA | 168 | 0.791 | [0.714, 0.840] | 0.454 | [0.347, 0.536] |
| mental_health | psychoeducation | E | 168 | 0.965 | [0.952, 0.974] | 0.865 | [0.819, 0.899] |
| mental_health | psychoeducation | D | 168 | 0.949 | [0.929, 0.961] | 0.777 | [0.718, 0.820] |
| mental_health | psychoeducation | F | 168 | 0.791 | [0.710, 0.846] | 0.483 | [0.386, 0.575] |
| education | other | OA | 72 | 0.770 | [0.667, 0.834] | 0.386 | [0.261, 0.493] |
| education | other | E | 72 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| education | other | D | 72 | 0.829 | [0.726, 0.896] | 0.511 | [0.338, 0.662] |
| education | other | F | 72 | nan | [nan, nan] | nan | [nan, nan] |
| education | relationship_boundary | OA | 31 | 0.980 | [0.945, 0.994] | 0.827 | [0.654, 0.941] |
| education | relationship_boundary | E | 31 | 0.992 | [0.981, 0.998] | 0.955 | [0.882, 0.992] |
| education | relationship_boundary | D | 31 | 0.982 | [0.948, 0.997] | 0.889 | [0.716, 0.979] |
| education | relationship_boundary | F | 31 | 0.991 | [0.932, 1.000] | 0.923 | [0.732, 1.000] |
| education | worked_example | OA | 268 | 0.663 | [0.585, 0.728] | 0.228 | [0.154, 0.304] |
| education | worked_example | E | 268 | 0.997 | [0.995, 0.999] | 0.982 | [0.966, 0.997] |
| education | worked_example | D | 268 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| education | worked_example | F | 268 | 0.734 | [0.606, 0.810] | 0.344 | [0.213, 0.454] |
| health | clinician_communication | OA | 66 | -0.470 | [-0.697, -0.234] | -0.068 | [-0.093, -0.041] |
| health | clinician_communication | E | 66 | -0.152 | [-0.613, 0.158] | -0.023 | [-0.082, 0.032] |
| health | clinician_communication | D | 66 | -0.291 | [-0.786, 0.040] | -0.044 | [-0.093, 0.010] |
| health | clinician_communication | F | 66 | -0.079 | [-0.412, 0.146] | -0.015 | [-0.069, 0.029] |
| health | emergency_risk | OA | 48 | 0.950 | [0.638, 0.975] | 0.547 | [0.206, 0.753] |
| health | emergency_risk | E | 48 | 0.935 | [0.908, 0.951] | 0.760 | [0.645, 0.808] |
| health | emergency_risk | D | 48 | 0.963 | [0.940, 0.974] | 0.770 | [0.620, 0.848] |
| health | emergency_risk | F | 48 | 0.928 | [0.004, 0.966] | 0.455 | [0.003, 0.703] |
| health | general_health_info | OA | 67 | -0.071 | [-0.397, 0.212] | -0.013 | [-0.060, 0.046] |
| health | general_health_info | E | 67 | 0.873 | [0.742, 0.919] | 0.480 | [0.267, 0.649] |
| health | general_health_info | D | 67 | 0.583 | [-0.158, 0.772] | 0.194 | [-0.027, 0.381] |
| health | general_health_info | F | 67 | -0.309 | [-0.934, 0.061] | -0.050 | [-0.110, 0.009] |
| health | medication_treatment | OA | 75 | 0.774 | [0.568, 0.850] | 0.402 | [0.180, 0.549] |
| health | medication_treatment | E | 75 | 0.919 | [0.876, 0.939] | 0.621 | [0.473, 0.734] |
| health | medication_treatment | D | 75 | 0.898 | [0.233, 0.952] | 0.357 | [0.049, 0.591] |
| health | medication_treatment | F | 75 | 0.904 | [0.843, 0.934] | 0.668 | [0.519, 0.764] |
| health | other | OA | 34 | 0.984 | [0.936, 0.992] | 0.760 | [0.388, 0.888] |
| health | other | E | 34 | 0.933 | [0.887, 0.949] | 0.739 | [0.528, 0.811] |
| health | other | D | 34 | 0.985 | [0.968, 0.991] | 0.798 | [0.579, 0.903] |
| health | other | F | 34 | 0.957 | [0.921, 0.974] | 0.728 | [0.516, 0.854] |
| health | triage_referral | OA | 104 | 0.060 | [-0.462, 0.380] | 0.013 | [-0.066, 0.107] |
| health | triage_referral | E | 104 | 0.927 | [0.899, 0.943] | 0.643 | [0.521, 0.735] |
| health | triage_referral | D | 104 | 0.715 | [0.364, 0.804] | 0.285 | [0.100, 0.405] |
| health | triage_referral | F | 104 | 0.808 | [0.700, 0.859] | 0.445 | [0.297, 0.546] |
| health | uncertainty_hedging | OA | 21 | 0.071 | [-0.362, 0.474] | 0.015 | [-0.061, 0.129] |
| health | uncertainty_hedging | E | 21 | 0.924 | [0.554, 0.955] | 0.565 | [0.171, 0.751] |
| health | uncertainty_hedging | D | 21 | 0.103 | [-0.394, 0.368] | 0.020 | [-0.072, 0.099] |
| health | uncertainty_hedging | F | 21 | 0.961 | [0.817, 0.977] | 0.730 | [0.265, 0.867] |

## Method check

- `OA` reliability is estimated from the Group A OA pool.
- `E`, `D`, and `F` reliability are estimated from the Group B dimension pool.
- The ICC formula is absolute-agreement average-measures ICC, so systematic rater level differences count against reliability rather than being ignored.
- The number of raters is read from each domain x dimension matrix after filtering to rows where that score is present.
