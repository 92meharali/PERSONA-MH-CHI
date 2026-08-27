# PERSONA Manuscript Revision and Rebuttal Record

This document records each professor-raised critical issue, the research team's
decision, every resulting change, the affected files, and remaining work. It can
be shared with the supervising professor as a revision record, but it is not
manuscript text and should not be submitted as part of the paper.

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
- Group B dimension ratings were completed by members of the author team and
  research interns after they jointly reviewed and agreed upon the construct
  definitions, anchors, attribution rules, and detailed annotation procedure.
  Ratings were completed independently after annotation began.
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

## Critical Issue 3: Reproducibility and Data Reconciliation

### Concern

The manuscript did not name the predictive estimator or fully specify
preprocessing, tuning, grouping, seeds, scoring, and uncertainty procedures. It
also combined the released 415-response education and health counts with stale
language about larger HumT exports and did not explain why 415 responses map to
139 education and 140 health prompt clusters. Prompt provenance was described
inconsistently.

### Team-Confirmed Facts

- Education and health each contained 415 released responses from the outset.
- There was no larger annotated response corpus and no analysis attrition stage.
- Education contains 139 prompt clusters: 138 have three model responses and one
  has one response.
- Health contains 140 prompt clusters: 136 have three model responses, three
  have two responses, and one has one response.
- The estimator is ordinary least squares linear regression with an intercept.
- Education natural prompts were sourced and adapted from Bridge and MathDial.
- Health natural prompts were sourced and adapted from HealthBench.
- Education and health adversarial prompts were authored for this study.

### Implemented Changes

- Named OLS with an intercept in the manuscript and generated predictive report.
- Documented recorded-scale predictors, pooled domain indicators, and no
  regularization, imputation, feature selection, tuning, or outcome
  transformation.
- Documented five-fold prompt-grouped CV repeated 20 times, deterministic seeds
  42--61, mean out-of-fold R-squared, 1,000 prompt-cluster bootstrap resamples,
  and paired comparison intervals.
- Added exact prompt-cluster size distributions and stated that prompt groups
  remain intact in cross-validation.
- Removed filtering, attrition, and larger-precursor-corpus language.
- Reduced `humt_education.csv` and `humt_health.csv` to the 415 one-to-one HumT
  records belonging to each released corpus. No HumT score used in analysis was
  changed.
- Corrected prompt provenance and added primary Bridge, MathDial, and HealthBench
  citations.
- Updated the current manuscript, older manuscript copy, analysis code,
  generated reports, domain documentation, claims boundaries, risk register,
  changelog, and TODO list.

### Unchanged Items

- Dataset sizes remain 660 mental-health, 415 education, and 415 health
  responses, totaling 1,490.
- Prompt-cluster counts remain 220, 139, and 140, totaling 499.
- No released response, human rating, or analysis-used HumT score changed.
- Predictive specifications and all reported statistical results remain
  unchanged.

### Status

Implemented and verified on 2026-08-25. The data-build, HumT-provenance, and
predictive phases regenerated successfully. All headline result tables remained
byte-for-byte unchanged, both HumT files and audits now report 415/415 rows, and
source, Python syntax, LaTeX structure, citation, and stale-reference checks
passed. Local PDF compilation remains pending because no LaTeX compiler is
installed.

## Critical Issue 4: Construct Validity, Contextual Fit Versus OA

### Concern

Contextual fit (`F`) and overall appropriateness (`OA`) are conceptually
adjacent, and the strong F-only predictive results in mental health and
education could be interpreted as definitional overlap. The prior manuscript
described the distinction but did not present a direct, complete relationship
audit or concrete disagreement cases.

### Team Decision

- Retain `F` because the framework evaluates the full response profile and the
  central claim is that human-likeness alone is insufficient.
- Define `F` narrowly as contextual calibration of content, action, tone,
  certainty, and role; retain `OA` as the separate holistic judgment of
  suitability, safety, helpfulness, and responsibility.
- Evaluate the relationship directly using both rank and linear associations,
  transparent disagreement screens, and predictor-redundancy diagnostics.
- Claim operational distinction and domain-dependent empirical alignment, not
  complete psychometric discriminant validity.
- Do not add CFA or HTMT because H, E, D, F, and OA are single-item dimensions,
  not multi-item latent scales.

### Implemented Analysis Changes

- Added `construct_relationships.csv` with all H/E/D/F associations with OA,
  including Spearman rho, 95% prompt-cluster bootstrap intervals, and Pearson r.
- Added `f_oa_disagreement.csv` with three fixed post-analysis screens: `F >= 4` and
  `OA <= 3`; `F <= 3` and `OA >= 4`; and `|F - OA| >= 2`.
- Added `f_oa_disagreement_examples.csv` so observed patterns remain traceable
  to response IDs, scenario types, profile scores, and response excerpts.
- Added all three tables to the Phase 3 JSON and generated report.
- F/OA Spearman/Pearson results are .694/.809 in mental health, .219/.756 in
  education, and .060/.242 in health.
- Mental health has one low-F/high-OA case and no gap of at least two points.
  Education has no threshold disagreement. Health has one high-F/low-OA case,
  42 low-F/high-OA cases, and 33 gaps of at least two points.

### Implemented Manuscript Changes

- Added one abstract sentence summarizing domain-dependent F/OA alignment.
- Added an analysis commitment to report profile/OA associations,
  disagreements, and collinearity rather than infer distinctness from
  definitions or separate rater pools.
- Added a 12-row construct-relationship table covering H, E, D, and F in all
  three domains.
- Added the exact F/OA coefficients, bootstrap intervals, disagreement
  thresholds, counts, and percentages.
- Added two concise health examples showing opposite directions of F/OA
  disagreement: unsafe-antibiotic refusal (F=2.6, OA=5.0) and an
  emergency-headache response (F=4.0, OA=2.6).
- Explained that education's smaller Spearman but larger Pearson coefficient is
  consistent with tied, concentrated ordinal scores and separation among rare
  lower-score observations, without presenting that explanation as causal.
- Replaced the Discussion's generic overlap argument with direct evidence and
  the conclusion that F is operationally narrower but strongly aligned with OA
  in mental health and education.
- Clarified that low VIF, disagreements, separate rater pools, and correlations
  do not jointly prove complete psychometric discriminant validity.
- Revised future-validation language to prioritize multi-item measures,
  alternative OA criteria, controlled manipulations, other rater populations,
  and multitrait-multimethod designs.

### Supporting-Document Changes

- Updated `analysis/README.md` to enumerate the new Phase 3 diagnostics.
- Added the exact correlations and disagreement counts to
  `docs/RESULTS_GROUND_TRUTH.md`.
- Added empirical F/OA evidence to `CONSTRUCT_DEFINITIONS.md` and
  `CLAIMS_AND_BOUNDARIES.md`.
- Updated `CLAIMS_AUDIT.md` to mark operational distinction as supported with a
  psychometric qualification and complete discriminant validity as not
  supported or claimed.
- Updated `REVIEWER_RISK.md` with the expanded mitigation and remaining
  single-item measurement limitation.
- Recorded every change in `PAPER_REVISION_CHANGELOG.md` and marked this issue
  completed in `PAPER_TODOS.md`.

### Unchanged Items

- No dataset, annotation, response, HumT score, rubric, or rater record changed.
- No predictive model, fold, estimator, bootstrap, reliability estimate,
  ablation, domain interaction, or headline performance result changed.
- No pre-existing Phase 3 result table or figure changed.
- The paper does not claim that F and OA are statistically independent, that F
  is unimportant, or that PERSONA is a validated universal psychometric scale.

### Status

Implemented and verified on 2026-08-25. Phase 3 regenerated successfully; the
numeric and response-example trace audit passed; all pre-existing Phase 3 tables
and figures remained unchanged; Python syntax, source formatting, LaTeX
environment balance, references, and citations passed. Local PDF compilation
remains pending because no LaTeX compiler is installed.

## Major Issue 4.2: Scope of D and Professional Authority

### Concern

The v3.1 D anchor listed professional authority alongside feelings,
relationships, identity, memory, continuity, and dependency. Standalone
expertise or capability misrepresentation is not necessarily anthropomorphic,
so the health D result could have reflected unsafe medical authority rather than
anthropomorphic misleading implication.

### Team Decision

- Keep the construct name Anthropomorphic Deception/Misleading-Implication Risk.
- Align its scope with DeVrio et al.'s linguistic taxonomy rather than broaden
  it to generic misleading self-presentation.
- Count professional-role language only when the AI presents itself as a human
  professional or enacts a professional relationship or continuity it does not
  possess.
- Assign unsupported expertise, excessive certainty, unsafe advice, and factual
  error without anthropomorphic self-presentation to F or OA, not D.
- Preserve all original v3.1 scores and document the revision as a scope
  clarification rather than pretending annotators received a different scale.
- Leave the approved score-template rationales unchanged.
- Remove the confirmed junk synthetic-annotation text from health
  `annotator_notes` while preserving the column and shared schema.

### Implemented Analysis Changes

- Added `analysis/d_scope_audit.py` as a reproducible Phase 5b audit.
- Added `d_scope_response_audit.csv`, which traces all 23 health responses with
  consensus D >= 3 to a fixed post-analysis cue-family classification.
- Added `d_scope_sensitivity.csv` and `d_scope_audit.md`.
- The inspection identifies 22 affective/relational-led responses and one
  clinician-identity/continuity-led response.
- D-only health CV R2 is .241 in the complete corpus, .208 after removing the
  clinician-role response, and .192 after removing its full prompt cluster.
- Removing all 34 `other` scenarios reduces D-only CV R2 to .022, demonstrating
  that the health signal is concentrated in the relational adversarial subset.
- The cue-family inspection is explicitly labeled post-analysis and does not
  create a new human-rated subtype variable.

### Implemented Manuscript Changes

- Replaced standalone authority language in the D definition with false human
  professional identity, enacted professional relationship, or continuity.
- Added the explicit boundary that unsupported expertise, certainty, unsafe
  advice, and factual error belong to F or OA without anthropomorphic
  self-presentation.
- Connected D directly to DeVrio et al.'s categories involving understanding,
  identity, relationships, emotions, intention, and recall.
- Revised the framework table and attribution explanation.
- Replaced the prior health interpretation about expertise, certainty, and
  authority with the response-inspection and sensitivity findings.
- Preserved the conclusion that health evidence is exploratory.

### Rubric and Theory Changes

- Added the same final scope clarification to `data/annotation_protocol.md` and
  the mental-health, education, and health rubrics.
- Updated construct definitions, distinctions, PERSONA theory, domain theory,
  hypotheses, literature map, research questions, and the human-likeness
  argument.
- Updated the claims audit and reviewer-risk register with the resolved boundary
  and remaining subtype limitation.

### Metadata Cleanup

- Blanked only the obsolete `annotator_notes` values in the five health
  annotator files.
- Retained the `annotator_notes` column so all domain CSVs preserve their shared
  schema.
- Verified all 415 rows in each file and confirmed that every field except
  `annotator_notes` is identical to the committed pre-cleanup version.

### Unchanged Items

- No original annotation score or rationale changed.
- No response, prompt, scenario, model, HumT value, or identifier changed.
- No original D subtype rating exists; the new cue-family audit is explicitly
  post-analysis.
- No headline prediction, reliability, ablation, interaction, correlation, or
  distribution result changed.

### Status

Implemented and verified on 2026-08-25. The complete Phase 1--5b pipeline
regenerated successfully. All pre-existing processed datasets, result tables,
reports, and figures remained byte-identical. The metadata-preservation audit
confirmed that only `annotator_notes` changed in the five health CSVs. Python,
CSV schema, numeric trace, source-formatting, LaTeX-structure, reference, and
citation checks passed. Local PDF compilation remains pending because no LaTeX
compiler is installed.

## Professor Review Follow-up: `kinda_final.tex`

### Scope

Following review of the compiled 19-page draft against the professor's complete
revision checklist, the manuscript was updated as `paper/kinda_final.tex`. This
follow-up corrects a reliability-table transcription problem, completes several
requested reporting additions, and improves examples and presentation. It does
not change the dataset, annotations, analysis pipeline, or generated results.

### Critical Items

#### Reliability Table: Resolved

The reviewed PDF contained incorrect supplementary reliability values in its
expanded table. Most importantly, it reported health E as ICC(A,k) = .992,
ICC(A,1) = .961, and ordinal alpha = .959, which did not match the generated
analysis output.

The table in `kinda_final.tex` was replaced directly from
`analysis/outputs/tables/reliability.csv`. The corrected health E values are
ICC(A,k) = .939 with 95% CI [.928, .948], ICC(A,1) = .754, and ordinal alpha =
.667. The remaining ICC(A,1) and alpha values were likewise reconciled with the
generated table. The education E values remain ICC(A,k) = .997, ICC(A,1) =
.985, and alpha = .988.

#### Institutional Determination: Pending

The manuscript accurately states that the study did not receive prospective
institutional ethics review and does not claim approval or exemption. A written
institutional determination remains pending. Its actual outcome and timing must
be added when received; it must not be described as retrospective approval.

#### Anonymous Supplementary Package: Pending

The manuscript uses the anonymous ACM review format and no longer directs
reviewers to the public repository. Before submission, the supplementary package
must still be checked for author names, institutional details, repository URLs,
usernames, acknowledgments, file metadata, and discoverable folder names.

### High-Priority Reporting Changes

- Removed the ambiguous statement that education and health were "pre-filtered
  prior to sampling." The manuscript now states that the attrition table begins
  with the final prompt packs and reports zero API failures, post-generation
  exclusions, HumT failures, and incomplete annotation rows.
- Clarified rater composition. Group A consists of the domain-relevant pools
  already documented: psychology students, MBBS students, teachers, and teaching
  assistants. Group B consists of members of the author team and research
  interns who agreed upon the rubric and detailed process before independently
  rating E, D, and F. No rater contributed to both OA and E/D/F.
- Added the exact generation endpoints available in the repository:
  `gpt-5.6-sol` through the OpenAI Responses API,
  `anthropic/claude-opus-4.8` through the OpenRouter Chat Completions API, and
  `z-ai/glm-5.2` through the OpenRouter Chat Completions API.
- Did not invent generation access dates because the repository does not
  preserve defensible dates for every endpoint. This remains a metadata gap to
  resolve only if contemporaneous records are located.
- Standardized all active manuscript uses of the metric name to `HumT`.

### HumT and the Generic-Quality Question

The manuscript now explains the HumT mechanism more precisely. HumT is an
LLM-based linguistic metric, but it is not an LLM judge of response quality. It
compares the relative probability of text under animate and inanimate reporting
frames, such as "he or she said" versus "it said." Pronouns, conversational
phrasing, and related linguistic cues may affect this attribution; helpfulness,
safety, and overall response quality are not its targets.

This clarification strengthens the interpretation of H as a style-focused
baseline, but it does not create or substitute for an independent generic
response-quality control. The team therefore retains the previously approved
narrow framing: the H-only comparison quantifies OA-associated information
omitted by reliance on H alone and is not claimed as universal incremental
validity over every quality baseline.

### Examples and Presentation Changes

- Removed the defensive sentence that called the examples "interpretive
  illustrations rather than additional statistical tests."
- Expanded the example-table caption to spell out H, E, D, F, and OA; state that
  E/D/F/OA are means across five raters; and confirm that the final corpus has no
  missing ratings.
- Added a traceable matched education pair from the same active-exam prompt. One
  response supplies the answer (H = .146, E = 1.0, D = 1.0, F = 1.0, OA = 1.0),
  while the comparison response refuses and offers the power rule (H = .065,
  E = 2.0, D = 1.0, F = 4.0, OA = 4.0).
- Removed the secondary composite profile score, which was not required by an
  RQ and introduced an unnecessary additional aggregation.
- Replaced the oversized three-bar model figure with a compact model/mean-OA
  table.
- Increased the ablation figure to the full available line width.
- Revised the Results overview to foreground the domain-specific calibration
  finding before walking through the RQs.
- Moved domain-specific calibration to the opening of the Discussion, followed
  by the narrower conclusion that human-likeness is useful but insufficient.

### Unchanged Analysis and Data

- No response, prompt, score, rationale, annotator record, HumT value, model
  output, or identifier changed.
- No estimator, preprocessing step, fold assignment, bootstrap procedure,
  reliability computation, predictive result, ablation result, interaction,
  correlation, or sensitivity result changed.
- The reliability edit corrects manuscript transcription against the generated
  source table; it does not recalculate or selectively alter reliability.
- The matched example uses existing processed-dataset rows and reported means.

### Remaining Editorial Work

- Incorporate the written institutional determination when received.
- Complete the anonymous supplementary-package audit.
- Normalize and alphabetize the complete reference list and author-name style.
- Add model access dates only if contemporaneous records can verify them.
- Recompile `kinda_final.tex` on Overleaf and inspect table placement, figure
  readability, page count, references, and line wrapping.
- Conduct a final concision pass after compilation; the latest content additions
  should be balanced against repeated caveats and non-central explanation.

### Status

Implemented in `paper/kinda_final.tex` and pushed in commit `a261421` on
2026-08-27. Source-level checks confirmed balanced environments, unique labels,
resolved internal references, corrected reliability values, and no active
`HumT` spelling. Local PDF compilation remains unavailable; Overleaf rendering
and the two external critical items above remain pending.
