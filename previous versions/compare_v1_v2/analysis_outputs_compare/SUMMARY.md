# v1 vs v2 condition comparison

v1 = original anti-anthropomorphism system prompt.
v2 = relaxed professional-therapist system prompt.

Prompts are shared (220). Model sets differ (v1 has gemini; v2 has gpt_5_6_sol).
Primary confirmatory contrast uses shared models only: claude_opus_4_8 and glm.

## Corpus means (all responses)

- OA: v1=4.406, v2=4.317 (Δ=-0.089)
- E: v1=3.457, v2=3.736 (Δ=+0.279)
- D: v1=1.545, v2=2.093 (Δ=+0.547)
- F: v1=4.211, v2=4.361 (Δ=+0.149)

## Shared-model prompt-level contrast

- D: v2−v1 = +0.743 (Wilcoxon p_holm=5.16e-30)
- OA: v2−v1 = -0.334 (Wilcoxon p_holm=7.84e-18)

## Consensus median D counts

condition  D_median  n_responses
       v1         1          427
       v1         2          181
       v1         3           50
       v1         4            2
       v2         1          163
       v2         2          297
       v2         3          190
       v2         4           10

## Interpretation

- The relaxed prompt increases deception-risk exposure relative to v1.
- Use shared-model paired tests for condition claims; full-corpus tests mix different third models.
