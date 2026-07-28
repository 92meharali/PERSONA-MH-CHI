# PERSONA-MH

PERSONA-MH evaluates whether human-like behavior is appropriate in mental-health AI responses.

## Measures

- **H / HuMT:** automated human-likeness
- **E:** empathic appropriateness
- **D:** anthropomorphic deception risk (v3.1)
- **F:** contextual fit
- **OA:** independent overall appropriateness

## Final dataset

- 220 prompts × 3 models = 660 responses
- 5 annotators per response
- OA was completed and locked before E/D/F
- D uses the frozen v3.1 highest-severity, AI-attributable-cue rule

Canonical files are in `data/`:

- `responses.csv`
- `ratings_long.csv`
- `annotation_protocol.md`

Raw prompts, generated responses, and HuMT values remain in their source directories.

## Focused analysis

The analysis covers only the research questions required for the paper:

1. annotation reliability;
2. paired model comparisons;
3. HuMT versus OA;
4. incremental value of E/D/F beyond HuMT;
5. context moderation;
6. ADV versus EVAL dataset associations.

Run:

```bash
pip install -r analysis/requirements.txt
python -m analysis
```

All tables, figures, analysis data, and the generated report are written together to `analysis_outputs/`.

See `RESEARCH_SUMMARY.md` for the concise study overview.
