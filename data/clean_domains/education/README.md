# PERSONA Education Dataset

Education adapts PERSONA to tutoring and teaching-assistant contexts. It tests whether appropriateness depends on pedagogical fit, academic boundaries, calibrated encouragement, and avoidance of false tutor identity or emotional dependency.

## Files

| File | Rows | Description |
|---|---:|---|
| `abrarahmed.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `emadsohail.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `meharali.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `nayabzahra.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `wahajaziz.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `humt_education.csv` | 450 | Combined HuMT outputs for the education responses |
| `rubric.md` | - | PERSONA-Education annotation protocol |
| `analysis.md` | - | Domain analysis summary |

## Design

- 450 responses.
- 5 annotators per response.
- Phase 1 scored independent `OA`.
- Phase 2 scored `scenario_type`, `E`, `D`, and `F`.
- HuMT is stored separately and can be joined through response text with `humt_education.csv`.

## Columns

Core score columns: `OA_score`, `E_score`, `D_score`, `F_score`.

Key metadata columns: `presentation_order`, `annotator_id`, `annotation_item_id`, `prompt`, `response`, `scenario_type`.
