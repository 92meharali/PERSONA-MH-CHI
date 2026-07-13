"""Part 9 — Sensitivity / robustness analyses."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import QuantileRegressor

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.sensitivity")


def _ols_r2(df: pd.DataFrame, predictors: list[str]) -> float:
    y = df["OA"]
    X = sm.add_constant(df[predictors])
    return float(sm.OLS(y, X).fit().rsquared_adj)


def run_sensitivity(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "sensitivity"
    out_fig = cfg.figures_dir / "sensitivity"
    out_tab = cfg.tables_dir / "sensitivity"
    preds = ["HuMT", "E", "D", "F"]
    data = df[preds + ["OA", "model", "dataset_family", "category"]].dropna().copy()
    full_adj = _ols_r2(data, preds)

    rows = []
    # Leave-one-model-out
    for model in sorted(data["model"].unique()):
        sub = data[data["model"] != model]
        rows.append({"scheme": "leave_one_model_out", "left_out": model, "adj_r2": _ols_r2(sub, preds), "n": len(sub)})

    # Leave-one-dataset-out
    for dset in sorted(data["dataset_family"].unique()):
        sub = data[data["dataset_family"] != dset]
        if len(sub) < 30:
            continue
        rows.append({"scheme": "leave_one_dataset_out", "left_out": dset, "adj_r2": _ols_r2(sub, preds), "n": len(sub)})

    # Leave-one-category-out (top categories)
    top_cats = data["category"].value_counts().head(12).index.tolist()
    for cat in top_cats:
        sub = data[data["category"] != cat]
        rows.append({"scheme": "leave_one_category_out", "left_out": cat, "adj_r2": _ols_r2(sub, preds), "n": len(sub)})

    # Bootstrap adj R2
    rng = np.random.default_rng(cfg.random_seed)
    boots = []
    n = len(data)
    for _ in range(cfg.n_bootstrap):
        sample = data.iloc[rng.integers(0, n, n)]
        boots.append(_ols_r2(sample, preds))
    boot_summary = {
        "mean": float(np.mean(boots)),
        "std": float(np.std(boots, ddof=1)),
        "ci_low": float(np.quantile(boots, 0.025)),
        "ci_high": float(np.quantile(boots, 0.975)),
    }

    # Jackknife
    jack = []
    for i in range(min(n, 200)):  # cap for runtime
        sub = data.drop(index=data.index[i])
        jack.append(_ols_r2(sub, preds))

    # Robust regression (Huber via statsmodels RLM)
    X = sm.add_constant(data[preds])
    rlm = sm.RLM(data["OA"], X, M=sm.robust.norms.HuberT()).fit()
    robust_params = rlm.params.to_dict()

    # Quantile regression at median
    qr = QuantileRegressor(quantile=0.5, alpha=0.0, solver="highs")
    qr.fit(data[preds], data["OA"])
    q_params = {"intercept": float(qr.intercept_), **{f: float(c) for f, c in zip(preds, qr.coef_)}}

    sens = pd.DataFrame(rows)
    save_csv(sens, out_res / "sensitivity_leave_one_out.csv")
    save_json(
        {
            "full_adj_r2": full_adj,
            "bootstrap_adj_r2": boot_summary,
            "jackknife_mean_adj_r2": float(np.mean(jack)),
            "jackknife_std_adj_r2": float(np.std(jack, ddof=1)),
            "robust_rlm_params": {k: float(v) for k, v in robust_params.items()},
            "quantile_median_params": q_params,
        },
        out_res / "sensitivity_summary.json",
    )
    dataframe_to_latex(sens.head(30), out_tab / "sensitivity_loo.tex",
                       caption="Leave-one-out sensitivity of OA~HuMT+E+D+F adjusted R².",
                       label="tab:sensitivity")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axhline(full_adj, color="black", ls="--", label=f"Full adj R²={full_adj:.3f}")
    for scheme, sub in sens.groupby("scheme"):
        ax.scatter(sub["left_out"], sub["adj_r2"], label=scheme, alpha=0.8)
    ax.set_ylabel("Adjusted R²")
    ax.set_xlabel("Left-out unit")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(fontsize=8)
    ax.set_title("Sensitivity of PERSONA regression fit")
    save_fig(fig, out_fig / "fig_sensitivity.png", dpi=cfg.dpi)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(boots, bins=30, color="#4C72B0", edgecolor="white")
    ax.axvline(boot_summary["ci_low"], color="#C44E52", ls="--")
    ax.axvline(boot_summary["ci_high"], color="#C44E52", ls="--")
    ax.set_title("Bootstrap distribution of adjusted R²")
    ax.set_xlabel("Adjusted R²")
    save_fig(fig, out_fig / "fig_bootstrap_adjr2.png", dpi=cfg.dpi)

    logger.info("Part 9 sensitivity complete.")
    return {"sensitivity": sens, "bootstrap": boot_summary}
