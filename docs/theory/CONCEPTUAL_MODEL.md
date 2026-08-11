# Conceptual model

```
                    CONTEXT
     user situation + domain + interaction purpose
                       |
                       v
                  AI RESPONSE
                       |
                       v
       OBSERVED ANTHROPOMORPHIC PROPERTIES
                       |
        +--------+-----+-----+--------+
        |        |           |        |
        v        v           v        v
        H        E           D        F
   human-    empathic    deception  contextual
   likeness  approp.      risk        fit
   (auto)    (human)     (human)    (human)
        |        |           |        |
        +--------+-----+-----+--------+
                       |
                  [ evaluated against ]
                       |
                       v
          INDEPENDENT HUMAN JUDGMENT
                       |
                       v
                       OA
             overall appropriateness
```

## Reading the diagram

**Context is prior.** The same response text is a different object in a crisis
than in a casual check-in. `F` is defined relative to context by construction,
and `OA` is elicited with the prompt visible. Only `H` is context-free — it is
computed from the response alone. That asymmetry is deliberate and is what makes
`H` a descriptive baseline rather than a judgment.

**The four dimensions are parallel, not sequential.** No dimension feeds another.
`D` is not computed from `H`; `E` is not a component of `F`. They are four
readings of one artefact.

**`OA` is not downstream of the dimensions.** The vertical arrow means "evaluated
against", not "produced by". This is the whole point: `OA` arrives from a
separate judgment process, and the empirical question is how well the dimensions
account for it. If `OA` were derived from the dimensions, the arrow would be
computation and the study would be arithmetic.

**Everything here is single-turn.** One prompt, one response, one set of
judgments. Nothing in the model represents conversation history, user state over
time, or outcomes.

## What the model claims

That there exist **observable interactional properties of responses** which
**relate systematically to human judgments of appropriateness**, and that those
properties are **not reducible to human-likeness**.

## What the model does not claim

- **Not objective morality.** `OA` is what these raters judged, under this
  rubric, in this domain. Appropriateness is treated as normative and
  audience-relative throughout. A different rater population could produce a
  different criterion, and the framework has no basis for calling one correct.
- **Not causation.** The model describes association between response properties
  and judgments. It does not establish that changing `D` would change how a real
  user is affected.
- **Not user experience.** `OA` comes from third-party raters evaluating
  responses, not from the people who asked the questions. Third-party judgment of
  appropriateness and first-person experience of receiving a response are
  different things, and the gap between them is unmeasured here.
- **Not outcomes.** Nothing connects any of these quantities to whether a person
  was helped.

## Where the model is most vulnerable

The arrow from response to dimensions assumes the four properties are separately
observable. If raters cannot reliably distinguish them — if, say, `F` and `OA`
are read as the same question in different words — then the profile is not four
readings but fewer. This is an empirical matter, tested by the separability and
reliability analyses, and the theory does not settle it. See
`CLAIMS_AND_BOUNDARIES.md` §separability.
