# PERSONA Health — annotation pack

## Give annotators

1. **`PERSONA_health_phase1_OA.csv`** — Phase 1 (OA only)
2. **`PERSONA_health_phase2_EDF.csv`** — Phase 2 (scenario + E/D/F)
3. **`annotation_protocol.md`** — health-adapted PERSONA rubric

Do **Phase 1 first**, lock OA, then Phase 2.

## Contents

- 450 rows = 150 prompts × 3 models (Claude Opus 4.8, GLM 5.2, GPT-5.6-Sol)
- Long format (one response per row), same as MH
- Shared `presentation_order` + `annotation_item_id` across both phases
- Non-English prompts/responses translated to English
- Score cells empty and ready to fill

## Study-team only (not for annotators)

| File | Purpose |
|---|---|
| `data/annotation_key.csv` | model + HuMT + translation flags |
| `data/responses.csv` | full analysis table + originals |
| `data/translation_log.csv` | translation audit |
| `../health_humt/` | source HuMT files on GitHub |

## Notes

- HuMT matched for **446/450** responses. Four GPT items in the uploaded combined sheet differ slightly from the text HuMT was computed on (`PHLT-N012`, `N033`, `N098`, `N100`); those HuMT cells are blank in the key.
- Source wide sheet: teammate `combined_annotation_sheet_health.xlsx`
- Raw generation clutter remains in `outputs/`
