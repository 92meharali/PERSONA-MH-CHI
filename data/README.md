# Active PERSONA data

Primary corpus = **relaxed system prompt**.

## Canonical files

| File | Role |
|---|---|
| `responses.csv` | 660 responses + HuMT + provenance (`PMH2-*` ids) |
| `ratings_long.csv` | 3,300 human ratings (5 annotators × 660) |
| `annotation_protocol.md` | Frozen PERSONA rating protocol |
| `annotation_sheet.csv` | Blinded annotation template |
| `annotation_key.csv` | Private model/HuMT join key |
| `responses_build_report.csv` | Response↔HuMT join diagnostics |
| `raw_annotations/` | Per-annotator uploaded sheets |
| `CORPUS.md` | Corpus-specific notes |

## Condition

`relaxed_system_prompt_v2`: models prompted as a professional therapist for a single-turn response. No anti-anthropomorphism ban.

## Models

- `claude_opus_4_8`
- `glm`
- `gpt_5_6_sol`
- Gemini planned

## Annotation notes

- Protocol: `persona_mh_human_v3_1`
- Model identity hidden during rating; metadata joined afterward
- Evidence spans excluded from `ratings_long.csv`
- Derived helpers (`H_likert`, `S_*`) are not stored as human ratings

Archived strict-prompt pilot data is under `../previous versions/v1_original_prompt/`.
