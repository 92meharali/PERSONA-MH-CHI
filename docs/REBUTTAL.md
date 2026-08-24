# PERSONA Manuscript Revision and Rebuttal Record

This internal document records each professor-raised critical issue, the research
team's decision, every resulting change, the affected files, and remaining work.
It is not manuscript text and should not be submitted as part of the paper.

## Critical Issue 1: Ethics and Annotator Documentation

### Concern

The manuscript and repository did not adequately document ethics status,
consent, recruitment, annotator qualifications, voluntary participation,
withdrawal rights, annotation duration, independent work, AI-use boundaries, or
sensitive-content safeguards. The repository also incorrectly described health
ratings as oversight or adjudication data.

### Team-Confirmed Facts

- No prospective ethics review had been obtained at the time of revision.
- Annotators gave consent and participated voluntarily.
- Mental-health annotators were final-year psychology students with
  mental-health-relevant training.
- General-health annotators were MBBS students.
- Education annotators were school teachers and ITU teaching assistants.
- Annotators had two weeks to complete the work.
- Annotators could withdraw; none withdrew, and all completed the study.
- Annotators worked independently.
- Annotators were instructed not to use AI to assign scores or write rationales.
  AI could be used only to clarify material they did not understand.
- Sensitive-content considerations were included in study procedures.
- Health ratings are human annotations, not LLM oversight or adjudication.
- Annotators will be acknowledged in the non-anonymous paper after acceptance,
  subject to consent and venue requirements.

### Implemented Changes

- Added a canonical ethics and annotator provenance record at
  `docs/ETHICS_AND_ANNOTATOR_PROVENANCE.md`.
- Added consent, voluntary participation, withdrawal rights, two-week timing,
  independent annotation, AI-use boundaries, and sensitive-content safeguards
  to the manuscript and repository documentation.
- Corrected mental-health qualifications from generic medical-student wording to
  final-year psychology students with relevant training.
- Removed the word "unpaid" and retained only "voluntary participation."
- Corrected health provenance throughout the repository from
  oversight/adjudication language to independent human annotation.
- Added an urgent TODO to obtain a written institutional ethics determination
  and report its actual status and timing without presenting it as retrospective
  approval.
- Added a future acknowledgment TODO for consenting annotators.

### Affected Files

- `paper/revised3.tex`
- `docs/ETHICS_AND_ANNOTATOR_PROVENANCE.md`
- `docs/CLAIMS_AUDIT.md`
- `docs/REVIEWER_RISK.md`
- `docs/PAPER_TODOS.md`
- Repository files containing outdated health-provenance wording

### Status

Implemented and pushed in commits `68d538c` and `bd9ac79`. Institutional ethics
determination remains pending and must be incorporated when received.

## Critical Issue 2: Near-Tautological H-Only Versus Full-Profile Comparison

### Concern

The old framing treated better performance from the richer `H+E+D+F` model as
"predictive validity" and as evidence that the full framework improves on
human-likeness. Because the richer model contains several variables designed to
relate to appropriateness, that framing could be read as near-tautological and
as a stronger validation claim than the analysis supports.

### Team Decision

- Retain H-only versus full-profile analysis because the paper's central claim
  is that human-likeness is useful but insufficient.
- Interpret the comparison as quantifying appropriateness-relevant information
  omitted when evaluation relies on H alone.
- Use ablations to diagnose which dimensions carry the available signal.
- Do not claim superiority over every alternative response-level evaluation
  baseline.
- Do not claim unique incremental validity or a fully validated universal
  psychometric instrument.
- Do not collect or introduce a generic response-quality variable in the current
  revision.
- Keep all current analyses and numerical outputs unchanged.

### Revised Research Questions

1. **RQ1: Sufficiency of human-likeness.** To what extent does automated
   human-likeness diverge from domain-relevant judgments of overall
   appropriateness?
2. **RQ2: Diagnostic explanatory value.** What appropriateness-relevant
   information do empathic appropriateness, misleading-implication risk, and
   contextual fit provide that human-likeness alone omits?
3. **RQ3: Domain-specific calibration.** How do the relative contributions of
   empathic appropriateness, misleading-implication risk, and contextual fit
   vary across mental health, education, and general health?

### Exact Manuscript Changes

- Rewrote the abstract to describe OA-associated variation captured by an
  informationally richer profile rather than validation through improved
  prediction.
- Added the ablation finding to the abstract: F carries most available signal in
  mental health and education, while D is strongest within the restricted health
  OA range.
- Removed the stale commented-out alternative abstract.
- Replaced "authentic empirical test" with a narrower statement that separate
  rater pools make the out-of-sample comparison empirical rather than a
  mathematical identity.
- Replaced all three research questions with the approved wording above.
- Replaced the contribution claim about the profile being "substantially more
  predictive" with a contribution about quantifying omitted information and
  identifying the dimensions that carry it.
- Replaced "Predictive validity" in the Analysis Plan with "Predictive
  comparison" and defined its omitted-information purpose.
- Replaced "incremental validity" with "added explanatory performance beyond
  H" in paper-facing prose.
- Replaced "incremental gains" with "gains over the H-only baseline."
- Added `Results Overview` and reordered the section as RQ1, RQ2, RQ3,
  measurement reliability, distributional constraints and robustness, and
  model-level descriptives.
- Renamed "Human-Likeness Alone Is Weak" to "RQ1: Human-Likeness and
  Appropriateness Diverge."
- Renamed "The Full Profile Improves Prediction" to "RQ2: What Human-Likeness
  Alone Omits."
- Combined ablation and domain-difference evidence under "RQ3: Diagnostic
  Contributions Vary by Domain."
- Revised Figure 2 and cross-validation table captions to avoid validation or
  superiority language.
- Added an explicit sentence that the gains quantify omitted information and do
  not establish universal construct validity.
- Inserted the approved health interpretation verbatim in substance: within the
  restricted OA range, D is strongest and F contributes comparatively little;
  this is exploratory domain-contingent calibration, not a definitive reversal.
- Renamed reliability to "Measurement Reliability" and moved it after the RQs.
- Combined ceiling/floor effects and VIF under "Distributional Constraints and
  Robustness," with VIF as "Predictor Collinearity Diagnostics."
- Renamed and moved the model comparison to "Model-Level Descriptives" at the
  end of Results.
- Fixed the missing space after the 499-prompt-cluster sentence.
- Reframed grouped validation in Discussion as an out-of-sample explanatory
  comparison that provides stronger empirical evidence than in-sample
  correlation without establishing causality or universal validity.
- Replaced "current validated profile" with "current profile."
- Added the future-work sentence: "Future work should also compare PERSONA with
  alternative response-level evaluation baselines and evaluator populations."
- Reframed the conclusion's "predictive gains" as "added explanatory
  performance over the H-only baseline."

### Supporting-Document Changes

- Updated `docs/theory/RESEARCH_QUESTIONS.md` with the approved RQs and explicit
  interpretive boundaries.
- Updated `docs/theory/PAPER_ARGUMENT.md` so the empirical questions and framing
  rules match the revised paper.
- Updated `docs/CLAIMS_AUDIT.md` to describe omitted information and record that
  universal baseline superiority is not tested or claimed.
- Updated `docs/REVIEWER_RISK.md` with the asymmetric-baseline risk, mitigation,
  and residual limitation.
- Updated `docs/PAPER_TODOS.md` to mark this critical issue completed.
- Updated `docs/PAPER_REVISION_CHANGELOG.md` with the complete revision record.

### Unchanged Items

- No dataset was edited.
- No analysis script was edited.
- No pipeline was rerun.
- No model specification, cross-validation fold, bootstrap procedure, estimate,
  confidence interval, table value, or figure file was changed.
- The manuscript title was not changed.

### Status

Implemented and verified on 2026-08-25. The numerical-token audit confirmed that
all active manuscript numbers were preserved; LaTeX environment and reference
checks passed. A local PDF compile was not possible because no LaTeX compiler is
installed, so the existing Overleaf compilation TODO remains open.
