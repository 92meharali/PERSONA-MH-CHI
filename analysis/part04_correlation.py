"""Part 4 — Correlation analysis among HuMT and PERSONA metrics."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_selection import mutual_info_regression

from .config import AnalysisConfig
from .data_loader import CANONICAL_METRICS
from .plotting import correlation_heatmap, save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.correlation")


def _partial_corr(df: pd.DataFrame, x: str, y: str, covariates: list[str]) -> float:
    from numpy.linalg import lstsq

    data = df[[x, y] + covariates].dropna()
    if len(data) < len(covariates) + 3:
        return float("nan")
    Z = data[covariates].to_numpy()
    Z = np.column_stack([np.ones(len(Z)), Z])
    rx = data[x].to_numpy() - Z @ lstsq(Z, data[x].to_numpy(), rcond=None)[0]
    ry = data[y].to_numpy() - Z @ lstsq(Z, data[y].to_numpy(), rcond=None)[0]
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def _distance_correlation(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    n = len(x)
    if n < 3:
        return float("nan")
    a = np.abs(x[:, None] - x[None, :])
    b = np.abs(y[:, None] - y[None, :])
    A = a - a.mean(axis=0) - a.mean(axis=1)[:, None] + a.mean()
    B = b - b.mean(axis=0) - b.mean(axis=1)[:, None] + b.mean()
    dcov2 = (A * B).mean()
    dvarx = (A * A).mean()
    dvary = (B * B).mean()
    if dvarx <= 0 or dvary <= 0:
        return float("nan")
    return float(np.sqrt(dcov2) / np.sqrt(np.sqrt(dvarx) * np.sqrt(dvary)))


def run_correlation(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "correlation"
    out_fig = cfg.figures_dir / "correlation"
    out_tab = cfg.tables_dir / "correlation"
    metrics = list(CANONICAL_METRICS)
    data = df[metrics].dropna()

    pearson = data.corr(method="pearson")
    spearman = data.corr(method="spearman")
    kendall = data.corr(method="kendall")
    for name, mat in [("pearson", pearson), ("spearman", spearman), ("kendall", kendall)]:
        save_csv(mat.reset_index().rename(columns={"index": "metric"}), out_res / f"corr_{name}.csv")
        dataframe_to_latex(mat.reset_index(), out_tab / f"corr_{name}.tex",
                           caption=f"{name.title()} correlation matrix.",
                           label=f"tab:corr_{name}")
        correlation_heatmap(mat, out_fig / f"fig_corr_{name}.png", dpi=cfg.dpi,
                            title=f"{name.title()} correlations")

    # Pairwise extended stats
    rows = []
    for i, a in enumerate(metrics):
        for b in metrics[i + 1 :]:
            xa = data[a].to_numpy()
            xb = data[b].to_numpy()
            pr, pp = stats.pearsonr(xa, xb)
            sr, sp = stats.spearmanr(xa, xb)
            kr, kp = stats.kendalltau(xa, xb)
            covars = [m for m in metrics if m not in (a, b)]
            partial = _partial_corr(data, a, b, covars)
            # MI: predict b from a
            mi = float(mutual_info_regression(xa.reshape(-1, 1), xb, random_state=cfg.random_seed)[0])
            dcor = _distance_correlation(xa, xb)
            rows.append(
                {
                    "var_a": a,
                    "var_b": b,
                    "pearson_r": pr,
                    "pearson_p": pp,
                    "spearman_r": sr,
                    "spearman_p": sp,
                    "kendall_tau": kr,
                    "kendall_p": kp,
                    "partial_r": partial,
                    "distance_corr": dcor,
                    "mutual_info": mi,
                }
            )
    pairwise = pd.DataFrame(rows)
    save_csv(pairwise, out_res / "pairwise_extended.csv")
    dataframe_to_latex(pairwise, out_tab / "pairwise_extended.tex",
                       caption="Extended pairwise association measures.",
                       label="tab:pairwise_assoc")

    # Pair plot
    n = len(metrics)
    fig, axes = plt.subplots(n, n, figsize=(2.2 * n, 2.2 * n))
    for i, yi in enumerate(metrics):
        for j, xj in enumerate(metrics):
            ax = axes[i, j]
            if i == j:
                ax.hist(data[yi], bins=12, color="#4C72B0", edgecolor="white")
            else:
                ax.scatter(data[xj], data[yi], s=8, alpha=0.35, color="#4C72B0")
            if i == n - 1:
                ax.set_xlabel(xj)
            else:
                ax.set_xticklabels([])
            if j == 0:
                ax.set_ylabel(yi)
            else:
                ax.set_yticklabels([])
    save_fig(fig, out_fig / "fig_pairplot.png", dpi=cfg.dpi)

    # Network graph of |spearman| edges
    G = nx.Graph()
    for m in metrics:
        G.add_node(m)
    for _, row in pairwise.iterrows():
        w = abs(float(row["spearman_r"]))
        if w >= 0.2:
            G.add_edge(row["var_a"], row["var_b"], weight=w)
    fig, ax = plt.subplots(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=cfg.random_seed)
    weights = [G[u][v]["weight"] * 3 for u, v in G.edges()]
    nx.draw_networkx(G, pos, ax=ax, node_color="#4C72B0", edge_color="#999999",
                     width=weights, with_labels=True, font_color="white")
    ax.set_title("Association network (|Spearman| ≥ 0.2)")
    ax.axis("off")
    save_fig(fig, out_fig / "fig_corr_network.png", dpi=cfg.dpi)

    summary = {"n": int(len(data)), "metrics": metrics}
    save_json(summary, out_res / "correlation_summary.json")
    logger.info("Part 4 correlation complete.")
    return {"pairwise": pairwise, "spearman": spearman}
