# D scope audit

This is a post-analysis qualitative inspection of health responses with consensus `D >= 3`.
It does not alter the original human ratings or create a new D subtype measure.

## Cue-family counts

- Affective or relational: 22
- Clinician identity and continuity: 1

## Sensitivity

| Analysis set | N | Clusters | Pearson | Spearman | D-only CV R2 | SD |
|---|---:|---:|---:|---:|---:|---:|
| all_health | 415 | 140 | -0.535 | -0.074 | 0.241 | 0.030 |
| minus_clinician_identity_response | 414 | 140 | -0.502 | -0.065 | 0.208 | 0.026 |
| minus_clinician_identity_prompt_cluster | 412 | 139 | -0.507 | -0.068 | 0.192 | 0.050 |
| minus_other_scenarios | 381 | 129 | -0.318 | -0.062 | 0.022 | 0.035 |

The professional-role sensitivity removes the sole high-D response whose dominant mechanism was an enacted clinician identity and false continuity. The `other` sensitivity shows that the health D-only result is concentrated in the relational adversarial subset.
