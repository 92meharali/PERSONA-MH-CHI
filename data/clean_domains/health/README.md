# PERSONA Health Dataset

Health adapts PERSONA to casual health-assistance contexts. It tests whether AI responses remain appropriate when users ask for medical triage, treatment advice, clinician identity, uncertainty handling, and patient-facing explanations.

The current health files contain independent human annotations from the study's general-health rater pools.

## Files

| File | Rows | Description |
|---|---:|---|
| `oa_group_a.csv` | 2,075 | Group A holistic OA ratings |
| `anonymous_annotator_1.csv` | 415 | Group B E/D/F ratings |
| `anonymous_annotator_2.csv` | 415 | Group B E/D/F ratings |
| `anonymous_annotator_3.csv` | 415 | Group B E/D/F ratings |
| `anonymous_annotator_4.csv` | 415 | Group B E/D/F ratings |
| `anonymous_annotator_5.csv` | 415 | Group B E/D/F ratings |
| `humt_health.csv` | 450 | Combined HuMT export; 415 rows are used in the filtered release |
| `rubric.md` | - | PERSONA-Health annotation protocol |
| `analysis.md` | - | Domain analysis summary |

## Design

- 415 HuMT-complete responses.
- 5 Group A OA ratings per response.
- 5 Group B E/D/F ratings per response.
- Group A scored independent holistic `OA`.
- Group B scored `scenario_type`, `E`, `D`, and `F`.
- HuMT is stored separately and can be joined through response text with `humt_health.csv`.

## Columns

Group A score columns: `OA_score`.

Group B score columns: `E_score`, `D_score`, `F_score`.

Key metadata columns: `presentation_order`, `annotator_id`, `annotation_item_id`, `prompt`, `response`, `scenario_type`.
