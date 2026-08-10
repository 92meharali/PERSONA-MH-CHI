# PERSONA Mental Health Dataset

Mental health is the primary PERSONA validation domain. It evaluates AI responses to online mental-health support prompts under a relaxed professional-therapist system prompt.

## Files

| File | Rows | Description |
|---|---:|---|
| `abrarahmed.csv` | 660 | Combined OA/E/D/F ratings with embedded HuMT and model metadata |
| `emadsohail.csv` | 660 | Combined OA/E/D/F ratings with embedded HuMT and model metadata |
| `meharali.csv` | 660 | Combined OA/E/D/F ratings with embedded HuMT and model metadata |
| `nayabzahra.csv` | 660 | Combined OA/E/D/F ratings with embedded HuMT and model metadata |
| `wahajaziz.csv` | 660 | Combined OA/E/D/F ratings with embedded HuMT and model metadata |
| `rubric.md` | - | PERSONA-MH annotation protocol v3.1 |
| `analysis.md` | - | Domain analysis summary |

## Design

- 220 prompts x 3 models = 660 responses.
- 5 blinded annotators per response.
- Models: Claude Opus 4.8, GLM, GPT-5.6-Sol.
- HuMT is embedded as `humt_score` and `humt_std`.
- `OA` is independent from `E/D/F`; it is not computed from the profile.

## Columns

Core score columns: `OA_score`, `E_score`, `D_score`, `F_score`, `humt_score`.

Key metadata columns: `annotation_item_id`, `annotator_id`, `model`, `prompt_id`, `source_set`, `topic`, `failure_mode`, `scenario_type`, `prompt`, `response`.
