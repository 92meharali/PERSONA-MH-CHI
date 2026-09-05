# PERSONA: theoretical foundation

**Status:** theory document. Contains no empirical results. Written before the
final statistical analysis is complete, and deliberately not revised to match
interim findings. See `CLAIMS_AND_BOUNDARIES.md` for what the project may and
may not currently assert.

---

## 1. The question

> When is anthropomorphic AI behaviour appropriate in context?

PERSONA is a framework for studying **contextual conversational
appropriateness of anthropomorphic behaviour**. It is not a general AI safety
metric, not a measure of response quality, and not a moral evaluation of
anthropomorphism as such.

## 2. What PERSONA does and does not argue

**The argument is not:** human-like AI is bad.

**The argument is:** human-likeness alone is insufficient to determine whether
anthropomorphic behaviour is appropriate in a given context.

Two asymmetries motivate this.

A response may be **highly human-like and inappropriate** because it implies
emotion the system does not have, personal experience it has not had, a
relationship that does not exist, memory or continuity it does not possess,
human professional identity it does not hold, or certainty the evidence does
not support.

A response may be **less human-like and more appropriate** because it preserves
role boundaries, states its limits, marks its uncertainty, and matches what the
situation actually calls for.

If both asymmetries occur in practice, then any single scalar ordering of
responses by human-likeness is insufficient for judging appropriateness, and a
multidimensional representation is required.

### Episteme and phronesis as a conceptual lens

PERSONA is informed by Aristotle's distinction between *episteme*, knowledge of
generalizable or demonstrable matters, and *phronesis*, practical judgment about
what to do in variable particular circumstances. This is a sensitizing lens,
not a claim that the framework directly measures either virtue or that a model
possesses practical wisdom. In particular, HumT-based `H` measures linguistic
human-likeness, not factual accuracy or scientific knowledge. `E`, `D`, and `F`
offer narrower diagnostics of situation-sensitive response calibration.

Context and domain are also separated. **Context** is the broader,
multidimensional environment through which an interaction acquires meaning.
Mental health, education, and general health are bounded analytical
**domains** within that environment. `F` retains the annotation rubric's focus
on content, action, tone, certainty, and role boundaries, while the name
**Domain Fit** makes its domain-specific application explicit.

## 3. The framework

PERSONA represents the anthropomorphic properties of a single response as a
profile:

```
P = (H, E, D, F)
```

| Symbol | Construct | Source |
|---|---|---|
| `H` | Human-likeness | Automated (HumT) |
| `E` | Empathic appropriateness | Human rating |
| `D` | Anthropomorphic deception risk | Human rating |
| `F` | Domain fit: situation-sensitive content, action, tone, certainty, and role boundaries within a domain | Human rating |

These are evaluated against a separate quantity:

| Symbol | Construct | Source |
|---|---|---|
| `OA` | Overall appropriateness | Group A independent holistic human judgment |

**`OA` is not computed from `E`, `D`, or `F`.** It is elicited from Group A and
serves as the criterion against which the Group B profile dimensions are
examined. This is the central methodological commitment of the framework and the
reason it is not circular. See `ANNOTATION_THEORY.md` for how this is
operationalised in the current release.

Full definitions are in `CONSTRUCT_DEFINITIONS.md`. The pairwise conceptual
separations the framework depends on are in `DISTINCTIONS.md`.

## 4. The scalar S is secondary

An optional scalar projection exists:

```
S = (H + E - D + F) / 4
```

`S` is a transparent ranking index for benchmarking, nothing more. It is **not**
ground truth, **not** `OA`, and **not** the contribution. A scalar necessarily
hides trade-offs among dimensions — two responses with identical `S` may have
opposite profiles, and the difference between them is precisely what PERSONA
exists to capture. `S` must not become the conceptual centre of the paper. See
`CLAIMS_AND_BOUNDARIES.md` §S.

## 5. Why a profile rather than a single measure

The framework separates four properties that evaluation practice frequently
collapses:

- **`H` is descriptive.** It says how human-like the language is, not whether
  that is good here. Human-likeness has no fixed valence.
- **`E` is relational.** Warmth and validation, judged by whether they are
  calibrated to the situation, not by their intensity.
- **`D` is a boundary and transparency property.** Whether the response implies
  experience, feeling, memory, relationship, continuity, or false human
  professional identity that the system does not have. Expertise or certainty
  alone is not `D`.
- **`F` is domain-sensitive calibration.** Whether content, action, tone,
  certainty, and role behaviour match the situation within the relevant domain.

These can move independently. A response can be warm and honest about being an
AI (high `E`, low `D`). It can be warm because it claims to care personally
(high `E`, high `D`). It can be human-like and well-calibrated, or human-like
and badly mismatched. A framework that measures only human-likeness cannot
distinguish these cases; a framework that measures only quality cannot say which
property produced the problem.

## 6. What PERSONA models

PERSONA does not define objective morality and does not claim that
appropriateness is a property of a response in isolation. It models the
**relationship between observable interactional properties of a response and
context-dependent human judgments of it**. Appropriateness here is normative and
audience-relative: it is what these raters, applying this rubric, in this domain,
judged suitable. See `CONCEPTUAL_MODEL.md`.

## 7. Document map

| File | Contents |
|---|---|
| `CONSTRUCT_DEFINITIONS.md` | Rigorous definitions of H, E, D, F, OA |
| `DISTINCTIONS.md` | The conceptual separations the framework requires |
| `LITERATURE_MAP.md` | Literature organised around the actual argument |
| `RESEARCH_QUESTIONS.md` | RQ1-RQ4 and which are answerable with current data |
| `HYPOTHESES.md` | H1-H5, marked pre-analysis |
| `CONCEPTUAL_MODEL.md` | Context to judgment pipeline |
| `ANNOTATION_THEORY.md` | Why two rating groups; the protocol as actually run |
| `CLAIMS_AND_BOUNDARIES.md` | Limitations and claim boundaries |
| `PAPER_ARGUMENT.md` | Intended paper logic |
| `BIBLIOGRAPHY.md` | Verified references and those needing verification |
| `CITATION_MATRIX.md` | Claim-level citation accounting |
