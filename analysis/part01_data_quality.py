"""Part 1 — Data quality and descriptive statistics."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config import AnalysisConfig
from .data_loader import CANONICAL_METRICS
from .plotting import boxplot_by_group, correlation_heatmap, histogram_grid, save_fig, violin_by_group
from .utils import dataframe_to_latex, mean_ci, save_csv, save_json

logger = logging.getLogger("analysis.data_quality")


def run_data_quality(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    metrics = list(CANONICAL_METRICS)
    out_res = cfg.results_dir / "data_quality"
    out_fig = cfg.figures_dir / "data_quality"
    out_tab = cfg.tables_dir / "data_quality"

    missing = df[metrics + ["model", "dataset_family", "category"]].isna().sum().rename("missing_count")
    missing_df = missing.reset_index().rename(columns={"index": "variable"})
    missing_df["missing_rate"] = missing_df["missing_count"] / len(df)
    save_csv(missing_df, out_res / "missing_values.csv")

    desc_rows = []
    for col in metrics:
        stats = mean_ci(df[col].dropna())
        desc_rows.append({"variable": col, **stats})
    desc = pd.DataFrame(desc_rows)
    save_csv(desc, out_res / "descriptive_statistics.csv")
    dataframe_to_latex(
        desc,
        out_tab / "descriptive_statistics.tex",
        caption="Descriptive statistics for HuMT and PERSONA metrics.",
        label="tab:descriptives",
    )

    # Outliers via IQR rule.
    outlier_rows = []
    for col in metrics:
        s = df[col].dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (df[col] < low) | (df[col] > high)
        outlier_rows.append(
            {
                "variable": col,
                "n_outliers": int(mask.sum()),
                "rate": float(mask.mean()),
                "low": float(low),
                "high": float(high),
            }
        )
    outliers = pd.DataFrame(outlier_rows)
    save_csv(outliers, out_res / "outliers_iqr.csv")

    imbalance = (
        df.groupby(["model", "dataset_family"]).size().reset_index(name="n")
    )
    imbalance["proportion"] = imbalance["n"] / imbalance["n"].sum()
    save_csv(imbalance, out_res / "class_balance.csv")

    corr = df[metrics].corr(method="spearman")
    save_csv(corr.reset_index().rename(columns={"index": "metric"}), out_res / "corr_spearman_preview.csv")
    correlation_heatmap(corr, out_fig / "fig_correlation_heatmap_preview.png", dpi=cfg.dpi,
                        title="Spearman correlations (quality preview)")

    histogram_grid(df, metrics, out_fig / "fig_score_histograms.png", dpi=cfg.dpi)

    for metric in metrics:
        boxplot_by_group(df, metric, "model", out_fig / f"fig_box_{metric}_by_model.png", dpi=cfg.dpi)
        violin_by_group(df, metric, "model", out_fig / f"fig_violin_{metric}_by_model.png", dpi=cfg.dpi)

    # Density plots (matplotlib KDE-ish via histogram density + gaussian smooth optional)
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    axes_r = axes.ravel()
    for i, metric in enumerate(metrics):
        ax = axes_r[i]
        vals = df[metric].dropna().to_numpy()
        ax.hist(vals, bins=20, density=True, alpha=0.35, color="#4C72B0")
        if len(vals) > 1:
            xs = np.linspace(vals.min(), vals.max(), 200)
            # Simple Gaussian KDE.
            bandwidth = 1.06 * np.std(vals, ddof=1) * (len(vals) ** (-0.2))
            bandwidth = max(bandwidth, 1e-6)
            dens = np.zeros_like(xs)
            for v in vals:
                dens += np.exp(-0.5 * ((xs - v) / bandwidth) ** 2)
            dens /= (len(vals) * bandwidth * np.sqrt(2 * np.pi))
            ax.plot(xs, dens, color="#C44E52")
        ax.set_title(f"{metric} density")
    axes_r[-1].axis("off")
    save_fig(fig, out_fig / "fig_score_densities.png", dpi=cfg.dpi)

    summary = {
        "n_rows": int(len(df)),
        "missing": missing_df.to_dict(orient="records"),
        "outliers": outliers.to_dict(orient="records"),
    }
    save_json(summary, out_res / "data_quality_summary.json")
    logger.info("Part 1 data quality complete.")
    return summary
