# PERSONA education & health prompt packs — draft status

## Decisions locked

| Item | Choice |
|---|---|
| Pack size | 100 natural + 50 adversarial per domain |
| Education natural sources | Bridge (50) + MathDial (50) |
| Health natural source | HealthBench OSS eval, single-turn only, stratified across 7 themes, non-clinician-preferring |
| System prompt | One simple fixed prompt per domain (no strict/relaxed) |
| Models / HuMT | Out of these CSVs — teammate generates later |
| Adversarial | Authored; pending your approval before final filenames |

## Files for review now

- `REVIEW_adversarial_education_50.md` — read/edit these first
- `REVIEW_adversarial_health_50.md`
- `DRAFT_persona_education_prompts.csv` — 150 rows (natural+adv), not final
- `DRAFT_persona_health_prompts.csv` — 150 rows (natural+adv), not final

## Final files (after you approve adversarial)

Will be written as:

- `persona_education_prompts.csv`
- `persona_health_prompts.csv`

## CSV columns

`prompt_id, domain, prompt_type, source, source_id, topic, failure_mode, prompt, system_prompt`

## Recommended generation setup for teammate (not in CSV)

- Same model set as mental-health study for comparability: Claude Opus, GLM, GPT (add Gemini if available)
- One system prompt column already included per row
- Then HuMT on responses; then human E/D/F/OA with domain-adapted anchors
