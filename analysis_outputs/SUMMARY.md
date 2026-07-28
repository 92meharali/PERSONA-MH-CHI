# Focused analysis summary

## Data

660 responses (220 prompts × 3 models), each rated independently by five annotators. OA was locked before E/D/F. D follows the frozen v3.1 AI-attribution rule.

## Reliability

- OA: ordinal α=0.453; ICC(A,k)=0.785
- E: ordinal α=0.493; ICC(A,k)=0.816
- D: ordinal α=0.733; ICC(A,k)=0.941
- F: ordinal α=0.458; ICC(A,k)=0.783

## Core findings

- HuMT–OA Spearman ρ=-0.096 (95% prompt-cluster bootstrap CI -0.171 to -0.011).
- Adding PERSONA dimensions and planned covariates changed grouped-CV R² by 0.087 relative to the identically adjusted HuMT baseline.
- The joint PERSONA increment is driven by independently supported coefficient(s): F. E and D should not be interpreted as independent OA predictors here.
- Consensus D distribution: {"1": 427, "2": 181, "3": 50, "4": 2}. Severe D is rare in the evaluated response corpus.

## Hypotheses

- **H1** Is human-likeness a weak proxy for OA? — Weak magnitude; not familywise-significant (estimate=-0.0961, Holm p=0.068).
- **H2** Do E/D/F add predictive information beyond HuMT? — Supported jointly; individual coefficients are secondary (estimate=0.0872, Holm p=2.5e-09).
- **H3** Do models differ in OA profiles? — Supported (estimate=0.0288, Holm p=0.0355).
- **H4** Do models differ in deception risk? — Not supported (estimate=0.0145, Holm p=0.31).
- **H5** Is E/D association with OA context-dependent? — Not supported (estimate=6.32, Holm p=0.612).
- **H6** Does D differ between ADV and EVAL sets? — No supported association (estimate=-0.089, Holm p=0.377).

## Interpretation limits

- Scores are ordinal; five-rater means are used for concise primary summaries, with median sensitivity.
- Inference is clustered/grouped by prompt to preserve the three-model pairing.
- CounselBench ADV and EVAL prompts are unmatched; their comparison is associative, not causal.
- Severe deception is rare in this corpus, so D4–D5 estimates have limited support; no causal explanation for that rarity is tested here.
