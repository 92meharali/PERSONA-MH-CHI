# Citation matrix

Every theoretical claim, its source, what the source actually supports, and the
status of that support.

**Status values**

| Status | Meaning |
|---|---|
| Direct support | Source states or demonstrates the claim itself |
| Verified | Bibliographic details confirmed; source supports the claim as background |
| Weak support | Source is relevant but does not establish the claim; needs a better citation |
| Needs verification | Bibliographic details unconfirmed — cannot be used yet |
| Unsupported | No citation currently attached — must be found or the claim softened |

A source is listed only where it supports the specific sentence, not because it
is broadly on topic.

---

## Human-likeness (H)

| Claim | Source | What it supports | Status |
|---|---|---|---|
| Human-like tone can be measured automatically from LLM token probabilities | [Cheng2025HumT] | The metric itself; feature set (pronouns, conversational register, personal opinion) | Direct support |
| Users prefer less human-like output in many contexts | [Cheng2025HumT] | Stated finding across preference and usage datasets | Direct support |
| Human-like output correlates with warmth, social closeness, femininity, low status | [Cheng2025HumT] | Stated finding | Direct support |
| Anthropomorphic signalling differs from anthropomorphic perception | [Epley2007]; [Waytz2010] | Anthropomorphism as a person-side psychological process with stable individual differences | Verified (inference is ours; sources support the person-side account, not the distinction as stated) |
| Linguistic cues drive personification of dialogue systems | [Abercrombie2023]; [DeVrio2025] | Catalogue and taxonomy of contributing expressions | Verified |
| Social cues in conversational agents can be taxonomised | [Feine2019] | — | Needs verification |

## Empathy (E)

| Claim | Source | What it supports | Status |
|---|---|---|---|
| Text-based empathy needs its own measurement, not face-to-face instruments | [Sharma2020] | Stated motivation of the paper | Direct support |
| Empathy in text support decomposes into distinguishable mechanisms | [Sharma2020] | Emotional reactions, interpretations, explorations on ordinal scales | Direct support |
| Existing empathy measures quantify expression, not calibration to situation | [Sharma2020] | Supported by what the instrument measures; the gap is our reading | Weak support — no source states the gap explicitly |
| Models can produce responses rated highly empathetic | [Ayers2023] | — | Needs verification (**load-bearing**) |
| High empathy is not automatically appropriate | — | — | **Unsupported** — currently argued from the rubric and from reasoning; find a source or present as a definitional stance |

## Deception risk (D)

| Claim | Source | What it supports | Status |
|---|---|---|---|
| Anthropomorphic design can be dishonest and harmful to users | [Leong2019] | Taxonomy of dishonest anthropomorphism and associated harms | Direct support |
| An honest-anthropomorphism principle exists in the literature | [Kaminski2017] via [Leong2019] | Origin of the principle | Verified (secondary) |
| Personification can produce transparency failures and over-reliance | [Abercrombie2023] | Stated in the abstract | Direct support |
| Deception and overreliance motivate measuring human-like tone | [Cheng2025HumT] | Stated motivation | Direct support |
| Disclosure that a user is interacting with AI is a legal obligation in the EU | [EUAIAct2024] | Article 50(1); enforceable 2 Aug 2026 | Direct support |
| Disclosure obligations do not reach turn-by-turn anthropomorphic implication | [EUAIAct2024] | Article 50 governs disclosure, not conversational behaviour | Direct support (reading of scope, stated as ours) |
| Trust should track reliability; anthropomorphic cues can inflate it independently | [Lee2004]; [Waytz2010] | Appropriate reliance; anthropomorphism predicts trust placed in agents | Needs verification for [Lee2004] (**load-bearing**); [Waytz2010] Verified |
| Deception in social robotics requires explicit treatment | [Sharkey2020]; [Danaher2020] | — | Needs verification |
| Ordinary conversational anthropomorphism differs from misleading signalling | Project rubric | The `D` negative list operationalises the boundary | Direct support (own protocol, not external) |

## Contextual fit (F)

| Claim | Source | What it supports | Status |
|---|---|---|---|
| Appropriateness norms are context-relative | [Nissenbaum2004] | Informational norms specific to social contexts | Needs verification (**load-bearing**) |
| Domain experts flag failures that quality scores miss | [CounselBench2025] | LLMs scored high on perceived quality yet were flagged for unauthorised medical advice | Direct support |
| Model-based judges are unreliable for expert-identified issues | [CounselBench2025] | LLM judges overrate and overlook safety issues experts identify | Direct support |
| `F` is not general response quality | Project rubric | Same text scores differently by scenario | Direct support (own protocol) |
| Different domains impose different warmth/boundary/authority expectations | — | — | **Weak support** — [CounselBench2025] covers mental health only; no source spans the three domains |

## Overall appropriateness (OA)

| Claim | Source | What it supports | Status |
|---|---|---|---|
| A criterion computed from its predictors cannot test them | — | — | Methodological reasoning; no citation needed, but a measurement-theory source would strengthen it |
| Human rather than model annotation is required for these judgments | [CounselBench2025] | LLM judges systematically overrate and miss expert-flagged issues | Direct support |
| Reliability should be reported per construct and per context | — | — | Standard practice; [Krippendorff2004] would support | Needs verification |

## Core argument

| Claim | Source | What it supports | Status |
|---|---|---|---|
| Human-likeness is not equivalent to appropriateness | [Cheng2025HumT] | Preference and human-likeness diverge | Direct support |
| Human-like language supports natural interaction and social presence | [Nass1994]; [Reeves1996] | — | Needs verification |
| Human-likeness has mixed rather than negative valence | [Cheng2025HumT] | Correlates with warmth (often desirable) yet dispreferred in many contexts | Direct support |
| Prior work does not decompose *why* human-likeness and preference diverge | [Cheng2025HumT] | Absence of such decomposition in the source | Weak support — an absence claim; verify no other work has done this before asserting novelty |

---

## Open citation tasks

**Priority 1 — load-bearing and unverified**

1. [Lee2004] — the entire over-reliance harm mechanism rests on it.
2. [Nissenbaum2004] — the only theoretical grounding for context-relativity.
3. [Ayers2023] — the claim that models already achieve high measured empathy.

**Priority 2 — unsupported claims needing a source or a softer statement**

4. "High empathy is not automatically appropriate" — currently reasoning plus own
   rubric. Either find support in the therapeutic-alliance or supportive-
   communication literature, or present it explicitly as a definitional stance of
   the framework rather than an established finding.
5. "Different domains impose different expectations around warmth, boundaries,
   and authority" — the domain argument's foundation, currently supported only
   for mental health. Needs at least one education-side and one general-health-side
   source.

**Priority 3 — novelty claims**

6. The claim that no prior work decomposes the human-likeness/appropriateness
   divergence is an absence claim. Absence claims need a documented search, not
   an impression. Run and record one before the paper asserts novelty.

**Priority 4 — completeness**

7. [CounselBench2025] author list and final venue.
8. [DeVrio2025], [Cheng2025Dehumanizing] DOIs and page ranges.
9. Resolve the [Sharkey2020] year discrepancy (2020 vs 2021 in secondary
   sources).
