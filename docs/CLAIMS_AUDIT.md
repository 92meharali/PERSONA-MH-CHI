# CHI Manuscript Claims Audit

This file audits major claims in `paper/revised3.tex` after the current
revision pass.

| Claim | Evidence source | Exact result or support | Evidence type | Status |
|---|---|---|---|---|
| Human-likeness alone is insufficient as a proxy for overall anthropomorphic appropriateness. | `analysis/outputs/tables/cv_performance.csv`; `analysis/outputs/tables/correlations.csv` | H-only R2: MH 0.026, Edu 0.099, Health -0.007, Pooled 0.221; H/OA Spearman weak by domain. | Empirical | SUPPORTED |
| Human-likeness is not wrong or harmful by default. | `docs/theory/PERSONA_THEORY.md`; HumT and HCI literature cited in manuscript | Theory assigns no fixed valence to H and treats it as descriptive. | Theoretical / literature-supported | SUPPORTED |
| The full PERSONA profile captures OA-associated information omitted by H alone. | `analysis/outputs/tables/incremental_validity.csv` | Full vs H-only gain: MH +0.632 CI [0.567,0.686]; Edu +0.462 CI [0.278,0.598]; Pooled +0.278 CI [0.204,0.339]; Health +0.264 CI [-0.053,0.400]. | Empirical | SUPPORTED WITH DOMAIN QUALIFICATION |
| PERSONA is superior to every alternative response-level quality baseline. | No direct baseline comparison in the current analysis. | The current comparison is specifically full profile versus H-only. | Empirical | NOT TESTED / NOT CLAIMED |
| Health provides weaker evidence. | `analysis/outputs/tables/incremental_validity.csv`; `analysis/outputs/tables/ceiling_floor.csv` | Health gain CI crosses zero; health OA ceiling is 63.86%. | Empirical | SUPPORTED |
| Contextual fit accounts for much of the predictive signal in mental health and education. | `analysis/outputs/tables/ablation.csv` | F-only R2: MH 0.651 vs full 0.659; Edu 0.562 vs full 0.562. | Empirical | SUPPORTED |
| F is not the same as OA. | `docs/theory/CONSTRUCT_DEFINITIONS.md`; `docs/theory/CLAIMS_AND_BOUNDARIES.md` | F is contextual calibration; OA is holistic and can include safety, accuracy, actionability, and responsibility. | Theoretical | REQUIRES QUALIFICATION |
| The dimensions exhibit low statistical redundancy. | `analysis/outputs/tables/collinearity_vif.csv` | Max VIF: MH 1.345, Edu 1.393, Health 1.490. | Empirical diagnostic | SUPPORTED |
| Low VIF establishes full construct validity. | `docs/theory/CLAIMS_AND_BOUNDARIES.md` | The documents explicitly reject this inference. | Theoretical / methodological | NOT SUPPORTED |
| Relationships between dimensions and OA vary by domain. | `analysis/outputs/tables/domain_interactions.csv` | Significant slope differences for E x Edu, E x Health, D x Health, F x Health; H x Health is borderline and not treated as significant. | Empirical | SUPPORTED |
| D measures intentional deception by the AI. | `docs/theory/CONSTRUCT_DEFINITIONS.md`; rubric | D concerns misleading implication risk, not model intent. | Theoretical | NOT SUPPORTED |
| D measures anthropomorphic deception/misleading implication risk. | `docs/theory/CONSTRUCT_DEFINITIONS.md`; rubric | D severity ladder captures implied feeling, experience, memory, authority, continuity, dependency. | Theoretical / annotation protocol | SUPPORTED |
| OA is independent from E/D/F measurement. | `docs/theory/ANNOTATION_THEORY.md`; `analysis/build_dataset.py`; clean data layout | Group A rates OA only; Group B rates E/D/F. | Methodological / empirical provenance | SUPPORTED |
| Separate rater pools prove complete construct independence. | `docs/theory/CLAIMS_AND_BOUNDARIES.md` | F and OA are conceptually adjacent; separate pools reduce criterion contamination but do not settle construct overlap. | Methodological | NOT SUPPORTED |
| PERSONA is novel as a diagnostic framing for anthropomorphic appropriateness. | Current paper theory plus cited literature | Existing work measures anthropomorphic cues, empathy, trust, or risks; PERSONA combines profile dimensions and independent OA prediction. | Interpretive / literature-supported | PARTIALLY SUPPORTED |
| PERSONA is a fully validated universal psychometric instrument. | `docs/theory/CLAIMS_AND_BOUNDARIES.md` | Current data are first empirical evaluation, not universal validation. | Methodological | NOT SUPPORTED |
