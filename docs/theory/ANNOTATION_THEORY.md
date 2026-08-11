# Annotation theory

Documents why the annotation is split into two groups and what the repository's
protocol actually specifies. All protocol details below are taken from
`data/clean_domains/*/rubric.md`. Nothing here is invented.

---

## 1. The two groups

**Group A — Overall Appropriateness.** Rates `OA` only. Sees the prompt and the
response. Never sees the `E`/`D`/`F` rubric.

**Group B — Dimensions.** Rates `E`, `D`, and `F`, plus assigns a
`scenario_type`. Works from the dimension rubric.

## 2. Why the separation is necessary

**To avoid circularity.** If the criterion is produced by the same person who
produced the predictors, in the same sitting, from the same rubric, then a
relationship between them may reflect the rater's internal consistency rather
than any property of the responses. The framework's central claim — that the
profile explains an independent judgment — requires that the judgment be
independent. Without separation, a large R² would be a fact about raters, not
about responses.

**To keep OA holistic.** `OA` must be free to include what the profile does not
cover: factual accuracy, safety, actionability. A rater who has just scored four
dimensions is primed to construct `OA` from them. The rubric instructs against
this explicitly — do not reconstruct a formula, do not average imagined E, D, and
F scores — but instruction is weaker than structural separation.

**To let OA disagree with the profile.** The scientifically interesting cases are
those where the dimensions and the holistic judgment diverge. A rater who has
seen both is less likely to produce them.

## 3. What the protocol specifies

The repository's protocol (`PERSONA-MH Human Annotation Protocol v3.1`) defines
the preferred design and a fallback design:

**Preferred design — separate rater pools.** The OA pool receives only the Phase
1 file and Phase 1 instructions and never receives the E/D/F rubric. The E/D/F
pool receives only the Phase 2 file. The same responses may be rated by both
pools, but *no person rates both*. The protocol states this "makes OA an
independently elicited criterion."

**Resource-constrained design — locked two-phase rating.** If separate pools are
not feasible, the same annotators may complete both phases under controls:

1. Phase 1 rates `OA` only, from prompt and response alone.
2. The Phase 1 file is submitted and **locked** before Phase 2 is received or
   opened.
3. `OA` may not be revised after `E`/`D`/`F` are rated.
4. A pre-specified washout interval is inserted before Phase 2 and reported.
5. Phase 2 assigns `scenario_type`, then rates `E`, `D`, `F` independently.

The protocol states plainly that this design "does not eliminate all same-rater
carryover. If used, report this limitation."

## 4. What the current release implemented — read this before writing the paper

**The released data implements the Group A / Group B separation.**

The cleaned data is organized accordingly:

- `oa_group_a.csv` contains holistic `OA` ratings from Group A.
- `anonymous_annotator_1.csv` through `anonymous_annotator_5.csv` contain
  Group B `E`, `D`, and `F` ratings.

The methodological consequence is important: `OA` is a separately elicited
holistic criterion and is not mathematically constructed from `E`, `D`, or `F`.
The central predictive analysis can therefore ask whether automated `H` and the
Group B profile dimensions explain a Group A criterion.

The paper should phrase this precisely:

> Group A rated overall appropriateness (`OA`) as a holistic criterion. Group B
> separately rated empathic appropriateness (`E`), anthropomorphic deception
> risk (`D`), and contextual fit (`F`). `OA` was not calculated from the profile
> dimensions.

**Provenance note.** The current clean release anonymizes the Group B files. The
data audit verifies score validity, duplicate annotations, rater counts per pool,
and HuMT join provenance. Rationale text should still be treated as rubric-coded
supporting text rather than independent qualitative evidence.

## 5. Why the dimension raters need a detailed rubric

`OA` is deliberately holistic — a rubric that decomposed it would defeat its
purpose. `E`, `D`, and `F` are the opposite: they are technical constructs whose
boundaries are precisely what the framework claims to have identified. Without
detailed anchors, raters would collapse them toward general quality, and the
separability the framework depends on would be lost at the point of measurement.

The `D` rubric carries the heaviest specification because it is the least
intuitive: a five-level severity ladder, a highest-severity-cue rule (no
accumulation across layers), a mandatory attribution rule (score only cues in the
AI's own voice, ignoring quoted speech suggested for the user and third-party
descriptions), and an explicit negative list — `D` is not raised for incorrect
advice, missed crisis lines, cold tone, medical inaccuracy, failure to answer,
recommending professional support, functional "I", or accurate AI
self-identification.

That negative list is the operational boundary between `D` and `F`/`OA` and
should be quoted in the paper. It is the clearest evidence that the constructs
were separated by design rather than by assertion.

## 6. Why calibration matters

The dimensions are not natural kinds. Whether a given phrase is "simulated
affect" (D=3) or "claimed feelings" (D=4) is a judgment that must be made
consistently. Calibration examples exist in the protocol (§12) precisely because
the ladder's steps are not self-evident.

## 7. Why inter-rater reliability matters

Reliability is the ceiling on validity: a dimension raters cannot agree on cannot
support conclusions about anything else. Reporting it per domain *and* per
dimension is necessary because reliability is a property of a construct in a
context, not a global property of a study — a rubric can work well for one
dimension and poorly for another.

The project uses ICC(A,k) as the primary inter-rater reliability statistic:
two-way mixed-effects, absolute-agreement, average-measures ICC. This matches the
annotation structure because multiple raters in each pool scored the same
responses and the analysis uses the averaged pool score. ICC(A,1) and
Krippendorff's ordinal alpha are reported as supplementary diagnostics.

**Comparison point.** [CounselBench2025], annotating adjacent constructs with 100
mental health professionals, reports Krippendorff's alpha at or above 0.7. That is
a reasonable external benchmark for what this rubric should aspire to, and the
paper should present its own coefficients against it rather than in isolation.

## 8. Protocol integrity

The `D` definition is marked **frozen** for the current annotation batch, with
change notes documenting the v3 redefinition (highest-severity-cue rule) and the
v3.1 addition (attribution rule). Any further change to `D` creates a
comparability break across batches and must be recorded in the protocol's change
log rather than applied silently.
