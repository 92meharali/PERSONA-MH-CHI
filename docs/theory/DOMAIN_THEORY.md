# Domain theory

Why mental health, education, and health, and what may and may not be inferred
from comparing them.

---

## 1. The theoretical claim

**Different domains impose different expectations around warmth, boundaries,
authority, certainty, and relational behaviour.**

This is the claim. It does **not** entail that any fixed weighting of `H`, `E`,
`D`, and `F` is universally correct, and PERSONA explicitly does not propose one.
The scalar `S` uses equal weights purely as a transparent default for ranking,
not as a claim about relative importance. See `CLAIMS_AND_BOUNDARIES.md` §S.

The claim generates an **empirical question**, not a conclusion: do the
relationships between dimensions and appropriateness actually differ across
domains? That is RQ3, and it is to be tested, not assumed.

## 2. Why these three domains

They vary along the axes the framework cares about, while sharing enough
structure to be comparable.

| | Mental health | Education | Health |
|---|---|---|---|
| Emotional load | High | Low to moderate | Moderate |
| Role-boundary stakes | High (clinical authority, therapeutic relationship) | Moderate (pedagogical authority) | High (medical authority) |
| Certainty expectations | Cautious; overconfidence harmful | Confident explanation often desirable | Cautious; overconfidence harmful |
| Relational continuity | Salient and risky | Sometimes desirable (tutoring) | Largely irrelevant |
| Warmth expectation | High | Moderate | Low to moderate |

The contrast that most directly probes the framework is **mental health versus
education on warmth and continuity**. In crisis support, emotional validation is
central and claimed personal relationship is a serious boundary problem. In
tutoring, sustained encouragement is pedagogically motivated and relational
continuity is closer to a design goal than a risk. If `E` and `D` relate to
appropriateness identically in both, the contextual thesis is weakened.

Authority calibration and unsupported expertise belong primarily to `F` or
`OA`. Under the final D scope clarification, professional language enters `D`
only when it enacts false human identity, relationship, or continuity.

**Health versus mental health** is a narrower contrast: similar authority stakes,
different emotional load. It functions as a partial control on the clinical-domain
properties.

## 3. Why not a single domain

A single-domain result cannot distinguish "these dimensions matter" from "these
dimensions matter *here*". Since the framework's thesis is that appropriateness is
contextual, a single-domain study would be self-undermining: it could not observe
the contextual variation it posits.

## 4. What comparison across these domains cannot show

**Domain is confounded.** The three domains differ in more than domain:

- **Source.** Mental health derives from CounselBench [CounselBench2025];
  education and health from separately constructed prompt sets.
- **Prompt construction.** Mental health includes expert-authored adversarial
  items; the others were built differently.
- **Rubric.** Each domain has its own rubric file. They share structure and
  anchor logic but are not identical documents, and scale meaning may not
  transfer exactly.
- **Rating batch.** Domains were annotated at different times and by different
  domain-relevant rater populations.

A difference between domains is therefore a difference between *domain-plus-its-
apparatus*. The paper may report that relationships differ across these three
settings; it may not claim that domain membership caused the difference.

**Measurement range can masquerade as domain difference.** If a domain's
criterion is concentrated near the top of its scale, relationships in that domain
are attenuated for reasons that have nothing to do with contextual norms. Before
interpreting any domain difference, the criterion's distribution in each domain
must be reported. A domain whose `OA` is at ceiling contributes evidence about
measurement, not about context.

## 5. What would strengthen the domain argument

- A domain with genuinely low warmth expectations and low authority stakes
  (technical support, information retrieval), to extend the range.
- Identical rubrics across domains, differing only in the scenario-specific
  guidance table.
- Prompt sets constructed by one procedure across domains, removing the source
  confound.
- Criterion distributions with usable variance in every domain.

These are future-work items, recorded here so that the current design's limits
are visible rather than discovered in review.
