# PERSONA education & health prompt packs

**Status: approved / final**

## Files for your teammate

| File | Rows | Contents |
|---|---|---|
| `persona_education_prompts.csv` | 150 | 100 natural (Bridge 50 + MathDial 50) + 50 adversarial |
| `persona_health_prompts.csv` | 150 | 100 natural (HealthBench) + 50 adversarial |

## Columns

`prompt_id, domain, prompt_type, source, source_id, topic, failure_mode, prompt, system_prompt`

- `prompt_type`: `natural` or `adversarial`
- `failure_mode`: blank for natural; filled for adversarial
- `system_prompt`: one simple fixed prompt per domain (no strict/relaxed)

## System prompts (already in CSV)

- **Education:** tutor, single-turn help
- **Health:** health assistant, single-turn help

## Recommended next steps (teammate)

1. Generate model responses for every prompt (same model set as mental-health study if possible)
2. Compute HuMT on responses
3. Human-annotate E / D / F / OA with domain-adapted anchors
4. Run PERSONA analysis

## Draft / review artifacts

Kept for provenance:

- `DRAFT_*.csv`, `_draft_*`, `REVIEW_adversarial_*.md`
- Adversarial text was approved as-is.
