# PERSONA

PERSONA evaluates when anthropomorphic AI behavior is appropriate in high-stakes human-support settings.

Mental health counseling is the current primary instantiation. The framework is designed to extend to education and health care with the same core dimensions.

## Measures

- **H / HuMT:** automated human-likeness (also remapped to 1–5 as `H` for scoring)
- **E:** empathic appropriateness
- **D:** anthropomorphic deception risk (v3.1)
- **F:** contextual fit
- **OA:** independent overall appropriateness
- **P = (H, E, D, F):** multidimensional profile
- **S = (H + E − D + F) / 4:** secondary ranking score (not a replacement for OA)

## Active corpus (relaxed system prompt)

- 220 CounselBench prompts × 3 models = 660 responses
- Models: Claude Opus 4.8, GLM, GPT-5.6-Sol (Gemini pending)
- 5 blinded annotators per response
- Protocol: `persona_mh_human_v3_1`
- Evidence spans excluded from analysis data

Canonical files are in `data/`:

- `responses.csv`
- `ratings_long.csv`
- `annotation_protocol.md`
- `CORPUS.md`

Raw generation/HuMT sources: `persona_mh_outputs/`, `humt_results/`, `counselbench_outputs/`.

Archived v1 materials live under `previous versions/`.

## Analysis

```bash
pip install -r analysis/requirements.txt
python -m analysis                 # primary relaxed-prompt corpus
python -m analysis --corpus v1     # archived pilot only
python -m analysis --compare       # optional archived v1 vs v2 contrast
```

Results are written to `analysis_outputs/`.

See `RESEARCH_SUMMARY.md` for the full study narrative and `DOMAIN_DATASETS.md` for education/health extension candidates.
