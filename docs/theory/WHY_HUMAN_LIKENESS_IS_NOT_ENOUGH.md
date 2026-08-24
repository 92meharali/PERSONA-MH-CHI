# Why human-likeness is not enough

The central argument of the paper, stated carefully. This section is where
overclaiming is easiest, so each step is separated and the conclusion is kept
narrow.

---

## 1. Human-like language does real work

Beginning from the harms would be a straw man. Human-like language:

- makes interaction feel natural and lowers the effort of using a system
- supports social presence, which is a design goal in conversational systems
  [Nass1994][NV]; [Reeves1996][NV]
- correlates with perceived warmth and social closeness [Cheng2025HumT], which in
  supportive contexts are frequently what the situation calls for
- sustains engagement, which for tutoring or long-term support is a precondition
  for any benefit at all

Any framework that treats human-likeness as a defect is wrong about the design
space. PERSONA does not.

## 2. The same language can carry false implications

The properties that make a response feel human are also the properties that carry
implicit claims about the speaker. First-person stance, expressions of feeling,
references to shared experience, and relational language are human-like *because*
humans use them to convey states they actually have.

When a system uses them, it may imply:

- **emotions it does not have** — "I feel terrible that you're going through this"
- **personal experience it has not had** — "I know exactly what that's like"
- **human professional identity it does not hold** — speaking as the user's
  clinician or enacting an ongoing professional relationship
- **memory it does not possess** — "I've been thinking about what you said"
- **relational continuity it cannot provide** — "I'll always be here for you"
- **certainty the evidence does not support** — confident framing of a contested
  claim

These are not stylistic quibbles. [Leong2019] identifies exactly this class as
dishonest anthropomorphism: designs that exploit predictable human responses to
human-like cues in ways contrary to the user's interest.

## 3. False implications matter because trust should track reliability

Appropriate reliance requires that a user's trust correspond to the system's
actual reliability [Lee2004][NV]. Anthropomorphic cues can raise trust
independently of reliability, and individual differences in anthropomorphism
predict how much responsibility and trust people place in an agent [Waytz2010].
[Abercrombie2023] connects personification directly to transparency failure and
over-reliance.

So the harm mechanism is not "users are deceived and feel bad". It is: the cue
raises trust, trust is not matched by reliability, and reliance becomes
miscalibrated. In a domain where miscalibrated reliance has consequences —
medication, crisis, diagnosis — this is a safety-relevant property of the
response, reachable from the text.

## 4. Context determines whether the same feature helps or harms

Warmth in crisis support is appropriate and probably necessary. The same warmth
in response to a factual query is a mismatch. Sustained encouragement in tutoring
is pedagogically motivated; the same language implying an ongoing personal
relationship in mental health support is a boundary problem.

The feature does not change. Its appropriateness does. So appropriateness cannot
be a function of the feature alone.

## 5. Therefore

> **Increasing `H` is not equivalent to increasing appropriateness.**

Not "decreasing `H` increases appropriateness". Not "anthropomorphism is
harmful". The claim is that the two orderings are not the same ordering, which is
sufficient to establish that human-likeness cannot serve as a proxy for
appropriateness — and that is all the framework needs.

## 6. What follows for evaluation

If human-likeness is insufficient, evaluation needs properties that capture what
it misses:

- whether emotional content is **calibrated** to the situation → `E`
- whether the response **implies capacities it does not have** → `D`
- whether tone, certainty, and role **match the situation** → `F`

This is the derivation of `P = (H, E, D, F)` from the argument, rather than from
convenience.

## 7. The framework is about calibration, not rejection

PERSONA does not recommend minimising human-likeness. `H` appears in the profile
as a descriptive coordinate with no assumed direction. A response can be highly
human-like and highly appropriate; that combination is common and unremarkable.

The design implication is **calibration**: match anthropomorphic behaviour to
context, and avoid implying capacities the system lacks. It is worth noting that
[Cheng2025HumT] pairs its metric with a method for *reducing* human-like tone,
which is a stronger normative position than PERSONA takes. PERSONA's position is
that the right level of human-likeness is context-dependent and that no single
direction is correct across contexts.

## 8. Two ways this argument fails, stated in advance

**If `H` has almost no variance in the corpus,** a weak `H`-`OA` relationship is
uninformative — the argument would be untested rather than supported.

**If the dimensions that beat `H` turn out to be a single dimension,** the
finding is that appropriateness is carried by that channel, not that a
multidimensional profile is required. The argument in §6 would be only partly
vindicated: human-likeness would still be shown insufficient, but the proposed
replacement would be simpler than `P`.

Both possibilities are recorded here, before analysis, so that neither can be
handled by adjusting the argument after the fact.
