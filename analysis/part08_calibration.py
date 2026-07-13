"""Part 8 — Calibration between HuMT and OA."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.calibration")


def run_calibration(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "calibration"
    out_fig = cfg.figures_dir / "calibration"
    out_tab = cfg.tables_dir / "calibration"

    data = df[["HuMT", "OA"]].dropna().copy()
    # Map OA 1-5 to [0,1] for calibration-style diagnostics;
    # HuMT min-max scaled as "probability-like" score.
    oa01 = (data["OA"] - 1.0) / 4.0
    humt = data["HuMT"].to_numpy()
    humt01 = (humt - humt.min()) / (humt.max() - humt.min() + 1e-12)

    # Treat high-OA as positive event threshold at median for reliability diagram
    y_bin = (oa01 >= oa01.median()).astype(int).to_numpy()
    prob_true, prob_pred = calibration_curve(y_bin, humt01, n_bins=8, strategy="quantile")

    # ECE / MCE
    bins = np.linspace(0, 1, 9)
    ece = 0.0
    mce = 0.0
    rows = []
    for i in range(len(bins) - 1):
        lo, hi = bins[i], bins[i + 1]
        mask = (humt01 >= lo) & ((humt01 < hi) if i < len(bins) - 2 else (humt01 <= hi))
        if not np.any(mask):
            continue
        conf = float(humt01[mask].mean())
        acc = float(y_bin[mask].mean())
        gap = abs(acc - conf)
        ece += gap * (mask.mean())
        mce = max(mce, gap)
        rows.append({"bin": i, "lo": lo, "hi": hi, "confidence": conf, "accuracy": acc, "gap": gap, "n": int(mask.sum())})

    # Brier against continuous OA01 using HumT01 as prediction
    brier = float(np.mean((humt01 - oa01.to_numpy()) ** 2))

    calib_bins = pd.DataFrame(rows)
    save_csv(calib_bins, out_res / "calibration_bins.csv")
    summary = {
        "ece": float(ece),
        "mce": float(mce),
        "brier": brier,
        "pearson_humt_oa": float(np.corrcoef(data["HuMT"], data["OA"])[0, 1]),
        "note": "HuMT min-max scaled; OA linearly mapped to [0,1]. Binary reliability uses median OA split.",
    }
    save_json(summary, out_res / "calibration_summary.json")
    dataframe_to_latex(pd.DataFrame([summary]), out_tab / "calibration_summary.tex",
                       caption="Calibration of HuMT against OA.",
                       label="tab:calibration")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot([0, 1], [0, 1], "--", color="gray", label="Perfect")
    axes[0].plot(prob_pred, prob_true, "o-", color="#4C72B0", label="HuMT")
    axes[0].set_xlabel("Mean predicted value (scaled HuMT)")
    axes[0].set_ylabel("Fraction high-OA")
    axes[0].set_title("Reliability diagram")
    axes[0].legend()

    # Calibration curve continuous: bin mean OA vs mean HuMT
    if len(calib_bins):
        axes[1].plot(calib_bins["confidence"], calib_bins["accuracy"], "o-", color="#C44E52")
        axes[1].plot([0, 1], [0, 1], "--", color="gray")
        axes[1].set_xlabel("Bin mean scaled HuMT")
        axes[1].set_ylabel("Bin mean high-OA rate")
        axes[1].set_title("Calibration bins")
    save_fig(fig, out_fig / "fig_calibration_curves.png", dpi=cfg.dpi)

    # Scatter HuMT vs OA
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.scatter(data["HuMT"], data["OA"], alpha=0.35, s=12, color="#4C72B0")
    # Linear fit
    coef = np.polyfit(data["HuMT"], data["OA"], 1)
    xs = np.linspace(data["HuMT"].min(), data["HuMT"].max(), 100)
    ax.plot(xs, coef[0] * xs + coef[1], color="#C44E52")
    ax.set_xlabel("HuMT")
    ax.set_ylabel("OA")
    ax.set_title("HuMT vs Overall Appropriateness")
    save_fig(fig, out_fig / "fig_humt_vs_oa.png", dpi=cfg.dpi)

    logger.info("Part 8 calibration complete.")
    return summary
