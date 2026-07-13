"""Part 13 — Latent structure (PCA / EFA / optional CFA)."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.latent")

PERSONA_ITEMS = ["E", "D", "F"]  # constructs under investigation


def run_latent_structure(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "latent"
    out_fig = cfg.figures_dir / "latent"
    out_tab = cfg.tables_dir / "latent"

    # Include HuMT optionally as marker variable
    cols = ["E", "D", "F", "HuMT", "OA"]
    data = df[cols].dropna()
    scaler = StandardScaler()
    X = scaler.fit_transform(data[PERSONA_ITEMS])

    pca = PCA(random_state=cfg.random_seed)
    pca.fit(X)
    ev = pd.DataFrame(
        {
            "component": [f"PC{i+1}" for i in range(len(PERSONA_ITEMS))],
            "explained_variance_ratio": pca.explained_variance_ratio_,
            "explained_variance": pca.explained_variance_,
        }
    )
    loadings = pd.DataFrame(
        pca.components_.T,
        index=PERSONA_ITEMS,
        columns=[f"PC{i+1}" for i in range(len(PERSONA_ITEMS))],
    ).reset_index().rename(columns={"index": "variable"})
    save_csv(ev, out_res / "pca_variance.csv")
    save_csv(loadings, out_res / "pca_loadings.csv")

    # EFA via factor_analyzer if available
    efa_loadings = None
    try:
        from factor_analyzer import FactorAnalyzer
        from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

        chi2, p = calculate_bartlett_sphericity(data[PERSONA_ITEMS])
        kmo_all, kmo_model = calculate_kmo(data[PERSONA_ITEMS])
        fa = FactorAnalyzer(n_factors=min(3, len(PERSONA_ITEMS)), rotation="varimax")
        fa.fit(data[PERSONA_ITEMS])
        efa_loadings = pd.DataFrame(
            fa.loadings_,
            index=PERSONA_ITEMS,
            columns=[f"F{i+1}" for i in range(fa.loadings_.shape[1])],
        ).reset_index().rename(columns={"index": "variable"})
        save_csv(efa_loadings, out_res / "efa_loadings.csv")
        save_json(
            {"bartlett_chi2": float(chi2), "bartlett_p": float(p), "kmo": float(kmo_model)},
            out_res / "efa_diagnostics.json",
        )
        dataframe_to_latex(efa_loadings, out_tab / "efa_loadings.tex",
                           caption="Exploratory factor analysis loadings (varimax).",
                           label="tab:efa")
    except Exception as exc:
        logger.warning("EFA unavailable/failed: %s", exc)

    # CFA light check: correlations should not collapse to one factor
    corr = data[PERSONA_ITEMS].corr()
    save_csv(corr.reset_index(), out_res / "persona_item_corr.csv")
    distinct = bool((corr.abs().values < 0.95).all())  # crude distinctness flag

    # Scree plot
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(range(1, len(ev) + 1), ev["explained_variance_ratio"], "o-", color="#4C72B0")
    ax.set_xlabel("Component")
    ax.set_ylabel("Explained variance ratio")
    ax.set_title("PCA scree plot (E, D, F)")
    save_fig(fig, out_fig / "fig_pca_scree.png", dpi=cfg.dpi)

    # Loading heatmap-like bar
    fig, ax = plt.subplots(figsize=(6.5, 4))
    x = np.arange(len(PERSONA_ITEMS))
    width = 0.25
    for i, pc in enumerate([c for c in loadings.columns if c.startswith("PC")]):
        ax.bar(x + i * width, loadings[pc], width=width, label=pc)
    ax.set_xticks(x + width)
    ax.set_xticklabels(PERSONA_ITEMS)
    ax.legend()
    ax.set_title("PCA loadings")
    save_fig(fig, out_fig / "fig_pca_loadings.png", dpi=cfg.dpi)

    summary = {
        "variables": PERSONA_ITEMS,
        "pca_variance": ev.to_dict(orient="records"),
        "appear_distinct": distinct,
        "note": (
            "With only three PERSONA rating dimensions, CFA is weakly identified; "
            "EFA/PCA are reported as exploratory evidence of separable constructs."
        ),
    }
    save_json(summary, out_res / "latent_summary.json")
    dataframe_to_latex(ev, out_tab / "pca_variance.tex",
                       caption="PCA explained variance for PERSONA dimensions.",
                       label="tab:pca_var")
    logger.info("Part 13 latent structure complete.")
    return summary
