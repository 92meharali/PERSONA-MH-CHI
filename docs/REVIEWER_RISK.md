# Reviewer Risk Register

## Critical

| Risk | Problem | Why reviewer may care | Manuscript response | Residual limitation |
|---|---|---|---|---|
| F/OA overlap | Contextual fit and overall appropriateness are conceptually adjacent. | A reviewer may argue high F prediction is partly definitional. | The manuscript now defines their operational boundary, reports all H/E/D/F associations with OA using Spearman and Pearson coefficients, audits transparent disagreement thresholds, gives concrete counterexamples, and limits the claim to operational distinction and statistical non-redundancy. | The single-item dimensions do not establish complete psychometric discriminant validity; strong mental-health and education alignment remains substantively important. |
| Asymmetric baseline comparison | The richer profile is compared with H alone, so a performance gain is expected when OA-associated predictors are added. | A reviewer may interpret the comparison as near-tautological or as an unsupported superiority claim. | RQs, analysis, results, and discussion now frame the comparison as quantifying information omitted by H alone; ablations identify which dimensions carry it. | The study does not compare PERSONA with every alternative response-level evaluation baseline. |
| Reproducibility and count reconciliation | The estimator and variable prompt-level model coverage were previously underreported, while stale HuMT-export language implied a larger precursor corpus. | Unexplained counts and modeling choices undermine reproducibility. | Methods now name OLS and all preprocessing, CV, seed, scoring, and bootstrap choices; corpus documentation consistently reports the original 415-response releases and their prompt-cluster sizes. | HuMT files still lack stable response IDs and therefore use documented one-to-one text matching. |
| Construct validity | Reliability, disagreement cases, correlations, and low VIF do not prove psychometric validity. | CHI reviewers may reject overclaiming. | Manuscript labels these as construct-relationship diagnostics and explicitly avoids treating them as complete discriminant validation. | Multi-item measures, alternative OA criteria, and external rater populations remain future work. |
| HCI contribution | Paper could look like a statistical benchmark only. | CHI expects design/research relevance. | Added diagnostic examples, architecture figure, and design implications. | No experiment tests whether designers using PERSONA make better decisions. |

## High

| Risk | Problem | Why reviewer may care | Manuscript response | Residual limitation |
|---|---|---|---|---|
| D operationalization | D could be read as intentional deception. | AI systems do not intend in the human sense. | D is defined as misleading implication risk, not intent. | Rater judgments still depend on rubric interpretation. |
| Health ceiling effect | Health OA is heavily ceilinged. | Predictive claims may be variance-limited. | Health is framed as weaker/uncertain evidence; ceiling is reported as 63.86%. | Health cannot strongly validate the framework without more OA variance. |
| Limited annotator pool | Five volunteer raters per pool: psychology students for mental health, MBBS students for general health, and teachers or teaching assistants for education. | Generalization and normative authority are limited. | Methods report recruitment and qualifications without calling trainees licensed professionals. | Licensed-professional and end-user validation remains needed. |
| Predictive vs causal interpretation | Models are associative. | Reviewers may object to design recommendations as causal. | Manuscript uses predictive/diagnostic language and labels design implications as not experimentally validated. | Intervention effects remain untested. |

## Medium

| Risk | Problem | Why reviewer may care | Manuscript response | Residual limitation |
|---|---|---|---|---|
| Novelty | Prior work already studies anthropomorphism, empathy, trust, and social cues. | Novelty claim could be challenged. | Manuscript frames contribution as integration plus independent OA criterion, not invention of each construct. | Literature review should be expanded further before submission. |
| Domain coverage | Three domains are not broad enough for universal claims. | Domain differences may reflect dataset construction. | Paper avoids universal validation language and reports domain interaction audit. | More domains and standardized prompt construction needed. |
| Education D floor | Education D has 87.23% floor. | D may appear uninformative in education. | Limitation notes education D floor effect. | Education deception-risk evidence is restricted. |

## Low

| Risk | Problem | Why reviewer may care | Manuscript response | Residual limitation |
|---|---|---|---|---|
| Figure selection | Ablation figure could overemphasize one model family. | Readers may want all specs. | Compact figure is paired with table/report references; full ablation lives in outputs. | Submission appendix may need full ablation table. |
| Overleaf compilation | Local machine lacks LaTeX. | Zip may need Overleaf compile checks. | PAPER_TODOS records compile verification. | Human must confirm PDF rendering on Overleaf. |
