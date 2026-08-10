# PERSONA Health Dataset

Health adapts PERSONA to casual health-assistance contexts. It tests whether AI responses remain appropriate when users ask for medical triage, treatment advice, clinician identity, uncertainty handling, and patient-facing explanations.

The current health files are oversight/adjudication rating passes rather than independently verified human-annotator exports.

## Files

| File | Rows | Description |
|---|---:|---|
| `abrar.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `emad.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `mehar.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `nayab.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `wahaj.csv` | 450 | Phase 1 OA and Phase 2 E/D/F merged by item |
| `humt_health.csv` | 450 | Combined HuMT outputs for the health responses |
| `rubric.md` | - | PERSONA-Health annotation protocol |
| `analysis.md` | - | Domain analysis summary |

## Design

- 450 responses.
- 5 oversight/adjudication passes per response.
- Phase 1 scored independent `OA`.
- Phase 2 scored `scenario_type`, `E`, `D`, and `F`.
- HuMT is stored separately and can be joined through response text with `humt_health.csv`.

## Columns

Core score columns: `OA_score`, `E_score`, `D_score`, `F_score`.

Key metadata columns: `presentation_order`, `annotator_id`, `annotation_item_id`, `prompt`, `response`, `scenario_type`.
