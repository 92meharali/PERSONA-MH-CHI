# Paper argument

The intended logic of the paper, in order. Written before the final analysis and
deliberately not tuned to interim results.

---

## Problem

Human-likeness in AI systems is increasingly measurable — by dedicated metrics
[Cheng2025HumT], by taxonomies of linguistic cues [DeVrio2025], by catalogues of
personification factors [Abercrombie2023]. But knowing how human-like a response
is does not tell us whether its anthropomorphic behaviour was **appropriate**.

The two come apart in both directions. A response can be highly human-like and
inappropriate, because the features that make it feel human also carry implicit
claims — to feeling, experience, memory, relationship, authority — that the
system cannot support. And a response can be less human-like and more
appropriate, because it preserves boundaries, marks uncertainty, and matches what
the situation calls for. Users prefer less human-like output in many contexts
[Cheng2025HumT]; anthropomorphic cues can inflate trust past warranted levels
[Leong2019]; [Abercrombie2023].

Disclosure regulation now attaches directly to this space: EU AI Act Article 50
became enforceable on 2 August 2026 [EUAIAct2024]. But disclosure is a one-time
obligation and anthropomorphic implication is a turn-by-turn behaviour. A system
can comply fully and still imply feeling and memory throughout a conversation.

## Gap

Existing evaluation collapses properties that come apart in practice. Empathy
measures quantify how much empathy is expressed [Sharma2020] without asking
whether it suited the situation. Quality benchmarks score responses without
separating relational, boundary, and contextual channels. Model-based judges
systematically overrate responses and miss what human experts flag
[CounselBench2025].

The result is that when an anthropomorphic response is judged inappropriate, no
existing instrument says *which property* made it so — whether the warmth was
miscalibrated, whether a false capacity was implied, or whether the whole posture
was wrong for the situation.

## Conceptual lens

Aristotle's distinction between *episteme* (generalizable or demonstrable
knowledge) and *phronesis* (practical judgment concerning variable particulars)
helps articulate the paper's motivating gap. PERSONA uses this distinction as a
conceptual lens rather than a literal measurement mapping. HumT-based `H`
captures linguistic human-likeness, not factual knowledge or *episteme*; `E`,
`D`, and `F` diagnose selected aspects of situation-sensitive calibration rather
than proving that a model possesses *phronesis*.

Context-aware computing further distinguishes the broader interactional
environment from the bounded domains studied here. Dey provides an operational
account of context and situation for context-aware applications; Dourish
emphasizes that context is also produced through interaction rather than fixed
in advance. PERSONA treats mental health, education, and general health as
analytical domains within this broader context.

## Proposal

Represent the anthropomorphic properties of a response as a profile:

```
P = (H, E, D, F)
```

`H` descriptive human-likeness (automated), `E` empathic appropriateness, `D`
anthropomorphic deception risk, `F` domain fit. `F` retains the original rubric's
focus on content, action, tone, certainty, and role boundaries while making its
domain-specific application explicit. Each dimension is defined so that it
captures a channel the others do not (`CONSTRUCT_DEFINITIONS.md`;
`DISTINCTIONS.md`).

## Methodological contribution

Evaluate the profile against **independently elicited overall appropriateness**.

`OA` is a holistic human judgment collected from Group A, while `E`, `D`, and
`F` are collected from a separate Group B. `OA` is never computed from the
profile dimensions. This matters because a framework whose criterion is derived
from its own predictors cannot be tested — a high R² would be arithmetic.
Separate pools make the relationship an empirical finding rather than a scoring
identity (`ANNOTATION_THEORY.md` §4).

## Empirical questions

1. To what extent does automated `H` diverge from domain-relevant judgments of `OA`? (RQ1)
2. What appropriateness-relevant information do `E`, `D`, and `F` provide that `H` alone omits? (RQ2)
3. How do the relative contributions of `E`, `D`, and `F` vary across mental health, education, and general health? (RQ3)
4. Does adversarial anthropomorphic elicitation activate `D`? (RQ4)

RQ4 is **not answerable with the present corpus** — the adversarial items target
clinical failure modes rather than anthropomorphic behaviour, and there is a
single system-prompt condition. It is reported as future work, not as a result.

## Contribution

A multidimensional empirical framework for studying **contextual conversational
appropriateness of anthropomorphic behaviour**, together with:

- construct definitions and an annotation protocol that separate the four
  channels operationally, including a `D` rubric with an explicit negative list
  marking its boundary against `F` and `OA`
- a criterion elicited from a separate OA annotator pool
- a multi-domain corpus with per-domain reliability
- a reproducible analysis pipeline

The framing is **calibration, not rejection**: the framework does not recommend
minimising human-likeness. `H` enters the profile with no assumed direction.

---

## Framing rules

**The contribution is `P`, not `S`.** `S` is a ranking convenience, confined to a
subsection, absent from the abstract.

**Report which claim the evidence supports.** The full-versus-`H` comparison
quantifies information omitted when evaluation relies on human-likeness alone;
it is not evidence that the profile is superior to every alternative
response-level baseline. If ablation shows the available signal is carried by
one dimension, the paper reports that directly. The result then identifies
*which channel carries appropriateness-relevant information* rather than
claiming validation that the data do not deliver.

**Do not retrofit.** This file predates the final analysis. If results are
unexpected, they are reported as results; the argument is not rewritten to have
predicted them.

**Negative results stay.** A framework that cannot be disconfirmed is not a
framework. Untestable-for-lack-of-variation and unsupported are different
verdicts and must not be conflated.
