"""Phase 4 - cross-validated prediction, ablation, and incremental validity.

Three deliberate departures from the previous pipeline:

1. Cross-validation groups on ``prompt_id``. Each prompt has one response per
   model, so ungrouped splitting puts sibling responses on both sides of the
   split. The education and health numbers in the committed summaries were
   produced without grouping because those files carry no prompt id; Phase 1
   reconstructs it.

2. Cross-validation is repeated with independently seeded fold assignments and
   reported as a mean with a standard deviation across repeats. A single
   grouped split is an arbitrary draw, and the library heuristic that produced
   the committed numbers is version dependent.

3. Every specification inside a domain is fitted on the same complete-case rows,
   so differences in performance reflect the predictors and not differences in
   sample.

Outputs:
  analysis/outputs/tables/cv_performance.csv
  analysis/outputs/tables/cv_folds.csv
  analysis/outputs/tables/ablation.csv
  analysis/outputs/tables/incremental_validity.csv
  analysis/outputs/tables/cv_fold_assignments.csv
  analysis/outputs/reports/predictive.md
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .persona_common import (
    CV_FOLDS,
    CV_REPEATS,
    DIMENSIONS,
    DOMAIN_LABEL,
    DOMAINS,
    FIGURE_DIR,
    N_BOOT,
    PROCESSED_DIR,
    PROFILE,
    SEED,
    cluster_bootstrap_indices,
    grouped_folds,
    load_consensus,
    mae,
    ols_fit_predict,
    percentile_ci,
    r2,
    rmse,
    save_json,
    save_markdown,
    save_table,
)

# Model A is H only, Model B is the full profile, Model C is the profile
# without H. The rest are the systematic ablation the analysis plan requires.
SPECS: dict[str, list[str]] = {
    "H_only": ["H"],
    "E_only": ["E"],
    "D_only": ["D"],
    "F_only": ["F"],
    "H+E": ["H", "E"],
    "H+D": ["H", "D"],
    "H+F": ["H", "F"],
    "H+E+D": ["H", "E", "D"],
    "H+E+F": ["H", "E", "F"],
    "H+D+F": ["H", "D", "F"],
    "E+D+F": ["E", "D", "F"],
    "H+E+D+F": ["H", "E", "D", "F"],
}
FULL = "H+E+D+F"
BASELINE = "H_only"


# --------------------------------------------------------------------------
# Cross-validation
# --------------------------------------------------------------------------
def repeated_grouped_cv(frame: pd.DataFrame, features: list[str], outcome: str = "OA"):
    """Return mean out-of-fold predictions plus per-fold and per-repeat metrics."""
    x = frame[features].to_numpy(dtype=float)
    y = frame[outcome].to_numpy(dtype=float)
    groups = frame["prompt_id"].to_numpy()

    oof = np.zeros((CV_REPEATS, len(y)))
    fold_rows, repeat_rows = [], []
    assignments = {}

    for repeat in range(CV_REPEATS):
        rng = np.random.default_rng(SEED + repeat)
        folds = grouped_folds(groups, CV_FOLDS, rng)
        assignments[repeat] = folds
        predictions = np.full(len(y), np.nan)
        for fold in range(CV_FOLDS):
            test = folds == fold
            train = ~test
            if train.sum() < len(features) + 2 or test.sum() == 0:
                continue
            predictions[test] = ols_fit_predict(x[train], y[train], x[test])
            fold_rows.append({
                "repeat": repeat, "fold": fold,
                "n_train": int(train.sum()), "n_test": int(test.sum()),
                "train_prompts": int(pd.unique(groups[train]).size),
                "test_prompts": int(pd.unique(groups[test]).size),
                "r2": r2(y[test], predictions[test]),
                "rmse": rmse(y[test], predictions[test]),
                "mae": mae(y[test], predictions[test]),
            })
        oof[repeat] = predictions
        repeat_rows.append({
            "repeat": repeat,
            "r2": r2(y, predictions),
            "rmse": rmse(y, predictions),
            "mae": mae(y, predictions),
            "spearman": float(stats.spearmanr(y, predictions).statistic),
            "pearson": float(stats.pearsonr(y, predictions)[0]),
        })

    return oof.mean(axis=0), pd.DataFrame(fold_rows), pd.DataFrame(repeat_rows), assignments[0]


def in_sample_r2(frame: pd.DataFrame, features: list[str], outcome: str = "OA") -> tuple[float, float]:
    x = frame[features].to_numpy(dtype=float)
    y = frame[outcome].to_numpy(dtype=float)
    fitted = ols_fit_predict(x, y, x)
    value = r2(y, fitted)
    n, k = len(y), len(features)
    adjusted = 1 - (1 - value) * (n - 1) / (n - k - 1) if n > k + 1 else float("nan")
    return value, adjusted


# --------------------------------------------------------------------------
# Per-domain analysis
# --------------------------------------------------------------------------
def analyse_domain(label: str, frame: pd.DataFrame, extra_features: list[str]):
    """Fit every specification on the same complete-case rows and compare them."""
    rng = np.random.default_rng(SEED)
    groups = frame["prompt_id"].to_numpy()
    y = frame["OA"].to_numpy(dtype=float)
    boot_indices = list(cluster_bootstrap_indices(groups, rng, N_BOOT))

    oof_by_spec, performance, folds_all, assignment = {}, [], [], None
    for name, base in SPECS.items():
        features = base + extra_features
        oof, fold_frame, repeat_frame, first_assignment = repeated_grouped_cv(frame, features)
        oof_by_spec[name] = oof
        assignment = first_assignment if assignment is None else assignment

        boots = [r2(y[idx], oof[idx]) for idx in boot_indices]
        low, high = percentile_ci(boots)
        ins, adj = in_sample_r2(frame, features)

        performance.append({
            "domain": label, "specification": name, "predictors": "+".join(features),
            "n": len(frame), "n_prompt_groups": int(pd.unique(groups).size),
            "cv_r2_mean": float(repeat_frame["r2"].mean()),
            "cv_r2_sd_across_repeats": float(repeat_frame["r2"].std(ddof=1)),
            "cv_r2_boot_ci_low": low, "cv_r2_boot_ci_high": high,
            "cv_rmse": float(repeat_frame["rmse"].mean()),
            "cv_mae": float(repeat_frame["mae"].mean()),
            "cv_spearman": float(repeat_frame["spearman"].mean()),
            "cv_pearson": float(repeat_frame["pearson"].mean()),
            "in_sample_r2": ins, "in_sample_adj_r2": adj,
            "fold_r2_min": float(fold_frame["r2"].min()),
            "fold_r2_max": float(fold_frame["r2"].max()),
        })
        fold_frame.insert(0, "specification", name)
        fold_frame.insert(0, "domain", label)
        folds_all.append(fold_frame)

    performance = pd.DataFrame(performance)

    # ---- ablation: every spec against the full profile, paired bootstrap ----
    ablation = []
    for name in SPECS:
        deltas = [r2(y[idx], oof_by_spec[name][idx]) - r2(y[idx], oof_by_spec[FULL][idx])
                  for idx in boot_indices]
        low, high = percentile_ci(deltas)
        point = (performance.loc[performance["specification"] == name, "cv_r2_mean"].iloc[0]
                 - performance.loc[performance["specification"] == FULL, "cv_r2_mean"].iloc[0])
        ablation.append({
            "domain": label, "specification": name,
            "dropped": "+".join(d for d in PROFILE if d not in SPECS[name]) or "nothing",
            "cv_r2": performance.loc[performance["specification"] == name, "cv_r2_mean"].iloc[0],
            "delta_vs_full": point,
            "delta_ci_low": low, "delta_ci_high": high,
            "worse_than_full": bool(high < 0),
            "boot_share_worse_than_full": float(np.mean(np.asarray(deltas) < 0)),
        })
    ablation = pd.DataFrame(ablation)

    # ---- incremental validity: full and E+D+F against the H-only baseline ---
    incremental = []
    for name in (FULL, "E+D+F", "H+F", "F_only"):
        deltas = [r2(y[idx], oof_by_spec[name][idx]) - r2(y[idx], oof_by_spec[BASELINE][idx])
                  for idx in boot_indices]
        low, high = percentile_ci(deltas)
        point = (performance.loc[performance["specification"] == name, "cv_r2_mean"].iloc[0]
                 - performance.loc[performance["specification"] == BASELINE, "cv_r2_mean"].iloc[0])
        incremental.append({
            "domain": label, "comparison": f"{name} vs {BASELINE}",
            "cv_r2_baseline": performance.loc[performance["specification"] == BASELINE, "cv_r2_mean"].iloc[0],
            "cv_r2_model": performance.loc[performance["specification"] == name, "cv_r2_mean"].iloc[0],
            "delta_cv_r2": point, "delta_ci_low": low, "delta_ci_high": high,
            "ci_excludes_zero": bool(low > 0 or high < 0),
        })
    # does H add anything on top of the human-rated dimensions?
    deltas = [r2(y[idx], oof_by_spec[FULL][idx]) - r2(y[idx], oof_by_spec["E+D+F"][idx])
              for idx in boot_indices]
    low, high = percentile_ci(deltas)
    incremental.append({
        "domain": label, "comparison": f"{FULL} vs E+D+F",
        "cv_r2_baseline": performance.loc[performance["specification"] == "E+D+F", "cv_r2_mean"].iloc[0],
        "cv_r2_model": performance.loc[performance["specification"] == FULL, "cv_r2_mean"].iloc[0],
        "delta_cv_r2": (performance.loc[performance["specification"] == FULL, "cv_r2_mean"].iloc[0]
                        - performance.loc[performance["specification"] == "E+D+F", "cv_r2_mean"].iloc[0]),
        "delta_ci_low": low, "delta_ci_high": high,
        "ci_excludes_zero": bool(low > 0 or high < 0),
    })
    # and does anything beat domain fit on its own?
    deltas = [r2(y[idx], oof_by_spec[FULL][idx]) - r2(y[idx], oof_by_spec["F_only"][idx])
              for idx in boot_indices]
    low, high = percentile_ci(deltas)
    incremental.append({
        "domain": label, "comparison": f"{FULL} vs F_only",
        "cv_r2_baseline": performance.loc[performance["specification"] == "F_only", "cv_r2_mean"].iloc[0],
        "cv_r2_model": performance.loc[performance["specification"] == FULL, "cv_r2_mean"].iloc[0],
        "delta_cv_r2": (performance.loc[performance["specification"] == FULL, "cv_r2_mean"].iloc[0]
                        - performance.loc[performance["specification"] == "F_only", "cv_r2_mean"].iloc[0]),
        "delta_ci_low": low, "delta_ci_high": high,
        "ci_excludes_zero": bool(low > 0 or high < 0),
    })

    assignment_frame = pd.DataFrame({
        "domain": label,
        "annotation_item_id": frame["annotation_item_id"].to_numpy(),
        "prompt_id": groups,
        "fold_repeat0": assignment,
    })
    return performance, pd.concat(folds_all, ignore_index=True), ablation, pd.DataFrame(incremental), assignment_frame


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def figure_model_comparison(performance: pd.DataFrame) -> None:
    order = ["H_only", "E_only", "D_only", "F_only", "E+D+F", "H+E+D+F"]
    labels = [DOMAIN_LABEL.get(d, d) for d in performance["domain"].unique()]
    fig, ax = plt.subplots(figsize=(11, 4.6))
    width = 0.8 / len(labels)
    for i, (domain, block) in enumerate(performance.groupby("domain", sort=False)):
        block = block.set_index("specification").reindex(order)
        positions = np.arange(len(order)) + i * width
        errors = np.vstack([
            block["cv_r2_mean"] - block["cv_r2_boot_ci_low"],
            block["cv_r2_boot_ci_high"] - block["cv_r2_mean"],
        ])
        ax.bar(positions, block["cv_r2_mean"], width=width * 0.92,
               label=DOMAIN_LABEL.get(domain, domain), yerr=np.abs(errors), capsize=3)
    ax.set_xticks(np.arange(len(order)) + width * (len(labels) - 1) / 2, order, rotation=20)
    ax.axhline(0, color="#444", linewidth=1)
    ax.set_ylabel("Prompt-grouped cross-validated R²")
    ax.set_title("Predicting independently rated OA: cross-validated model comparison")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_cv_model_comparison.png", dpi=160)
    plt.close(fig)


def figure_ablation(ablation: pd.DataFrame) -> None:
    domains = list(ablation["domain"].unique())
    fig, axes = plt.subplots(1, len(domains), figsize=(5.2 * len(domains), 4.8), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, domain in zip(axes, domains):
        block = ablation[ablation["domain"] == domain].sort_values("delta_vs_full")
        positions = np.arange(len(block))
        ax.barh(positions, block["delta_vs_full"],
                xerr=np.vstack([block["delta_vs_full"] - block["delta_ci_low"],
                                block["delta_ci_high"] - block["delta_vs_full"]]),
                color=["#C44E52" if w else "#8C8C8C" for w in block["worse_than_full"]],
                capsize=2)
        ax.set_yticks(positions, block["specification"], fontsize=9)
        ax.axvline(0, color="#333", linewidth=1)
        ax.set_title(DOMAIN_LABEL.get(domain, domain), fontsize=11)
        ax.set_xlabel("Δ cross-validated R² vs full profile")
        ax.grid(axis="x", alpha=0.25)
    fig.suptitle("Ablation: red bars are specifications reliably worse than the full profile", fontsize=12)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_ablation.png", dpi=160)
    plt.close(fig)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main() -> None:
    data = load_consensus()
    needed = ["H"] + DIMENSIONS + ["prompt_id"]

    performance, folds, ablation, incremental, assignments = [], [], [], [], []
    coverage = []

    for domain in DOMAINS:
        block = data[data["domain"] == domain]
        complete = block.dropna(subset=needed).reset_index(drop=True)
        coverage.append({"domain": domain, "responses": len(block), "complete_cases": len(complete),
                         "excluded_incomplete": len(block) - len(complete),
                         "prompt_groups": complete["prompt_id"].nunique()})
        p, f, a, i, s = analyse_domain(domain, complete, [])
        performance.append(p); folds.append(f); ablation.append(a); incremental.append(i); assignments.append(s)

    # pooled, with domain held constant through indicator columns
    pooled = data.dropna(subset=needed).reset_index(drop=True).copy()
    dummies = pd.get_dummies(pooled["domain"], prefix="dom", drop_first=True).astype(float)
    pooled = pd.concat([pooled, dummies], axis=1)
    coverage.append({"domain": "pooled", "responses": len(data), "complete_cases": len(pooled),
                     "excluded_incomplete": len(data) - len(pooled),
                     "prompt_groups": pooled["prompt_id"].nunique()})
    p, f, a, i, s = analyse_domain("pooled", pooled, list(dummies.columns))
    performance.append(p); folds.append(f); ablation.append(a); incremental.append(i); assignments.append(s)

    performance = pd.concat(performance, ignore_index=True)
    folds = pd.concat(folds, ignore_index=True)
    ablation = pd.concat(ablation, ignore_index=True)
    incremental = pd.concat(incremental, ignore_index=True)
    assignments = pd.concat(assignments, ignore_index=True)
    coverage = pd.DataFrame(coverage)

    save_table(performance, "cv_performance")
    save_table(folds, "cv_folds")
    save_table(ablation, "ablation")
    save_table(incremental, "incremental_validity")
    save_table(assignments, "cv_fold_assignments")
    save_table(coverage, "cv_coverage")

    figure_model_comparison(performance[performance["domain"] != "pooled"])
    figure_ablation(ablation[ablation["domain"] != "pooled"])

    save_markdown(render(performance, ablation, incremental, coverage), "predictive")
    save_json({"coverage": coverage.to_dict(orient="records"),
               "cv_performance": performance.to_dict(orient="records"),
               "ablation": ablation.to_dict(orient="records"),
               "incremental_validity": incremental.to_dict(orient="records"),
               "settings": {"estimator": "ordinary_least_squares_with_intercept",
                            "regularization": "none", "hyperparameter_tuning": "none",
                            "predictor_scaling": "recorded_scales", "imputation": "none",
                            "seed": SEED, "folds": CV_FOLDS, "repeats": CV_REPEATS,
                            "bootstrap": N_BOOT, "grouping": "prompt_id"}},
              "phase4_results")
    print(f"Phase 4 complete: {len(performance)} specifications across {performance['domain'].nunique()} groupings")


def render(performance, ablation, incremental, coverage) -> str:
    lines = ["# Cross-validated prediction, ablation, incremental validity (Phase 4)", "",
             "Every specification uses ordinary least squares linear regression with an intercept. "
             "Predictors enter on their recorded scales; pooled specifications also include domain "
             "indicators. There is no regularization, imputation, feature selection, hyperparameter "
             "tuning, or outcome transformation.", "",
             f"Cross-validation is 5-fold, grouped on `prompt_id`, repeated {CV_REPEATS} times with "
             f"independently seeded fold assignments (base seed {SEED}). Confidence intervals come from "
             f"{N_BOOT} prompt-cluster bootstrap resamples of the out-of-fold predictions; comparisons "
             "between specifications reuse the same resamples so the differences are paired.", "",
             "## Sample", "",
             "| Grouping | Responses | Complete cases | Excluded | Prompt groups |",
             "|---|---:|---:|---:|---:|"]
    for _, r in coverage.iterrows():
        lines.append(f"| {r['domain']} | {r['responses']} | {r['complete_cases']} | "
                     f"{r['excluded_incomplete']} | {r['prompt_groups']} |")
    lines += ["", "All released responses are complete for the analysis variables. Every specification "
              "within a grouping uses identical rows, so performance differences reflect predictors only.", ""]

    lines += ["## Cross-validated performance", "",
              "| Grouping | Specification | N | CV R² | SD across repeats | 95% CI | Spearman | Pearson | MAE | RMSE | In-sample R² |",
              "|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|"]
    for _, r in performance.iterrows():
        lines.append(
            f"| {r['domain']} | {r['specification']} | {r['n']} | {r['cv_r2_mean']:.3f} | "
            f"{r['cv_r2_sd_across_repeats']:.4f} | [{r['cv_r2_boot_ci_low']:.3f}, {r['cv_r2_boot_ci_high']:.3f}] | "
            f"{r['cv_spearman']:.3f} | {r['cv_pearson']:.3f} | {r['cv_mae']:.3f} | {r['cv_rmse']:.3f} | "
            f"{r['in_sample_r2']:.3f} |")

    lines += ["", "## Incremental validity", "",
              "| Grouping | Comparison | Baseline CV R² | Model CV R² | Δ | 95% CI | CI excludes 0 |",
              "|---|---|---:|---:|---:|---|---|"]
    for _, r in incremental.iterrows():
        lines.append(f"| {r['domain']} | {r['comparison']} | {r['cv_r2_baseline']:.3f} | {r['cv_r2_model']:.3f} | "
                     f"{r['delta_cv_r2']:.3f} | [{r['delta_ci_low']:.3f}, {r['delta_ci_high']:.3f}] | "
                     f"{'yes' if r['ci_excludes_zero'] else 'no'} |")

    lines += ["", "## Ablation", "",
              "Each specification is compared with the full profile on paired bootstrap resamples. "
              "`reliably worse` means the 95 per cent interval for the difference lies entirely below zero, "
              "which is the test of whether dropping a dimension actually costs predictive accuracy.", "",
              "| Grouping | Specification | Dropped | CV R² | Δ vs full | 95% CI | Reliably worse |",
              "|---|---|---|---:|---:|---|---|"]
    for _, r in ablation.iterrows():
        lines.append(f"| {r['domain']} | {r['specification']} | {r['dropped']} | {r['cv_r2']:.3f} | "
                     f"{r['delta_vs_full']:.3f} | [{r['delta_ci_low']:.3f}, {r['delta_ci_high']:.3f}] | "
                     f"{'yes' if r['worse_than_full'] else 'no'} |")

    lines += ["", "## Figures", "",
              "- `fig_cv_model_comparison.png`", "- `fig_ablation.png`", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
