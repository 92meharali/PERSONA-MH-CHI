# PERSONA Education and Health Generation Notebooks

This package is intended to be extracted into the repository root. It creates:

- `education/` — eight generation notebooks and `education/outputs/`
- `health/` — eight generation notebooks and `health/outputs/`

Each notebook contains exactly **nine executable cells**:

1. Setup and paths
2. Load, validate, and filter the combined domain CSV
3. Model settings and row-level system prompt construction
4. Provider API helper
5. One-prompt test
6. Full checkpointed/resumable generation
7. Quality checks
8. Regeneration of failed, incomplete, or over-limit rows
9. E/D/F/OA annotation-sheet creation

## Input files

The notebooks expect these existing repository files:

- `prompt_packs/persona_education_prompts.csv`
- `prompt_packs/persona_health_prompts.csv`

Each notebook filters the combined CSV by `prompt_type`:

- `natural` → expected 100 rows
- `adversarial` → expected 50 rows

The `system_prompt` is read from the **current row** on every request. The notebook
appends the same response constraints used in the earlier pipeline:

- no more than 170 words
- 1–2 short paragraphs
- avoid bullets unless necessary

## Generation settings

- OpenRouter Claude and GLM: `temperature = 0.2`
- Gemini: `temperature = 0.2`
- OpenAI GPT-5.6 Sol: `reasoning.effort = "low"`; temperature is not set
- All notebooks: `MAX_OUTPUT_TOKENS = 500`

## Environment variables

Add these to the repository `.env`:

```env
OPENROUTER_API_KEY=put_your_openrouter_key_here
OPENROUTER_MODEL_SLUG=z-ai/glm-5.2
OPENROUTER_CLAUDE_MODEL_SLUG=anthropic/claude-opus-4.8

GEMINI_API_KEY=put_your_gemini_key_here
GEMINI_MODEL=gemini-3.5-flash

OPENAI_API_KEY=put_your_openai_api_key_here
OPENAI_MODEL=gpt-5.6-sol
```

## Output naming

Files are written inside the relevant domain:

- `<condition>_<model>_responses_clean_v1.csv`
- `<condition>_<model>_annotation_sheet_clean_v1.csv`

Existing valid responses are retained, duplicate prompt IDs are removed, and
generation resumes only for unfinished prompts.
