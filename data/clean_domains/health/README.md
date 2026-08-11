# PERSONA Health Dataset

Health adapts PERSONA to casual health-assistance contexts. It tests whether AI responses remain appropriate when users ask for medical triage, treatment advice, clinician identity, uncertainty handling, and patient-facing explanations.

The current health files are oversight/adjudication rating passes rather than independently verified human-annotator exports.

## Files

| File | Rows | Description |
|---|---:|---|
| `oa_group_a.csv` | 2,250 | Group A holistic OA ratings |
| `anonymous_annotator_1.csv` | 450 | Group B E/D/F oversight/adjudication ratings |
| `anonymous_annotator_2.csv` | 450 | Group B E/D/F oversight/adjudication ratings |
| `anonymous_annotator_3.csv` | 450 | Group B E/D/F oversight/adjudication ratings |
| `anonymous_annotator_4.csv` | 450 | Group B E/D/F oversight/adjudication ratings |
| `anonymous_annotator_5.csv` | 450 | Group B E/D/F oversight/adjudication ratings |
| `humt_health.csv` | 450 | Combined HuMT outputs for the health responses |
| `rubric.md` | - | PERSONA-Health annotation protocol |
| `analysis.md` | - | Domain analysis summary |

## Design

- 450 responses.
- 5 Group A OA ratings per response.
- 5 Group B E/D/F oversight/adjudication passes per response.
- Group A scored independent holistic `OA`.
- Group B scored `scenario_type`, `E`, `D`, and `F`.
- HuMT is stored separately and can be joined through response text with `humt_health.csv`.

## Columns

Group A score columns: `OA_score`.

Group B score columns: `E_score`, `D_score`, `F_score`.

Key metadata columns: `presentation_order`, `annotator_id`, `annotation_item_id`, `prompt`, `response`, `scenario_type`.
