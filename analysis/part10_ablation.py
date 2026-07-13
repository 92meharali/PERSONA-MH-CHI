"""Part 10 — Ablation of PERSONA dimensions."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.ablation")

ABLATIONS = [
    ("HuMT", ["HuMT"]),
    ("HuMT+E", ["HuMT", "E"]),
    ("HuMT+D", ["HuMT", "D"]),
    ("HuMT+F", ["HuMT", "F"]),
    ("HuMT+E+D", ["HuMT", "E", "D"]),
    ("HuMT+E+F", ["HuMT", "E", "F"]),
    ("HuMT+D+F", ["HuMT", "D", "F"]),
    ("HuMT+E+D+F", ["HuMT", "E", "D", "F"]),
]


def run_ablation(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "ablation"
    out_fig = cfg.figures_dir / "ablation"
    out_tab = cfg.tables_dir / "ablation"
    data = df[["OA", "HuMT", "E", "D", "F"]].dropna()

    rows = []
    for name, preds in ABLATIONS:
        X = sm.add_constant(data[preds])
        fit = sm.OLS(data["OA"], X).fit()
        lr = LinearRegression()
        cv = cross_val_score(lr, data[preds], data["OA"], cv=cfg.n_cv_folds,
                             scoring="r2")
        rows.append(
            {
                "specification": name,
                "predictors": "+".join(preds),
                "r2": float(fit.rsquared),
                "adj_r2": float(fit.rsquared_adj),
                "aic": float(fit.aic),
                "bic": float(fit.bic),
                "cv_r2_mean": float(np.mean(cv)),
                "cv_r2_std": float(np.std(cv, ddof=1)),
            }
        )
    abl = pd.DataFrame(rows).sort_values("adj_r2", ascending=False)
    save_csv(abl, out_res / "ablation_results.csv")
    dataframe_to_latex(abl, out_tab / "ablation_results.tex",
                       caption="Ablation study of PERSONA dimensions for predicting OA.",
                       label="tab:ablation")

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(abl["specification"], abl["adj_r2"], color="#4C72B0")
    ax.set_ylabel("Adjusted R²")
    ax.set_title("Ablation: predictive power for OA")
    ax.tick_params(axis="x", rotation=35)
    save_fig(fig, out_fig / "fig_ablation_adjr2.png", dpi=cfg.dpi)

    save_json({"best": abl.iloc[0].to_dict()}, out_res / "ablation_summary.json")
    logger.info("Part 10 ablation complete.")
    return {"ablation": abl}
