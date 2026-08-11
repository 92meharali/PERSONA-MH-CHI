# PERSONA Mental Health Dataset

Mental health is the primary PERSONA validation domain. It evaluates AI responses to online mental-health support prompts under a relaxed professional-therapist system prompt.

## Files

| File | Rows | Description |
|---|---:|---|
| `oa_group_a.csv` | 3,300 | Group A holistic OA ratings |
| `anonymous_annotator_1.csv` | 660 | Group B E/D/F ratings with embedded HuMT and model metadata |
| `anonymous_annotator_2.csv` | 660 | Group B E/D/F ratings with embedded HuMT and model metadata |
| `anonymous_annotator_3.csv` | 660 | Group B E/D/F ratings with embedded HuMT and model metadata |
| `anonymous_annotator_4.csv` | 660 | Group B E/D/F ratings with embedded HuMT and model metadata |
| `anonymous_annotator_5.csv` | 660 | Group B E/D/F ratings with embedded HuMT and model metadata |
| `rubric.md` | - | PERSONA-MH annotation protocol v3.1 |
| `analysis.md` | - | Domain analysis summary |

## Design

- 220 prompts x 3 models = 660 responses.
- 5 Group A OA ratings per response.
- 5 Group B E/D/F ratings per response.
- Models: Claude Opus 4.8, GLM, GPT-5.6-Sol.
- HuMT is embedded as `humt_score` and `humt_std`.
- `OA` is rated by Group A and is independent from Group B `E/D/F`; it is not
  computed from the profile.

## Columns

Group A score columns: `OA_score`.

Group B score columns: `E_score`, `D_score`, `F_score`, `humt_score`.

Key metadata columns: `annotation_item_id`, `annotator_id`, `model`, `prompt_id`, `source_set`, `topic`, `failure_mode`, `scenario_type`, `prompt`, `response`.
