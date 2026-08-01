# Relaxed-prompt corpus (v2)

Merged from `persona_mh_outputs_v2/` and `humt_results_v2/`.

## Condition

`relaxed_system_prompt_v2`: models were prompted as a professional therapist
providing a single-turn online mental-health response. Unlike v1, the system
prompt does not include the anti-anthropomorphism / no-lived-experience ban.

## Files

- `responses_v2.csv`: 660 items (220 prompts × 3 models) with HuMT and provenance.
- `annotation_sheet_v2.csv`: blinded sheet for human annotation (prompt + response only).
- `annotation_key_v2.csv`: private join key back to model / HuMT / metadata.
- `responses_v2_build_report.csv`: per-file join diagnostics.

## Models

- `claude_opus_4_8`
- `glm`
- `gpt_5_6_sol`

## Counts

- CounselBench-Eval: 100 prompts × 3 = 300
- CounselBench-Adv: 120 prompts × 3 = 360
- Total: 660

IDs use the prefix `PMH2-####` so they do not collide with v1 `PMH-####`.
