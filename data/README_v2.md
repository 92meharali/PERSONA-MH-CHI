# Relaxed-prompt corpus (v2)

Merged from `persona_mh_outputs_v2/` and `humt_results_v2/`, with five-rater human annotations.

## Condition

`relaxed_system_prompt_v2`: models were prompted as a professional therapist providing a single-turn online mental-health response. Unlike v1, the system prompt does not include the anti-anthropomorphism / no-lived-experience ban.

## Models

- `claude_opus_4_8`
- `glm`
- `gpt_5_6_sol`

## Counts

- CounselBench-Eval: 100 prompts × 3 = 300
- CounselBench-Adv: 120 prompts × 3 = 360
- Total responses: **660**
- Annotators: **5** × 660 = **3,300** ratings
- IDs: `PMH2-0001` … `PMH2-0660`

## Canonical files

| File | Role |
|---|---|
| `responses_v2.csv` | Master response + HuMT provenance |
| `ratings_long_v2.csv` | Five-rater human scores/reasons (no evidence spans) |
| `annotation_sheet_v2.csv` | Original blank blinded sheet template |
| `annotation_key_v2.csv` | Private model/HuMT key |
| `raw_annotations_v2/` | Per-annotator uploaded sheets (provenance) |
| `responses_v2_build_report.csv` | Response↔HuMT join diagnostics |

## Annotation notes

- Protocol: `persona_mh_human_v3_1` (rubric 3.1)
- Annotators: abrarahmed, emadsohail, meharali, nayabzahra, wahajaziz
- Shared evidence spans were identical across raters and are **excluded** from `ratings_long_v2.csv`
- Derived helpers in the uploads (`H_likert`, `S_score`, `S_persona`) are **not** stored as human ratings
- Uploaded sheets include model identity; treat blinding status cautiously for this round

## Quick score snapshot (raw rating means)

- OA ≈ 4.32
- E ≈ 3.74
- D ≈ 2.09
- F ≈ 4.36

Consensus median D counts: D1=163, D2=297, D3=190, D4=10 (no D5). Severe-to-moderate deception is substantially more present than in the v1 safety-conditioned corpus.
