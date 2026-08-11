# Annotation reliability (Phase 2)

The primary reliability statistic is `ICC(A,k)`: a two-way mixed-effects, absolute-agreement, average-measures intraclass correlation. This matches the annotation structure because multiple raters in the relevant pool scored the same responses and the analysis uses their averaged score. Confidence intervals are 95 per cent percentile intervals from a response-level bootstrap.

`ICC(A,1)` is reported as the single-rater counterpart. Krippendorff's ordinal alpha is retained as a supplementary ordinal diagnostic, not as the primary inter-rater reliability statistic.

| Domain | Dimension | N | Raters | Primary ICC(A,k) | 95% CI | ICC(A,1) | 95% CI | Supplementary alpha | 95% CI | Interpretation |
|---|---|---:|---:|---:|---|---:|---|---:|---|---|
| mental_health | OA | 660 | 5 | 0.851 | [0.830, 0.870] | 0.534 | [0.493, 0.573] | 0.566 | [0.528, 0.601] | strong agreement |
| mental_health | E | 660 | 5 | 0.948 | [0.939, 0.956] | 0.786 | [0.755, 0.812] | 0.792 | [0.759, 0.820] | strong agreement |
| mental_health | D | 660 | 5 | 0.959 | [0.954, 0.965] | 0.826 | [0.805, 0.846] | 0.840 | [0.818, 0.859] | strong agreement |
| mental_health | F | 660 | 5 | 0.864 | [0.839, 0.885] | 0.559 | [0.511, 0.607] | 0.569 | [0.533, 0.602] | strong agreement |
| education | OA | 450 | 5 | 0.919 | [0.886, 0.938] | 0.695 | [0.610, 0.752] | 0.477 | [0.412, 0.532] | strong agreement |
| education | E | 450 | 5 | 0.997 | [0.995, 0.998] | 0.983 | [0.974, 0.992] | 0.984 | [0.972, 0.995] | strong agreement |
| education | D | 450 | 5 | 0.964 | [0.934, 0.981] | 0.841 | [0.740, 0.910] | 0.845 | [0.780, 0.901] | strong agreement |
| education | F | 450 | 5 | 0.954 | [0.929, 0.968] | 0.805 | [0.723, 0.858] | 0.638 | [0.554, 0.708] | strong agreement |
| health | OA | 450 | 5 | 0.900 | [0.793, 0.938] | 0.644 | [0.434, 0.753] | 0.328 | [0.209, 0.436] | strong agreement |
| health | E | 450 | 5 | 0.937 | [0.926, 0.947] | 0.750 | [0.715, 0.781] | 0.659 | [0.608, 0.708] | strong agreement |
| health | D | 450 | 5 | 0.935 | [0.902, 0.954] | 0.743 | [0.647, 0.805] | 0.410 | [0.319, 0.504] | strong agreement |
| health | F | 450 | 5 | 0.918 | [0.904, 0.930] | 0.692 | [0.654, 0.726] | 0.692 | [0.653, 0.728] | strong agreement |

## Scenario-level reliability

Reported for scenario types with at least 20 responses. ICC(A,k) remains the primary statistic; alpha is supplementary.

| Domain | Scenario | Dimension | N | ICC(A,k) | 95% CI | alpha | 95% CI |
|---|---|---|---:|---:|---|---:|---|
| mental_health | boundary_authority | OA | 118 | 0.889 | [0.842, 0.921] | 0.636 | [0.543, 0.713] |
| mental_health | boundary_authority | E | 118 | 0.964 | [0.948, 0.977] | 0.854 | [0.791, 0.908] |
| mental_health | boundary_authority | D | 118 | 0.978 | [0.969, 0.984] | 0.900 | [0.863, 0.925] |
| mental_health | boundary_authority | F | 118 | 0.926 | [0.879, 0.951] | 0.692 | [0.609, 0.758] |
| mental_health | crisis_risk | OA | 110 | 0.860 | [0.787, 0.905] | 0.585 | [0.469, 0.689] |
| mental_health | crisis_risk | E | 110 | 0.960 | [0.929, 0.978] | 0.818 | [0.712, 0.888] |
| mental_health | crisis_risk | D | 110 | 0.956 | [0.940, 0.973] | 0.850 | [0.779, 0.902] |
| mental_health | crisis_risk | F | 110 | 0.918 | [0.875, 0.951] | 0.728 | [0.639, 0.828] |
| mental_health | general_distress | OA | 378 | 0.838 | [0.798, 0.868] | 0.553 | [0.489, 0.608] |
| mental_health | general_distress | E | 378 | 0.889 | [0.843, 0.919] | 0.585 | [0.486, 0.663] |
| mental_health | general_distress | D | 378 | 0.947 | [0.936, 0.957] | 0.808 | [0.772, 0.838] |
| mental_health | general_distress | F | 378 | 0.826 | [0.784, 0.855] | 0.523 | [0.471, 0.573] |
| mental_health | psychoeducation | OA | 168 | 0.791 | [0.697, 0.835] | 0.454 | [0.360, 0.532] |
| mental_health | psychoeducation | E | 168 | 0.965 | [0.953, 0.975] | 0.865 | [0.818, 0.898] |
| mental_health | psychoeducation | D | 168 | 0.949 | [0.932, 0.961] | 0.777 | [0.725, 0.822] |
| mental_health | psychoeducation | F | 168 | 0.791 | [0.704, 0.852] | 0.483 | [0.381, 0.574] |
| education | other | OA | 72 | 0.770 | [0.693, 0.835] | 0.386 | [0.289, 0.494] |
| education | other | E | 72 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| education | other | D | 72 | 0.829 | [0.705, 0.895] | 0.511 | [0.306, 0.649] |
| education | other | F | 72 | nan | [nan, nan] | nan | [nan, nan] |
| education | relationship_boundary | OA | 31 | 0.980 | [0.922, 0.994] | 0.827 | [0.644, 0.941] |
| education | relationship_boundary | E | 31 | 0.992 | [0.982, 0.998] | 0.955 | [0.878, 0.992] |
| education | relationship_boundary | D | 31 | 0.982 | [0.949, 0.996] | 0.889 | [0.730, 0.976] |
| education | relationship_boundary | F | 31 | 0.991 | [0.945, 1.000] | 0.923 | [0.744, 1.000] |
| education | worked_example | OA | 300 | 0.658 | [0.593, 0.713] | 0.223 | [0.158, 0.288] |
| education | worked_example | E | 300 | 0.996 | [0.993, 0.999] | 0.977 | [0.959, 0.994] |
| education | worked_example | D | 300 | 1.000 | [1.000, 1.000] | 1.000 | [1.000, 1.000] |
| education | worked_example | F | 300 | 0.723 | [0.627, 0.796] | 0.330 | [0.231, 0.434] |
| health | clinician_communication | OA | 78 | -0.378 | [-0.673, -0.040] | -0.059 | [-0.093, -0.009] |
| health | clinician_communication | E | 78 | -0.037 | [-0.436, 0.227] | -0.005 | [-0.072, 0.054] |
| health | clinician_communication | D | 78 | -0.311 | [-0.704, 0.022] | -0.048 | [-0.091, -0.000] |
| health | clinician_communication | F | 78 | -0.182 | [-0.481, 0.060] | -0.032 | [-0.072, 0.011] |
| health | emergency_risk | OA | 51 | 0.947 | [0.709, 0.972] | 0.532 | [0.274, 0.730] |
| health | emergency_risk | E | 51 | 0.934 | [0.910, 0.952] | 0.756 | [0.676, 0.811] |
| health | emergency_risk | D | 51 | 0.960 | [0.941, 0.972] | 0.745 | [0.589, 0.836] |
| health | emergency_risk | F | 51 | 0.940 | [0.763, 0.968] | 0.512 | [0.188, 0.714] |
| health | general_health_info | OA | 72 | -0.106 | [-0.457, 0.166] | -0.019 | [-0.065, 0.035] |
| health | general_health_info | E | 72 | 0.867 | [0.754, 0.916] | 0.466 | [0.266, 0.615] |
| health | general_health_info | D | 72 | 0.542 | [-0.026, 0.757] | 0.170 | [-0.008, 0.361] |
| health | general_health_info | F | 72 | -0.152 | [-0.716, 0.193] | -0.027 | [-0.096, 0.045] |
| health | medication_treatment | OA | 84 | 0.785 | [0.666, 0.871] | 0.420 | [0.261, 0.594] |
| health | medication_treatment | E | 84 | 0.913 | [0.880, 0.935] | 0.594 | [0.472, 0.700] |
| health | medication_treatment | D | 84 | 0.878 | [0.632, 0.943] | 0.311 | [0.054, 0.523] |
| health | medication_treatment | F | 84 | 0.889 | [0.844, 0.916] | 0.625 | [0.522, 0.698] |
| health | other | OA | 34 | 0.984 | [0.942, 0.994] | 0.760 | [0.442, 0.910] |
| health | other | E | 34 | 0.933 | [0.898, 0.950] | 0.739 | [0.563, 0.803] |
| health | other | D | 34 | 0.985 | [0.965, 0.991] | 0.798 | [0.536, 0.901] |
| health | other | F | 34 | 0.957 | [0.906, 0.977] | 0.728 | [0.443, 0.881] |
| health | triage_referral | OA | 110 | 0.079 | [-0.376, 0.333] | 0.018 | [-0.063, 0.089] |
| health | triage_referral | E | 110 | 0.924 | [0.895, 0.941] | 0.641 | [0.535, 0.719] |
| health | triage_referral | D | 110 | 0.683 | [0.283, 0.795] | 0.250 | [0.064, 0.407] |
| health | triage_referral | F | 110 | 0.791 | [0.688, 0.846] | 0.416 | [0.286, 0.516] |
| health | uncertainty_hedging | OA | 21 | 0.071 | [-0.456, 0.461] | 0.015 | [-0.083, 0.126] |
| health | uncertainty_hedging | E | 21 | 0.924 | [0.580, 0.956] | 0.565 | [0.190, 0.767] |
| health | uncertainty_hedging | D | 21 | 0.103 | [-0.313, 0.352] | 0.020 | [-0.063, 0.095] |
| health | uncertainty_hedging | F | 21 | 0.961 | [0.883, 0.980] | 0.730 | [0.321, 0.885] |

## Method check

- `OA` reliability is estimated from the Group A OA pool.
- `E`, `D`, and `F` reliability are estimated from the Group B dimension pool.
- The ICC formula is absolute-agreement average-measures ICC, so systematic rater level differences count against reliability rather than being ignored.
- The number of raters is read from each domain x dimension matrix after filtering to rows where that score is present.
