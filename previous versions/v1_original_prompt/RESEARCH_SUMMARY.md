# PERSONA-MH research summary

## Idea

Human-like language is not automatically appropriate in mental-health AI. PERSONA-MH separates:

- human-likeness (H / HuMT);
- empathic appropriateness (E);
- anthropomorphic deception risk (D);
- contextual fit (F);
- independent overall appropriateness (OA).

The multidimensional profile is **P = (H, E, D, F)** with OA as an independent target. A secondary equal-weight score

\[
S = (H + E - D + F) / 4
\]

ranks responses/models after remapping continuous HuMT onto the same 1–5 Likert range as the human ratings. S is not a substitute for OA.

## Study

Three models answered 220 CounselBench prompts (660 responses). Five blinded annotators rated each response. OA was completed and locked before E/D/F. Empathy scores come from a second blind round with the same E rubric after annotators were asked to apply it carefully. Shared evidence spans are excluded from analysis. D follows the final v3.1 rule: score the highest-severity anthropomorphic cue spoken in the AI’s own voice.

## Confirmatory hypotheses

1. **H1** — Human-likeness is not a reliable proxy for OA.
2. **H2** — E/D/F add predictive information beyond HuMT.
3. **H3** — In the joint model, E and F associate positively with OA and D negatively.
4. **H4** — Models differ in OA/E/F profiles.

## Focused findings

- HuMT–OA ρ ≈ −0.096 with near-zero standalone CV R²; **H1 supported** (HuMT is not a reliable OA proxy).
- Adding E/D/F improves prompt-grouped cross-validated R² by ≈ 0.266 over an identically adjusted HuMT baseline; **H2 supported**.
- In the adjusted model, E (+), D (−), and F (+) are each independently associated with OA; **H3 supported**.
- Models differ on OA/E/F with small paired effects; **H4 supported**.
- Blind E reannotation raised E reliability (ordinal α ≈ 0.83; ICC(A,k) ≈ 0.95) and the OA–E association (ρ ≈ 0.44).
- Equal-weight **S** tracks OA (ρ ≈ 0.33). Ablation shows the PERSONA-only form \(S_{\text{persona}}=(E-D+F)/3\) tracks OA more closely (ρ ≈ 0.41), consistent with H not being a normative appropriateness signal.
- Model ranking by mean S: GLM ≳ Claude ≫ Gemini; OA ranking puts Claude first, so S and OA ranks are related but not identical.
- Severe deception is rare: consensus ratings contain two D4 responses and no D5 responses.

## Interpretation

Sounding human is not the same as being appropriate. Empathic appropriateness and contextual fit help OA; deception risk hurts OA. Profile **P** reports the dimensions separately; score **S** provides a transparent secondary ranking index supported by ablation and sensitivity checks.

All reproducible tables and figures are in `analysis_outputs/`.
