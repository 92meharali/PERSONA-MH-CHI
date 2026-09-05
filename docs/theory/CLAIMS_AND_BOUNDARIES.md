# Claims and boundaries

What PERSONA may claim, what it may not, and what remains open. This document is
written to be read by a reviewer looking for overclaim.

**Status: PERSONA is not validated.** It is a proposed framework with an
in-progress empirical evaluation. No sentence in the paper should imply
otherwise.

---

## §normative — Appropriateness is normative and audience-relative

`OA` is what a specific small group of raters judged appropriate under a specific
rubric. It is not a fact about responses. A different rater population — clinicians,
patients, teachers, people from other cultural or linguistic backgrounds — could
produce a different criterion, and nothing in the framework identifies one as
correct.

Everything downstream inherits this. "The profile explains appropriateness" always
means "explains these raters' judgments."

## §annotators — Annotator population

Five raters per pool were recruited according to domain. Mental-health raters
were final-year psychology students with mental-health-relevant training,
general-health raters were MBBS students, and education raters were school
teachers and university teaching assistants. They were volunteers rather than
project-team annotators.

The pools provide domain-relevant judgment but do not represent licensed mental-
health clinicians, patients, or other affected end-user populations. This bounds
generalisation. [CounselBench2025] used 100 mental-health professionals for
adjacent constructs; the contrast should be stated rather than avoided.

## §independence — Criterion independence

The released data uses separate rater pools. Group A produced holistic `OA`;
Group B produced `E`, `D`, and `F`. This is the core anti-circularity control:
`OA` is separately elicited and not mathematically constructed from the profile
dimensions. See `ANNOTATION_THEORY.md` §4.

**Consequence:** a relationship between `P` and `OA` is not a formula artifact.
It remains a judgment-based empirical relationship and inherits the limitations
of small rater pools, domain expertise, rubric design, and response sampling.

## §variance — Restricted variance

Restricted variance in a predictor attenuates any relationship it can show;
restricted variance in the criterion caps what anything can explain. Where either
occurs, the correct statement is that the relationship is **untestable in this
range**, not that it is absent.

This applies specifically to `H` (narrow spread across all domains), to `D`
(concentrated near its floor outside the mental-health adversarial items), and to
`OA` in domains where consensus ratings cluster at the scale maximum. Actual
figures are in `analysis/outputs/tables/ceiling_floor.csv` and must be reported
alongside every relationship they bear on.

## §H — Limitations of the automated H measure

- HumT measures anthropomorphic **signalling**, not **perception**. No claim
  about what any reader inferred is licensed.
- It is single-turn and text-only.
- It is one operationalisation of a broader construct; where the construct is
  wider than the metric, results speak to the metric.
- It is computed by a language model and inherits that model's properties.
- A null result for `H` is a null for *this metric on this corpus*, not for
  human-likeness in general.

## §F-OA — Construct overlap between Domain Fit and OA

`F` (do content, action, tone, certainty, and role boundaries fit the
domain-specific situation) and `OA` (holistic suitability) are theoretically
related. A strong `F`-`OA` relationship is
therefore partly predicted by the definitions and is **weaker evidence for the
framework** than an equally strong `E`-`OA` or `D`-`OA` relationship would be.

If the profile's explanatory power concentrates in `F`, the honest reading is
that appropriateness judgments are carried by contextual calibration — not that
`P` has been validated as a multidimensional construct. Recorded in
`HYPOTHESES.md` H3 before analysis.

The final construct-relationship audit quantifies this boundary. `F`/`OA`
Spearman and Pearson associations are `.694/.809` in mental health, `.219/.756`
in education, and `.060/.242` in health. The education coefficient divergence
is consistent with concentrated, tied ordinal scores and separation among rare
lower-scoring observations; neither coefficient should be privileged as a
complete construct test. Transparent disagreement screens (`F >= 4` with
`OA <= 3`, or `F <= 3` with `OA >= 4`) identify one case in mental health, none
in education, and 43 in health; health also contains 33 cases with
`|F - OA| >= 2`. These observations support operational non-identity and
domain-dependent alignment. They do not establish complete discriminant
validity for single-item dimensions.

## §separability — Empirical separability is not established by definition

The four dimensions are conceptually distinct (`DISTINCTIONS.md`). Whether raters
*measurably* separated them is an empirical question answered by the correlation,
collinearity, and reliability analyses. Conceptual argument does not settle it,
and correlations alone do not establish construct validity.

In the current corpus, maximum profile-dimension VIF is 1.490 and the largest
pairwise profile-dimension Spearman association is below .50. This supports low
statistical redundancy among predictors, not a validated latent measurement
model.

## §singleturn — Single-turn evaluation

Every judgment concerns one prompt and one response. The properties `D` is most
concerned with — claimed memory, relational continuity, dependency — are
inherently multi-turn phenomena. A single turn can only capture the *signal* of
continuity ("I'll remember this"), never the behaviour. This is a structural limit
on `D`, and arguably the framework's largest measurement gap.

## §outcomes — Appropriateness is not an outcome

`OA` is a third-party judgment of a response. It is not a measure of whether a
user was helped, understood, or harmed. No inference to wellbeing, behaviour
change, or clinical benefit is licensed.

## §safety — Appropriateness is not safety

Overlapping, not identical. `OA` includes safety considerations; it does not
verify facts, and a response can be appropriate-as-judged and factually wrong.
PERSONA is not a safety evaluation and must not be described as one.

## §clinical — Appropriateness is not clinical effectiveness

`OA` says nothing about therapeutic outcome. This boundary needs stating
explicitly given the mental-health domain, where readers may otherwise assume
clinical relevance. [CounselBench2025] carries an explicit disclaimer against
endorsing LLMs in therapeutic practice; this project should carry an equivalent
one.

## §models — Model and version limitations

Three model families, at specific versions, at a specific time. Model behaviour
changes across versions. Findings are about these systems at this point, not
about LLMs generally.

## §language — Language and culture

English only. Anthropomorphic cues, warmth norms, and boundary expectations are
culturally variable, and neither the rubric nor the rater pool samples that
variation.

## §domains — Domain limitations

Three domains, each confounded with its source dataset, prompt construction,
rubric document, and rating batch. See `DOMAIN_THEORY.md` §4. Differences between
domains are differences between domain-plus-apparatus.

## §RQ4 — Adversarial elicitation does not exist in this corpus

The adversarial items target clinical failure modes, not anthropomorphic
behaviour, and there is one system-prompt condition. RQ4 and H5 are therefore
**NOT AVAILABLE — requires additional data**. See `RESEARCH_QUESTIONS.md` RQ4.

## §S — S is secondary

`S = (H + E − D + F) / 4` is an optional transparent scalar for benchmarking.

- `S` is **not** ground truth.
- `S` is **not** `OA`.
- `S` is **not** the contribution.
- `S` must **not** replace the profile.
- Equal weights are a transparent default, not a claim about importance.
- A scalar hides trade-offs: two responses with equal `S` can have opposite
  profiles, and that difference is what the framework exists to capture.

If `S` appears in the paper, it appears as a ranking convenience in a subsection,
never in the abstract's contribution statement.

---

## Claim ledger

| Claim | Category | Current status | Boundary |
|---|---|---|---|
| PERSONA is a coherent framework separating four properties | Supported by literature/theory | Argued conceptually in `PERSONA_THEORY.md`, `CONSTRUCT_DEFINITIONS.md`, and `DISTINCTIONS.md` | Conceptual separability is not construct validation |
| `OA` is elicited independently of the dimensions | Supported by repository design | Group A rated `OA`; Group B rated `E/D/F` | Still limited by small, domain-relevant rater pools |
| Human-likeness alone is insufficient to explain holistic appropriateness | Supported by current data and literature | `H_only` is weak by domain; full profile outperforms `H` in mental health and education | Do not claim all forms of human-likeness are useless |
| The multidimensional profile adds information beyond `H` | Supported by current data | Strong in mental health and education; pooled improvement positive | Health improvement is weaker and its interval crosses zero |
| `F` appears to be a major contributor in some domains | Supported by current data | Ablation and `F_only` models show `F` carries much of the mental-health and education signal | Do not claim `F` causes appropriateness |
| The profile dimensions are not redundant copies | Supported by current diagnostics | Pairwise correlations, VIF, and condition numbers do not show obvious redundancy | This supports separability, not full construct validity |
| Relationships differ by domain | Supported by formal audit | Domain interaction model estimates slope differences with uncertainty | R² differences alone are not evidence of interaction |
| Health provides equal-strength validation | Not supported / should not be claimed | Ceiling effects and uncertainty limit the health result | Treat as transfer/ceiling-case evidence |
| PERSONA distinguishes appropriate from misleading anthropomorphism under elicitation | Requires additional data | RQ4 is not answerable with the current corpus | Needs anthropomorphic elicitation or paired conditions |
| PERSONA is validated | Not supported / should not be claimed | The current archive supports a first empirical evaluation | Avoid final validation language until stronger external evidence exists |
