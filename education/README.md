# PERSONA Education — annotation pack

## Give annotators

1. **`PERSONA_education_phase1_OA.csv`** — Phase 1 (OA only)
2. **`PERSONA_education_phase2_EDF.csv`** — Phase 2 (scenario + E/D/F)
3. **`annotation_protocol.md`** — education-adapted PERSONA rubric

Do **Phase 1 first**, lock OA, then Phase 2.

## Contents

- 450 rows = 150 prompts × 3 models (Claude Opus 4.8, GLM 5.2, GPT-5.6-Sol)
- Long format (one response per row), same as MH/health
- Shared `presentation_order` + `annotation_item_id` across both phases
- Prompts/responses already English in source sheet (no translation needed)
- Score cells empty and ready to fill

## Study-team only (not for annotators)

| File | Purpose |
|---|---|
| `data/annotation_key.csv` | model + HuMT + join notes |
| `data/responses.csv` | full analysis table |
| `data/translation_log.csv` | empty/minimal (no translations required) |
| `../education_humt/` | source HuMT files on GitHub |

## Notes

- HuMT matched for **350/450** responses.
- **Missing on GitHub:** natural GLM HuMT file (`education_humt/glm_5_2_text_humt.csv` not present) → 100 natural GLM HuMT cells blank in the key.
- Source wide sheet: teammate `combined_annotation_sheet_edu.xlsx`
- Raw generation clutter remains in `outputs/`
