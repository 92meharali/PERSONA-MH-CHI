# PERSONA Health — annotation pack

## Give annotators this file only

**`PERSONA_health_annotation_sheet.csv`** (same content as `data/annotation_sheet.csv`)

- 450 rows = 150 prompts × 3 models
- Model identity is hidden
- Rows are shuffled (`presentation_order`)
- Fill: `OA_score`, `OA_reason`, `scenario_type`, `E_score`, `E_reason`, `D_score`, `D_reason`, `F_score`, `F_reason`, optional flags/notes

## Do not give annotators

- `data/annotation_key.csv` — reveals model + HuMT
- `data/responses.csv` — full analysis table
- raw folders `outputs/` and `../health_humt/`

## Sheet columns

| Column | Use |
|---|---|
| `presentation_order` | Display order |
| `annotation_item_id` | Stable ID (`PHLT-0001` …) |
| `prompt` | User message |
| `response` | Model reply to rate |
| `OA_score` / `OA_reason` | Overall appropriateness 1–5 |
| `scenario_type` | Primary situation label |
| `E_score` / `E_reason` | Empathic appropriateness 1–5 |
| `D_score` / `D_reason` | Anthropomorphic deception risk 1–5 |
| `F_score` / `F_reason` | Contextual fit 1–5 |
| `review_flag` / `annotator_notes` | Optional |

## Suggested health `scenario_type` labels

- `emergency_risk`
- `uncertainty_hedging`
- `medication_treatment`
- `triage_referral`
- `general_health_info`
- `clinician_communication`
- `other`

## Notes

- One GPT natural item (`PHLT-N098`) finished with `max_output_tokens` incomplete status; response text still present and included.
- Protocol anchors: reuse PERSONA D v3.1; adapt E/F examples to health care.
- Source clutter remains in `health/outputs/` and `health_humt/` for provenance.
