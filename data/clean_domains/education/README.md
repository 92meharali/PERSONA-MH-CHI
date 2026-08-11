# PERSONA Education Dataset

Education adapts PERSONA to tutoring and teaching-assistant contexts. It tests whether appropriateness depends on pedagogical fit, academic boundaries, calibrated encouragement, and avoidance of false tutor identity or emotional dependency.

## Files

| File | Rows | Description |
|---|---:|---|
| `oa_group_a.csv` | 2,250 | Group A holistic OA ratings |
| `anonymous_annotator_1.csv` | 450 | Group B E/D/F ratings |
| `anonymous_annotator_2.csv` | 450 | Group B E/D/F ratings |
| `anonymous_annotator_3.csv` | 450 | Group B E/D/F ratings |
| `anonymous_annotator_4.csv` | 450 | Group B E/D/F ratings |
| `anonymous_annotator_5.csv` | 450 | Group B E/D/F ratings |
| `humt_education.csv` | 450 | Combined HuMT outputs for the education responses |
| `rubric.md` | - | PERSONA-Education annotation protocol |
| `analysis.md` | - | Domain analysis summary |

## Design

- 450 responses.
- 5 Group A OA ratings per response.
- 5 Group B E/D/F ratings per response.
- Group A scored independent holistic `OA`.
- Group B scored `scenario_type`, `E`, `D`, and `F`.
- HuMT is stored separately and can be joined through response text with `humt_education.csv`.

## Columns

Group A score columns: `OA_score`.

Group B score columns: `E_score`, `D_score`, `F_score`.

Key metadata columns: `presentation_order`, `annotator_id`, `annotation_item_id`, `prompt`, `response`, `scenario_type`.
