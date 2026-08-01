# Focused analysis summary

## Data

660 responses (220 prompts × 3 models), each rated independently by five annotators. OA was locked before E/D/F. D follows the frozen v3.1 AI-attribution rule.

## Reliability

- OA: ordinal α=0.453; ICC(A,k)=0.785
- E: ordinal α=0.834; ICC(A,k)=0.950
- D: ordinal α=0.733; ICC(A,k)=0.941
- F: ordinal α=0.458; ICC(A,k)=0.783

## Core findings

- HuMT–OA Spearman ρ=-0.096 (95% prompt-cluster bootstrap CI -0.171 to -0.011); HuMT is treated as not a reliable OA proxy.
- Adding PERSONA dimensions and planned covariates changed grouped-CV R² by 0.266 relative to the identically adjusted HuMT baseline.
- Independently supported PERSONA coefficients: E (positive), D (negative), F (positive).
- Profile score S=(H+E−D+F)/4, with H=HuMT remapped to 1–5, tracks OA (ρ=0.325).
- Model ranking by mean S: glm (S=2.333, OA=4.420); claude_opus_4_8 (S=2.315, OA=4.478); gemini (S=2.221, OA=4.321).
- Consensus D distribution: {"1": 427, "2": 181, "3": 50, "4": 2}. Severe D is rare in the evaluated response corpus.

## Hypotheses

- **H1** Is human-likeness a reliable proxy for OA? — Supported: HuMT is not a reliable OA proxy (estimate=-0.0961, Holm p=0.017).
- **H2** Do E/D/F add predictive information beyond HuMT? — Supported (estimate=0.266, Holm p=2.8e-41).
- **H3** In the joint model, do E and F associate positively with OA and D negatively? — Supported (estimate=0.0477, Holm p=0.0157).
- **H4** Do models differ in OA/E/F profiles? — Supported (estimate=0.0288, Holm p=9.05e-05).

## Interpretation limits

- Scores are ordinal; five-rater means are used for concise primary summaries, with median sensitivity.
- Inference is clustered/grouped by prompt to preserve the three-model pairing.
- CounselBench ADV and EVAL prompts are unmatched; their comparison is associative, not causal.
- Profile P reports H/E/D/F separately; S is a secondary equal-weight ranking index, not a replacement for independent OA.
- H is a corpus min–max remap of HuMT onto 1–5 so it can enter S on the same scale as E/D/F.
- Severe deception is rare in this corpus, so D4–D5 estimates have limited support.
