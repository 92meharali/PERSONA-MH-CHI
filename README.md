# PERSONA-MH

PERSONA-MH evaluates whether human-like behavior is appropriate in mental-health AI responses.

## Measures

- **H / HuMT:** automated human-likeness (raw HuMT; also remapped to a 1–5 Likert value `H` for scoring)
- **E:** empathic appropriateness
- **D:** anthropomorphic deception risk (v3.1)
- **F:** contextual fit
- **OA:** independent overall appropriateness
- **P = (H, E, D, F):** multidimensional profile
- **S = (H + E − D + F) / 4:** secondary equal-weight ranking score (not a replacement for OA)

## Final dataset

- 220 prompts × 3 models = 660 responses
- 5 annotators per response
- OA was completed and locked before E/D/F
- E uses a second blind annotation round with the unchanged rubric
- Evidence spans are excluded from analysis
- D uses the frozen v3.1 highest-severity, AI-attributable-cue rule

Canonical files are in `data/`:

- `responses.csv`
- `ratings_long.csv`
- `annotation_protocol.md`

Raw prompts, generated responses, and HuMT values remain in their source directories.

## Focused analysis

Confirmatory hypotheses:

1. HuMT is not a reliable proxy for OA
2. E/D/F add information beyond HuMT
3. Joint model directions: E↑/F↑ with OA, D↓ with OA
4. Models differ in OA/E/F profiles

Also reported: reliability, correlations, context/dataset associations (exploratory), and the full **S** validity / ablation / sensitivity / model-ranking block.

Run:

```bash
pip install -r analysis/requirements.txt
python -m analysis --corpus v1
python -m analysis --corpus v2
python -m analysis --corpus both --compare
```

Outputs:

- v1 → `analysis_outputs/`
- v2 (relaxed prompt) → `analysis_outputs_v2/`
- v1 vs v2 comparison → `analysis_outputs_compare/`

See `RESEARCH_SUMMARY.md` for the concise study overview.
