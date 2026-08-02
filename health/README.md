# PERSONA Health — annotation pack

## Give annotators these files

1. **`PERSONA_health_annotation_sheet.csv`** (same content as `data/annotation_sheet.csv`)
2. **`annotation_protocol.md`** — health-adapted PERSONA rubric

- **450 rows** = 150 prompts × 3 models
- Model identity is hidden
- Rows are shuffled (`presentation_order`)
- **All prompts and responses are in English**
- Fill: `OA_score`, `OA_reason`, `scenario_type`, `E_score`, `E_reason`, `D_score`, `D_reason`, `F_score`, `F_reason`, optional flags/notes
- Use health scenario labels and D/F/E anchors from `annotation_protocol.md` (not the mental-health protocol)

## Translation

Non-English / mixed items (French, Portuguese, Russian, Hinglish, etc.) were **translated to English**, not dropped.

- Original text kept in `data/responses.csv` (`prompt_original`, `response_original`)
- Translation audit: `data/translation_log.csv`
- HuMT scores remain from the **original** generated text

## Do not give annotators

- `data/annotation_key.csv` — reveals model + HuMT + translation flags
- `data/responses.csv` — full analysis table
- raw folders `outputs/` and `../health_humt/`

## Sheet columns

| Column | Use |
|---|---|
| `presentation_order` | Display order |
| `annotation_item_id` | Stable ID (`PHLT-####`) |
| `prompt` | User message (English) |
| `response` | Model reply to rate (English) |
| `OA_score` / `OA_reason` | Overall appropriateness 1–5 |
| `scenario_type` | Primary situation label |
| `E_score` / `E_reason` | Empathic appropriateness 1–5 |
| `D_score` / `D_reason` | Anthropomorphic deception risk 1–5 |
| `F_score` / `F_reason` | Contextual fit 1–5 |
| `review_flag` / `annotator_notes` | Optional |

## Scenario labels

See `annotation_protocol.md`:

- `emergency_risk`
- `triage_referral`
- `medication_treatment`
- `uncertainty_hedging`
- `general_health_info`
- `clinician_communication`
- `other`
