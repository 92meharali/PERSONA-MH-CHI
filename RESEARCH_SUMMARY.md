# PERSONA-MH research summary

## Idea

Human-like language is not automatically appropriate in mental-health AI. PERSONA-MH separates:

- human-likeness (HuMT);
- empathic appropriateness (E);
- anthropomorphic deception risk (D);
- contextual fit (F);
- independent overall appropriateness (OA).

The same response can be warm yet misleading. The study tests whether E/D/F explain OA beyond surface human-likeness.

## Study

Three models answered 220 CounselBench prompts (660 responses). Five blinded annotators rated each response. OA was completed and locked before E/D/F. Empathy scores come from a second blind round with the same E rubric after annotators were asked to apply it carefully. Shared evidence spans are excluded from analysis. D follows the final v3.1 rule: score the highest-severity anthropomorphic cue spoken in the AI’s own voice.

## Focused findings

- HuMT has a weak negative association with OA (ρ = −0.096); it is not familywise-significant across the six headline hypotheses.
- Adding E/D/F improves prompt-grouped cross-validated R² by 0.266 over an identically adjusted HuMT baseline.
- In the adjusted model, E (positive), D (negative), and F (positive) are each independently associated with OA.
- Blind E reannotation raised E reliability (ordinal α ≈ 0.83; ICC(A,k) ≈ 0.95) and the OA–E association (ρ ≈ 0.44).
- Models differ statistically in OA after multiplicity correction, but paired effect sizes are small; model differences in D are not supported.
- No E/D context moderation survives confirmatory testing.
- D does not differ reliably between the unmatched ADV and EVAL sets.
- Severe deception is rare: consensus ratings contain two D4 responses and no D5 responses. The study does not include a system-prompt comparator, so it does not test why severe cues are rare.

## Interpretation

The current evidence supports the framework’s central distinction: sounding human is not the same as being appropriate. With carefully reannotated E, empathic appropriateness, deception risk, and contextual fit each contribute independent signal for OA in this safety-conditioned corpus. Severe deception remains rare under the anti-anthropomorphism generation prompt; loosening that prompt (not the D rubric) is the next step for estimating high-severity failure modes.

All reproducible tables and figures are in `analysis_outputs/`.
