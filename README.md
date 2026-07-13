# PERSONA-MH-CHI

PERSONA is a research framework for evaluating when anthropomorphic behavior in AI systems is contextually appropriate. This repository implements the mental-health instantiation (**PERSONA-MH**).

## PERSONA dimensions

| Code | Name | Role |
|------|------|------|
| **H** | Human-likeness | Descriptive style signal (here: automated **HuMT**) |
| **E** | Empathic Appropriateness | Warmth / validation that is helpful |
| **D** | Deception Risk | Risk of encouraging anthropomorphic misunderstanding |
| **F** | Contextual Fit | Style/content match to the situation |
| **OA** | Overall Appropriateness | Holistic suitability (not a plain average of E/D/F) |
| **R** | Relational Expectation | Optional; not scored in the current pipeline |

Core idea from the Executive Summary: high empathy is not always better — PERSONA separates **E**, **D**, and **F**, with **H** (HuMT) carried as a separate descriptive measure.

---

## Repository structure

```text
PERSONA-MH-CHI/
├── Executive Summary.pdf          # Research plan / PERSONA framework write-up
├── README.md
├── .env.example
├── dataset_generation.py          # Build CounselBench prompt CSVs
├── compute_humt_sociot_colab.py   # HuMT (human-likeness) scoring
│
├── counselbench_outputs/          # Prompt datasets
│   ├── counselbench_eval_100_prompts.csv
│   └── counselbench_adv_120_prompts.csv
│
├── persona_mh_outputs/            # Model responses only (read-only inputs)
│   ├── eval_{glm,gemini,claude_opus_4_8}_responses_*.csv
│   └── adv_{glm,gemini,claude_opus_4_8}_responses_*.csv
│
├── humt_results/                  # HuMT scores aligned to responses
│
├── persona_annotation/            # Scaffold → score → CSV export pipeline
│
├── annotations_csv/               # Structured PERSONA outputs (per model)
│   ├── glm_persona_annotations.csv
│   ├── gemini_persona_annotations.csv
│   ├── claude_opus_4_8_persona_annotations.csv
│   └── all_models_persona_annotations.csv
│
├── *generation*.ipynb             # Response generation notebooks
└── presentations and drafts/      # Research plans / slides / rubric notes
```

Regenerable intermediates (`annotations/`, `annotations_scored/`) are gitignored; rebuild them with the CLI below if needed.

---

## Current data inventory

| Asset | Count | Notes |
|-------|------:|-------|
| CounselBench-Eval prompts | 100 | 20 topics × 5 |
| CounselBench-Adv prompts | 120 | 6 failure modes × 20 |
| Models | 3 | `glm`, `gemini`, `claude_opus_4_8` |
| Responses | 660 | 220 per model (100 eval + 120 adv) |
| HuMT scores | 660 | Joined by `response_text` |
| PERSONA CSV rows | 660 | E/D/F/OA + reasons + evidence |

Generation settings (shared across models): temperature `0.2`, fixed safety-oriented system prompt, target under ~170 words.

---

## Annotation CSV schema

Each per-model CSV flattens one response into:

```text
filename, index, prompt_id, model, source_id, source_set, topic, failure_mode,
response, humt_score,
Empathy_score, Empathy_reason, Empathy_evidence,
DeceptionRisk_score, DeceptionRisk_reason, DeceptionRisk_evidence,
ContextualFit_score, ContextualFit_reason, ContextualFit_evidence,
OverallAppropriateness_score, OverallAppropriateness_reason, OverallAppropriateness_evidence
```

Scores are 1–5. Evidence quotes are verbatim spans from the response. Automated scoring uses protocol `persona_rubric_v1_response_grounded` and is a **pilot**, not a substitute for expert clinician annotation described in the Executive Summary.

---

## Setup

```bash
git clone https://github.com/92meharali/PERSONA-MH-CHI.git
cd PERSONA-MH-CHI

conda create -n persona-mh python=3.10 -y
conda activate persona-mh

pip install -r persona_annotation/requirements.txt
pip install requests python-dotenv datasets notebook ipykernel
```

Create a local `.env` (never commit it):

```env
OPENROUTER_API_KEY=your_openrouter_key
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-3.1-pro-preview
```

---

## PERSONA statistical analysis

Publication-oriented analyses live in `analysis/` and write to:

```text
figures/   # matplotlib publication figures
tables/    # LaTeX tables
results/   # CSV + JSON intermediates
reports/   # analysis_report.md + run summary
```

```bash
pip install -r analysis/requirements.txt
python -m analysis
```

The pipeline covers data quality, (multi-rater) reliability when available, model comparison, correlations, nested regression / incremental validity over HuMT, ML feature importance (+ SHAP when available), calibration, sensitivity, ablation, adversarial dataset contrasts, clustering, latent structure, hypothesis battery, and an auto-generated report. Raw annotation/response CSVs are never modified.


### 1) Rebuild prompts (optional)

```bash
python dataset_generation.py
```

### 2) Generate / refresh model responses

Use the matching notebook, e.g. `persona_mh_generation.ipynb` (GLM eval), `persona_mh_adversarial_generation.ipynb`, Gemini/Claude variants.

### 3) Run PERSONA annotation tooling

```bash
# Blank JSON scaffolds (writes annotations/; gitignored)
python -m persona_annotation scaffold

# Fill E/D/F/OA with evidence quotes (writes annotations_scored/; gitignored)
python -m persona_annotation score

# Export per-model structured CSVs (writes annotations_csv/)
python -m persona_annotation export-csv --overwrite
```

Upstream CSVs under `counselbench_outputs/`, `persona_mh_outputs/`, and `humt_results/` are never modified by these commands.

---

## Research status (vs Executive Summary)

**Done in this repo**

- CounselBench-Eval + Adv prompts extracted
- Responses for GLM, Gemini, Claude Opus 4.8 (eval + adv)
- HuMT human-likeness scores
- PERSONA annotation scaffolding + automated pilot scores + per-model CSVs

**Still planned (paper protocol)**

1. Expert clinician annotation (multi-rater E/D/F/OA + IRR)
2. **Persona-ADV** prompts (identity / memory / attachment / promise / authority / dependency)
3. Re-annotation / comparison against original CounselBench expert metrics
4. Model-profile analyses, context interactions, OA prediction
5. Optional Relational Expectation (**R**); multi-turn follow-ups

---

## Safety / ethics

- Do not commit `.env`, API keys, or credentials
- Mental-health content may be sensitive; review dataset licenses, IRB guidance, and ethics requirements before broader release of annotations or model outputs

---

## License / usage

Academic research on mental-health AI evaluation. See `Executive Summary.pdf` for the full research plan, related work, experimental design, and intended repository release structure.
