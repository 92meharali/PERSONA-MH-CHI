"""Matplotlib-only plotting helpers (no seaborn)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def apply_style(font_size: int = 11) -> None:
    plt.rcParams.update(
        {
            "font.size": font_size,
            "axes.titlesize": font_size + 1,
            "axes.labelsize": font_size,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save_fig(fig: plt.Figure, path: Path, dpi: int = 300) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return path


def histogram_grid(
    df: pd.DataFrame,
    columns: Sequence[str],
    path: Path,
    *,
    dpi: int = 300,
) -> Path:
    n = len(columns)
    cols = min(3, n)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.2 * rows))
    axes_arr = np.atleast_1d(axes).ravel()
    for i, col in enumerate(columns):
        ax = axes_arr[i]
        vals = df[col].dropna().to_numpy()
        ax.hist(vals, bins=15, color="#4C72B0", edgecolor="white")
        ax.set_title(col)
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
    for j in range(i + 1, len(axes_arr)):
        axes_arr[j].axis("off")
    return save_fig(fig, path, dpi=dpi)


def boxplot_by_group(
    df: pd.DataFrame,
    value: str,
    group: str,
    path: Path,
    *,
    dpi: int = 300,
    title: Optional[str] = None,
) -> Path:
    groups = [g for g, _ in df.groupby(group)]
    data = [df.loc[df[group] == g, value].dropna().to_numpy() for g in groups]
    fig, ax = plt.subplots(figsize=(max(6, 1.4 * len(groups)), 4.5))
    ax.boxplot(data, tick_labels=[str(g) for g in groups], showfliers=True)
    ax.set_ylabel(value)
    ax.set_xlabel(group)
    ax.set_title(title or f"{value} by {group}")
    ax.tick_params(axis="x", rotation=30)
    return save_fig(fig, path, dpi=dpi)


def violin_by_group(
    df: pd.DataFrame,
    value: str,
    group: str,
    path: Path,
    *,
    dpi: int = 300,
) -> Path:
    groups = [g for g, _ in df.groupby(group)]
    data = [df.loc[df[group] == g, value].dropna().to_numpy() for g in groups]
    data = [d if len(d) else np.array([np.nan]) for d in data]
    fig, ax = plt.subplots(figsize=(max(6, 1.4 * len(groups)), 4.5))
    parts = ax.violinplot(data, showmeans=True, showmedians=True)
    for body in parts["bodies"]:
        body.set_facecolor("#4C72B0")
        body.set_alpha(0.7)
    ax.set_xticks(range(1, len(groups) + 1))
    ax.set_xticklabels([str(g) for g in groups], rotation=30, ha="right")
    ax.set_ylabel(value)
    ax.set_title(f"{value} violin by {group}")
    return save_fig(fig, path, dpi=dpi)


def correlation_heatmap(
    corr: pd.DataFrame,
    path: Path,
    *,
    dpi: int = 300,
    title: str = "Correlation heatmap",
) -> Path:
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    mat = corr.to_numpy(dtype=float)
    im = ax.imshow(mat, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title(title)
    return save_fig(fig, path, dpi=dpi)


def bar_values(
    labels: Sequence[str],
    values: Sequence[float],
    path: Path,
    *,
    ylabel: str,
    title: str,
    dpi: int = 300,
) -> Path:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(labels))
    ax.bar(x, values, color="#4C72B0")
    ax.set_xticks(x)
    ax.set_xticklabels(list(labels), rotation=30, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return save_fig(fig, path, dpi=dpi)


def radar_chart(
    categories: Sequence[str],
    series: dict[str, Sequence[float]],
    path: Path,
    *,
    dpi: int = 300,
    title: str = "Model profiles",
) -> Path:
    cats = list(categories)
    n = len(cats)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(polar=True))
    for name, values in series.items():
        vals = list(values) + [values[0]]
        ax.plot(angles, vals, label=name)
        ax.fill(angles, vals, alpha=0.12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats)
    ax.set_title(title)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1))
    return save_fig(fig, path, dpi=dpi)
