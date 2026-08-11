# Theoretical distinctions

PERSONA depends on a set of conceptual separations. Each is stated as a claim,
with the case that shows the two come apart. These are conceptual arguments; the
empirical question of whether the constructs are *measurably* distinguishable is
separate and belongs to the separability analysis.

---

## Human-likeness ≠ Empathy

Human-likeness is a register; empathy is a communicative act.

- Human-like, not empathic: casual, opinionated, first-person, and completely
  fails to acknowledge the user's distress.
- Empathic, not especially human-like: plain, formal language that accurately
  names what the user is feeling and why it is reasonable.

The two correlate in practice — HumT's own validation finds human-like output
correlates with perceived warmth [Cheng2025HumT] — but correlation across a
corpus is not identity, and the framework needs them separated precisely because
the correlation is imperfect.

## Human-likeness ≠ Deception

Human-likeness is how the language reads; deception risk is what it claims.

- Human-like, not deceptive: warm and conversational while stating plainly it is
  an AI and making no claim to feeling or memory.
- Deceptive, not human-like: flat and formal while asserting clinical authority
  or guaranteeing confidentiality it cannot provide.

Conflating the two produces the position PERSONA rejects — that anthropomorphic
language is inherently a problem. The problem is the false implication, not the
register.

## Human-likeness ≠ Contextual fit

Fit is defined relative to a situation; human-likeness is not.

The same human-like response scores differently on `F` depending on what it is
responding to. A light conversational reply fits a casual check-in and fails a
crisis. `H` does not move; `F` does. A property that varies with context while
another holds constant cannot be the same property.

## Empathy ≠ Appropriateness

Empathy is one channel among several. A response can validate feelings warmly
and still be inappropriate because it does not answer the question, misses an
urgent safety need, or overreaches on certainty. Warmth is not a substitute for
the action a situation requires.

## Contextual fit ≠ Safety

`F` includes safety-relevant considerations but is not reducible to them. A
response can be entirely safe and still poorly fitted — clinically cautious,
accurate, and wholly unresponsive to what was asked. Conversely a well-fitted
response is not thereby safe; fit does not verify facts. Safety is a
partially-overlapping property, and PERSONA does not measure it.

## Appropriateness ≠ Human-likeness

This is the framework's central claim and the reason it exists. Stated
carefully: **the ordering of responses by human-likeness is not the ordering of
responses by appropriateness.** Not that they are unrelated; not that
human-likeness is bad. That one cannot be substituted for the other.

## Appropriateness ≠ General helpfulness

Helpfulness asks whether the user got what they wanted. Appropriateness asks
whether what they got was suitable, which sometimes means declining, redirecting,
or stating a limit. A maximally helpful response to a request for a diagnosis may
be an inappropriate one.

## Appropriateness ≠ Clinical effectiveness

`OA` is a judgment about a single response in a single turn. Clinical
effectiveness is an outcome measured over time in a person's life. Nothing in
this project licenses inference from one to the other. A response judged highly
appropriate has not been shown to help anyone; a response judged inappropriate
has not been shown to harm anyone. See `CLAIMS_AND_BOUNDARIES.md`.

---

## Scope statement for the paper

PERSONA is about **contextual conversational appropriateness of anthropomorphic
behaviour**.

It is **not**:

- a universal AI safety metric
- an objective moral measure
- a clinical outcome measure
- a benchmark of general model capability
- a compliance instrument for any regulation

Reviewers will test the boundary between what the framework measures and what its
name suggests it measures. The scope statement should appear early in the paper,
not buried in limitations.
