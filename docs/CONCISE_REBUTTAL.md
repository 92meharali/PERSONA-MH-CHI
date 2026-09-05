# Concise Response to Professor Feedback

## 1. Ethics and Annotator Documentation

**Concern.** The manuscript did not sufficiently explain ethics status,
annotator recruitment and qualifications, consent, voluntary participation,
withdrawal rights, independence, AI-use boundaries, or safeguards for sensitive
content.

**What we implemented.** We added a transparent ethics statement and complete
annotator documentation. The manuscript now explains the domain-relevant rater
backgrounds, separate rating groups, two-week annotation period, informed
consent, voluntary participation, withdrawal rights, independent work, limited
AI-use policy, anonymization, and sensitive-content safeguards. We also
corrected the health ratings to be described as human annotations rather than
oversight or adjudication. We also confirmed that PERSONA is a sub-study under a
broader university EIRB-approved project, with approval dated 12 February 2026,
and added this status using wording that preserves the parent-project scope.

## 2. Strength of the H-Only Comparison

**Concern.** Comparing human-likeness alone with a richer multidimensional
profile could appear near-tautological or be interpreted as overly strong
predictive validation.

**What we implemented.** We retained the comparison because the central claim
is that human-likeness is useful but insufficient, but narrowed its
interpretation. The analysis now quantifies appropriateness-relevant information
omitted by human-likeness alone. Claims of universal superiority, unique
incremental validity, and complete psychometric validation were removed. The
research questions and conclusions now emphasize explanatory value, diagnostic
contributions, and domain-specific calibration.

## 3. Reproducibility and Data Reporting

**Concern.** The estimator, preprocessing, cross-validation, uncertainty
procedure, prompt grouping, dataset counts, and prompt provenance required more
precise documentation.

**What we implemented.** We specified ordinary least-squares regression with an
intercept, predictor handling, pooled domain indicators, the absence of
imputation or tuning, prompt-grouped five-fold cross-validation repeated 20
times, deterministic seeds, and 1,000 prompt-cluster bootstrap resamples. We
also reconciled all dataset and prompt-cluster counts, clarified prompt sources,
and confirmed that all 1,490 responses have complete ratings and human-likeness
measurements.

## 4. Domain Fit and Overall Appropriateness

**Concern.** Domain fit and overall appropriateness are conceptually close,
and the strong domain-fit results could reflect construct overlap.

**What we implemented.** We clarified that domain fit is a focused judgment of
content, action, tone, certainty, and role boundaries within a bounded domain,
whereas overall appropriateness is a holistic judgment of suitability, safety,
helpfulness, and responsibility. We added rank and linear
associations, disagreement cases, and collinearity diagnostics. The manuscript
now claims operational distinction and domain-dependent alignment, not complete
discriminant validity. It explicitly acknowledges that domain fit carries
most of the predictive signal in mental health and education.

## 5. Scope of Deception Risk

**Concern.** Professional authority could be mistaken for anthropomorphic
deception even when no human identity or relationship is implied.

**What we implemented.** We narrowed deception risk to misleading
anthropomorphic implications in the AI's own voice, including false human
professional identity, relationship, memory, emotion, or continuity. Unsupported
expertise, excessive certainty, unsafe advice, and factual error without such
self-presentation are assigned to domain fit or overall appropriateness.
The construct is now explicitly grounded in DeVrio et al.'s linguistic taxonomy.

## 6. Reliability and Statistical Accuracy

**Concern.** Some reliability values in the manuscript did not match the
generated statistical results.

**What we implemented.** We reconciled the complete reliability table directly
with the analysis outputs and corrected the affected values. The manuscript now
reports average-measures and single-rater ICCs with ordinal alpha consistently.
No ratings, datasets, analytical procedures, or generated results were altered.

## 7. Results and Presentation

**Concern.** The results required clearer research-question alignment, stronger
domain interpretation, more traceable examples, and less visually inefficient
presentation.

**What we implemented.** We reorganized the results around the three research
questions, foregrounded domain-specific calibration, added a matched same-prompt
example, improved table explanations, removed an unnecessary composite score,
and simplified the model comparison. Mental health remains the primary result,
education provides transfer evidence, and the ceiling-restricted health result
is presented as exploratory and statistically uncertain.

## 8. Length and Submission Compliance

**Concern.** The manuscript appeared long in the required single-column review
format, and the abstract exceeded the venue limit.

**What we implemented.** We verified that the main-text length is within the
venue's encouraged range and clarified that the single-column format naturally
produces a longer page count. The abstract was reduced below 150 words while
retaining the framework, sample, rating design, headline findings, health
qualification, and central conclusion.

## 9. Context, Domains, and Terminology

**Concern.** The manuscript treated context and the three evaluated domains as
interchangeable, and the construct name obscured the bounded operational
settings.

**What we implemented.** We now distinguish macro-level context from mental
health, education, and general health as bounded analytical domains. The
manuscript reports `F` as Domain Fit while preserving the original rubric's
content, action, tone, certainty, and role-boundary criteria. The frozen rubrics
record that annotators saw the label Contextual Fit and that no anchor or rating
changed.

## 10. Context-Aware and Philosophical Grounding

**Concern.** The framework needed stronger theoretical grounding for why
appropriateness varies by situation.

**What we implemented.** We added Dey's operational account of context,
Dourish's interactional critique, and the Aristotelian distinction between
*episteme* and *phronesis*. The latter is explicitly a conceptual lens, not a
measurement claim: HumT measures linguistic human-likeness rather than factual
knowledge, and PERSONA does not claim to measure or confer practical wisdom.

## 11. Human-Likeness Measurement Scope

**Concern.** Weak H-only prediction could partly reflect limited observed HumT
dispersion rather than a universal failure of human-likeness measures.

**What we implemented.** We added this qualification to the discussion and
limited the finding to the current HumT operationalization. Multi-metric and
human-rated human-likeness measures are identified as future validation work.

## Overall Outcome

The revised manuscript makes a narrower and more defensible contribution:
human-likeness remains a useful descriptive signal, but it is not sufficient for
evaluating context-sensitive appropriateness. The framework provides a
diagnostic profile of empathy, misleading anthropomorphic implications, and
domain fit, with its strongest evidence in mental health and education. The remaining
external task is the final anonymous supplementary-material audit.
