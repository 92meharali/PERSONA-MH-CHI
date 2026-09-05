# Hypotheses

**All five are theory-derived and pre-analysis.** They are stated here as
predictions from the framework, with the reasoning that generates them. This file
records what the theory predicted; it is not a results file and must not be
edited to match outcomes. Findings belong in `analysis/outputs/`.

Where a hypothesis is not supported, the negative result is preserved and
reported. A framework that cannot be disconfirmed is not a framework.

---

### H1 — Human-likeness alone is insufficient to explain overall appropriateness

**Derivation.** If the two asymmetries in `PERSONA_THEORY.md` §2 occur (human-like
but inappropriate; less human-like but appropriate), then human-likeness cannot
determine appropriateness. Users prefer less human-like output in many contexts
[Cheng2025HumT], and anthropomorphic cues can inflate trust beyond warranted
levels [Leong2019], so the relationship should be weak and is not required to be
positive.

**Prediction.** `H` explains little variance in `OA`.

**Critical caveat.** This hypothesis is directional-agnostic and easy to
"confirm" badly. Two failure modes must be avoided:

1. **Accepting the null.** Failing to find a relationship is not the same as
   showing there is none. If the association is not statistically distinguishable
   from zero, the correct statement is that no reliable relationship was
   detected — not that human-likeness is unrelated to appropriateness.
2. **Restricted variance.** If `H` barely varies in this corpus, a weak
   relationship is expected regardless of the truth. The variance must be
   reported next to the estimate.

H1 is the framework's *premise*, and confirming a premise weakly is the most
likely way for this paper to overclaim.

---

### H2 — The full profile explains OA better than human-likeness alone

**Derivation.** `E`, `D`, and `F` are defined as properties that bear on
appropriateness through channels `H` does not capture: calibration of warmth,
truthfulness of implied capacities, and situational fit. If those definitions
pick out real properties of responses, adding them should improve explanation of
an independently elicited criterion.

**Prediction.** Out-of-sample explanatory performance for `H + E + D + F` exceeds
that for `H` alone, by a margin whose uncertainty interval excludes zero.

**Constraint.** Must be evaluated out-of-sample with grouping on prompt.
In-sample R² is not evidence: adding predictors cannot reduce it.

**What H2 does not establish.** That the profile is *multidimensional*. If one
dimension carries the increment, H2 is supported and the multidimensionality
claim is not. These must be reported separately — see H3.

---

### H3 — Domain fit provides incremental information beyond human-likeness

**Derivation.** `F` is the dimension defined directly in terms of the
situation, and appropriateness is situation-relative. Of the four, `F` should
have the strongest relationship with `OA`.

**Prediction.** `F` improves explanation of `OA` over `H` alone.

**The construct-overlap problem, stated in advance.** `F` and `OA` are
conceptually adjacent: `F` asks whether tone, certainty, and role fit the
situation; `OA` asks holistically whether the response was suitable. A strong
`F`-`OA` relationship is therefore *partly* predicted by the definitions, and is
weaker evidence for the framework than an equally strong `E`-`OA` or `D`-`OA`
relationship would be.

This is recorded here, before analysis, so that it cannot later look like a
post-hoc excuse. If `F` dominates, the honest reading is that appropriateness
judgments are carried by contextual calibration rather than by the anthropomorphic
channels — an interesting finding, but not a validation of `P` as a
multidimensional construct.

**Corollary predictions worth testing explicitly.**

- H3a: `E` adds information beyond `H` and `F`.
- H3b: `D` adds information beyond `H` and `F`.

If H3a and H3b both fail while H3 succeeds, the framework reduces empirically to
`F`, and the paper must say so.

---

### H4 — Dimension-appropriateness relationships differ across domains

**Derivation.** Appropriateness norms are context-relative [Nissenbaum2004][NV].
Domains impose different expectations around warmth, boundaries, authority, and
certainty: emotional validation is central in crisis support and largely
irrelevant to a factual education query; role-boundary claims carry different
weight where clinical authority is at stake. If `E`, `D`, and `F` capture these
channels, their relationships with `OA` should not be constant across domains.
Authority calibration enters primarily through `F` and `OA`; it enters `D` only
when professional language enacts false human identity, relationship, or
continuity.

**Prediction.** A formal interaction between domain and the dimensions improves
model fit over a domain-invariant specification.

**Constraints.**

- Requires a formal interaction test. Differing per-domain coefficients are not
  evidence of interaction.
- Domain is confounded with dataset source, prompt construction, and rating
  batch. A supported H4 does not establish that *context* caused the difference.
- Restricted criterion variance in any domain undermines its contribution.

**Deliberately not predicted:** the *direction* of any domain difference. The
literature does not support directional predictions at this granularity, and
inventing them would be retrofitting.

---

### H5 — Deception risk is negatively associated with appropriateness where deception-relevant behaviour is elicited

**Derivation.** Misleading implication of experience, feeling, memory,
relationship, continuity, or human professional identity is a boundary
violation [Leong2019], and transparency about machine status is a normative
expectation now reflected in regulation [EUAIAct2024]. Where such behaviour
occurs, raters should judge it less appropriate. Unsupported expertise without
anthropomorphic self-presentation is outside this hypothesis.

**Prediction.** Higher `D` associates with lower `OA`, conditional on
deception-relevant behaviour actually being present.

**The conditional is load-bearing and is currently unmet.** As documented in
`RESEARCH_QUESTIONS.md` (RQ4), the corpus contains no condition designed to
elicit anthropomorphic behaviour: the adversarial items target clinical failure
modes, and there is a single system-prompt condition. If `D` sits near its floor
for most responses, the hypothesis is untested rather than disconfirmed — there
is no variation for a relationship to appear in.

**Reporting rule.** If `D` shows floor effects, report H5 as **untested for lack
of elicited variation**, not as unsupported. These are different scientific
statements and only one of them is honest here.

---

## Status table

| # | Hypothesis | Type | Precondition | Status |
|---|---|---|---|---|
| H1 | H alone insufficient | Pre-analysis | Adequate `H` variance | Awaiting analysis |
| H2 | Full profile > H alone | Pre-analysis | Out-of-sample, prompt-grouped | Awaiting analysis |
| H3 | F adds beyond H | Pre-analysis | Construct-overlap caveat noted | Awaiting analysis |
| H3a | E adds beyond H and F | Pre-analysis | — | Awaiting analysis |
| H3b | D adds beyond H and F | Pre-analysis | — | Awaiting analysis |
| H4 | Domain differences | Pre-analysis | Formal interaction test | Awaiting analysis |
| H5 | D negatively related to OA | Pre-analysis | **Requires elicited D variation — not currently met** | Likely untestable with current data |
