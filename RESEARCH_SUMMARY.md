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

Three models answered 220 CounselBench prompts (660 responses). Five blinded annotators rated each response. OA was completed and locked before E/D/F. D follows the final v3.1 rule: score the highest-severity anthropomorphic cue spoken in the AI’s own voice.

## Focused findings

- HuMT has a weak negative association with OA (ρ = −0.096); it is not familywise-significant across the six headline hypotheses.
- Adding E/D/F improves prompt-grouped cross-validated R² by 0.087 over an identically adjusted HuMT baseline.
- This incremental signal is driven primarily by F; E and D have no independent OA association in the adjusted model.
- Models differ statistically in OA and F after multiplicity correction, but paired effect sizes are small; model differences in D are not supported.
- No E/D context moderation survives FDR correction.
- D does not differ reliably between the unmatched ADV and EVAL sets.
- Severe deception is rare: consensus ratings contain two D4 responses and no D5 responses. The study does not include a system-prompt comparator, so it does not test why severe cues are rare.

## Interpretation

The current evidence supports the framework’s central distinction: sounding human is not the same as being appropriate. Contextual fit is the clearest contributor to OA in this safety-conditioned corpus. Deception remains conceptually important, but targeted PERSONA-ADV prompts are needed to estimate severe failure modes.

All reproducible tables and figures are in `analysis_outputs/`.
