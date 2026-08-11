# Research questions

Four questions. Each carries an **answerability** verdict describing whether the
current corpus can address it, decided from the dataset's structure and *not*
from any result.

---

### RQ1

> To what extent does automated human-likeness predict independently judged
> conversational appropriateness?

**Answerable: yes.** `H` is available for every response in mental health and for
most responses in education and health; `OA` is available throughout.

**Interpretive constraint.** `H` in this corpus has very little spread. A weak
`H`-`OA` relationship under restricted predictor variance is not evidence that
human-likeness is irrelevant to appropriateness in general — it is evidence about
this range of this metric on this corpus. The paper must report the variance
alongside the relationship and must not upgrade a null into a general claim. See
`CLAIMS_AND_BOUNDARIES.md` §variance.

---

### RQ2

> Do empathy, deception risk, and contextual fit provide information about
> appropriateness beyond human-likeness alone?

**Answerable: yes**, and this is the framework's primary empirical question.

**Interpretive constraint.** "The profile beats `H` alone" and "the profile is
multidimensional" are different claims. If the increment over `H` is carried by
one dimension, RQ2 is answered affirmatively while the multidimensionality claim
is not supported. The analysis must therefore report per-dimension ablation, not
only the full-versus-baseline contrast, and the paper must state which of the two
claims the evidence supports.

---

### RQ3

> Do the relationships between anthropomorphic dimensions and overall
> appropriateness vary across interaction domains?

**Answerable: partially.** Three domains exist (mental health, education,
health), each with the same four dimensions and the same criterion, which
supports a formal interaction test.

**Constraints.**

- Domain is confounded with source dataset, prompt construction, and rating
  batch. A difference between domains is not necessarily a difference *caused by*
  domain.
- The three domains were annotated under related but separately authored rubrics.
  Scale meaning may not be identical across them.
- If any domain's criterion has severely restricted variance, that domain cannot
  contribute evidence of a *relationship*, and its inclusion in an interaction
  test may produce a difference that reflects measurement range rather than
  contextual norms.

The question should be framed as testing whether relationships differ, not as
demonstrating that context determines appropriateness. Numerical differences
between per-domain coefficients are not by themselves evidence of interaction.

---

### RQ4

> Under conditions that explicitly elicit anthropomorphic behaviour, can the
> framework distinguish appropriate human-like interaction from misleading
> anthropomorphic signalling?

**Answerable: NO — requires additional data.**

This verdict is structural and should not be softened.

The adversarial portion of the corpus derives from CounselBench-Adv
[CounselBench2025], whose expert-authored items are designed to trigger
**clinical** failure modes. The failure-mode labels in the repository are
`apathetic`, `assumptions`, `symptoms`, `judgmental`, `medication`, and
`therapy`. None of these elicits anthropomorphic behaviour. They elicit
dismissiveness, unwarranted inference, symptom mishandling, judgmental framing,
unauthorised medication advice, and inappropriate therapy direction.

An adversarial set that stresses clinical conduct is not an adversarial set that
stresses anthropomorphic signalling. Reporting `D` scores on it shows how the
dimension behaves under clinical stress — which is worth reporting — but it does
not answer RQ4.

Further, the corpus contains a **single system-prompt condition**. There is no
contrast between a condition that encourages anthropomorphic behaviour and one
that discourages it, so the manipulation RQ4 presupposes was never run.

**What RQ4 would require.** Prompts or system conditions designed to elicit
claims of feeling, memory, relationship, continuity, or authority; ideally paired
so that the same user situation appears under different anthropomorphic
conditions, holding content constant. Until such data exists, RQ4 belongs in
future work.

**Do not** re-describe the existing adversarial set as anthropomorphism-eliciting
in order to retain RQ4. It is a clinical stress test, its designers describe it as
such, and misdescribing it is the kind of claim a reviewer familiar with
CounselBench will catch immediately.

---

## Summary

| RQ | Answerable | Principal constraint |
|---|---|---|
| RQ1 | Yes | Restricted `H` variance limits generalisation |
| RQ2 | Yes | Must separate "beats H" from "is multidimensional" |
| RQ3 | Partially | Domain confounded with dataset and rubric; ceiling effects |
| RQ4 | **No** | Adversarial set targets clinical, not anthropomorphic, failure; single condition |
