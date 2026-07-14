# PERSONA Analysis Report

Automated statistical analysis of HuMT human-likeness and PERSONA dimensions (E, D, F, OA) for mental-health AI responses.

## 1. Major findings

- Analyzed **660** annotated responses.

### Hypothesis outcomes

- **H1** (Models differ on Deception Risk (D)): Kruskal-Wallis = 4.895978761426432, p=0.0864672645904626 → not significant / N/A.

- **H2** (Models differ on Overall Appropriateness (OA)): Kruskal-Wallis = 15.019597295281006, p=0.0005476913565593 → significant.

- **H3** (HuMT correlates with OA): Spearman = 0.2094010152467883, p=5.644225576126734e-08 → significant.

- **H4** (PERSONA explains OA beyond HuMT): Nested F-test (M4 vs M1) = 1614.809359852669, p=0.0 → significant.

- **H5** (Deception Risk higher on ADV than EVAL): Mann-Whitney (greater) = 54963.0, p=0.0505486392295719 → not significant / N/A.

- **H6** (Empathy relates more positively to OA when D is low): Spearman in low-D subset = 0.8219370779990786, p=8.199684591269579e-160 → significant.

- **H7** (Contextual Fit correlates with OA): Spearman = 0.5470259631135928, p=8.82992135837746e-53 → significant.

### Incremental validity

- Δ Adjusted R² (M4 PERSONA full vs M1 HuMT-only) = **0.8436120317957664** (base=0.04173239389850292, full=0.8853444256942693).

- PERSONA dimensions add incremental validity beyond HuMT if delta_adj_r2 > 0 and nested F/LRT are significant.

- Best ablation specification: **HuMT+E+D+F** (adj R²=0.885).

### Calibration (HuMT vs OA)

- Pearson(HuMT, OA)=0.20781366108063623, ECE=0.041637008306660304, MCE=0.3453098269481127, Brier=0.14863819833677125.

- If calibration error is high / correlation modest, human-likeness is **not** a reliable proxy for appropriateness.

### Adversarial datasets

- Dataset families present: ['CounselBench-ADV', 'CounselBench-EVAL'].

- Note: PERSONA-ADV prompts are not yet present; comparisons use available dataset families.

### Annotation reliability

- Status: skipped_aggregated_only. Final PERSONA scores are the integer-masked mean of 5 human annotators, but raw per-annotator ratings are not stored in the analysis CSV. Krippendorff/Kappa/ICC require unaggregated rater columns.

## 2. Statistical significance and effect sizes

- See `results/hypotheses/hypothesis_tests.csv` and `results/model_comparison/effect_sizes.csv` for full effect-size reporting (Cohen's d, Hedges' g, Cliff's delta, η²/ω²).

## 3. Interpretation

- PERSONA disentangles empathy, deception risk, and contextual fit rather than treating anthropomorphism as a single 'human-like is better' axis.
- Primary claim under test: PERSONA dimensions explain Overall Appropriateness beyond HuMT alone (incremental validity / nested models / ablation).
- Model profile differences (radar / omnibus tests) support model-specific anthropomorphism signatures.

## 4. Potential threats to validity

- Published PERSONA scores are human-aggregated (5 annotators → mean → integer mask); raw per-annotator ratings are not in the CSVs, so IRR is not yet estimable.
- Many OA reason strings still reference Empathy/DeceptionRisk/ContextualFit components; treat nested OA~E+D+F incremental claims cautiously until OA is confirmed fully independent.
- DeceptionRisk is heavily floor-distributed (mostly 1), limiting D discriminability.
- PERSONA-ADV prompt set is not yet in the CSV inventory.
- HuMT and Likert PERSONA scales have different metric properties; comparisons use standardized/robust methods where possible.
- Cross-sectional single-turn responses underrepresent multi-turn attachment dynamics.

## 5. Reviewer discussion points

- Why OA is judged holistically rather than as a mean of E/D/F.
- Why incremental R² over HuMT is the key claim versus raw correlations.
- Distinguishing descriptive human-likeness (H/HuMT) from normative appropriateness.
- Release or archive raw 5-annotator matrices to unlock IRR reporting.

## 6. Limitations

- Aggregated labels without per-rater spreads hide disagreement and prevent Kappa/ICC.
- No original CounselBench clinician metrics joined yet for Exp.1-style convergence tests.
- Clustering/EFA with few dimensions is exploratory.

## 7. Future work

- Publish raw multi-rater matrices + IRR (Krippendorff/Kappa/ICC).
- Add PERSONA-ADV prompts and re-run adversarial contrasts.
- Join CounselBench expert Quality/Empathy ratings for convergent validity.
- Multi-turn extensions and user-study validation of Relational Expectation (R).

## 8. Artifact index

- Figures: `figures/`
- Tables: `tables/`
- Numeric results: `results/`
