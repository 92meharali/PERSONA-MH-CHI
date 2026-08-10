# Focused analysis summary

## Data

Corpus: relaxed system prompt (primary). 660 responses (220 prompts × 3 models), each rated independently by five annotators. Ratings use protocol v3.1; model identity was hidden during annotation. Relaxed professional-therapist system prompt (no anti-anthropomorphism ban). D follows the frozen v3.1 AI-attribution rule.

## Reliability

- OA: ordinal α=0.566; ICC(A,k)=0.851
- E: ordinal α=0.792; ICC(A,k)=0.948
- D: ordinal α=0.840; ICC(A,k)=0.959
- F: ordinal α=0.569; ICC(A,k)=0.864

## Core findings

- HuMT–OA Spearman ρ=-0.167 (95% prompt-cluster bootstrap CI -0.243 to -0.082); HuMT is treated as not a reliable OA proxy.
- Adding PERSONA dimensions and planned covariates changed grouped-CV R² by 0.333 relative to the identically adjusted HuMT baseline.
- Independently supported PERSONA coefficients: E (positive), D (negative), F (positive).
- Profile score S=(H+E−D+F)/4, with H=HuMT remapped to 1–5, tracks OA (ρ=0.429).
- Model ranking by mean S: gpt_5_6_sol (S=2.313, OA=4.720); claude_opus_4_8 (S=2.190, OA=4.133); glm (S=2.152, OA=4.098).
- Consensus D distribution: {"1": 163, "2": 297, "3": 190, "4": 10}. Severe D is rare in the evaluated response corpus.

## Hypotheses

- **H1** Is human-likeness a reliable proxy for OA? — Supported: HuMT is not a reliable OA proxy (estimate=-0.167, Holm p=0.474).
- **H2** Do E/D/F add predictive information beyond HuMT? — Supported (estimate=0.333, Holm p=1.29e-76).
- **H3** In the joint model, do E and F associate positively with OA and D negatively? — Supported (estimate=0.0303, Holm p=0.0361).
- **H4** Do models differ in OA/E/F profiles? — Supported (estimate=0.411, Holm p=3.9e-43).

## Interpretation limits

- Scores are ordinal; five-rater means are used for concise primary summaries, with median sensitivity.
- Inference is clustered/grouped by prompt to preserve the three-model pairing.
- CounselBench ADV and EVAL prompts are unmatched; their comparison is associative, not causal.
- Profile P reports H/E/D/F separately; S is a secondary equal-weight ranking index, not a replacement for independent OA.
- H is a corpus min–max remap of HuMT onto 1–5 so it can enter S on the same scale as E/D/F.
- D4–D5 remain uncommon relative to D1–D3; interpret high-severity tails cautiously.
