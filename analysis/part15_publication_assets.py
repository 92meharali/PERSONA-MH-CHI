"""Part 15/16 — Compile publication figure/table indices."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from .config import AnalysisConfig
from .utils import save_csv, save_json

logger = logging.getLogger("analysis.pub_assets")


def compile_publication_index(cfg: AnalysisConfig) -> dict[str, Any]:
    """Index generated figures/tables into a publication checklist."""

    figure_map = {
        "Figure 2": "data_quality/fig_score_histograms.png",
        "Figure 3": "model_comparison/fig_oa_model_ranking.png",
        "Figure 4": "correlation/fig_corr_spearman.png",
        "Figure 5": "regression/fig_regression_coefficients.png",
        "Figure 6": "feature_importance/fig_permutation_importance_rf.png",
        "Figure 7": "calibration/fig_calibration_curves.png",
        "Figure 8": "sensitivity/fig_sensitivity.png",
        "Figure 9": "ablation/fig_ablation_adjr2.png",
        "Figure 10": "model_comparison/fig_model_radar.png",
        "Figure 11": "adversarial/fig_adv_deception_means.png",
        "Figure 12": "clustering/fig_clusters_pca.png",
    }
    table_map = {
        "Table 1": "data_quality/descriptive_statistics.tex",
        "Table 2": "model_comparison/omnibus_tests.tex",
        "Table 3": "correlation/corr_spearman.tex",
        "Table 4": "regression/nested_model_comparison.tex",
        "Table 5": "incremental/incremental_validity.tex",
        "Table 6": "feature_importance/permutation_importance.tex",
        "Table 7": "ablation/ablation_results.tex",
        "Table 8": "hypotheses/hypothesis_tests.tex",
        "Table 9": "adversarial/adversarial_pairwise.tex",
        "Table 10": "clustering/kmeans_centers.tex",
    }

    fig_rows = []
    for label, rel in figure_map.items():
        path = cfg.figures_dir / rel
        fig_rows.append({"label": label, "path": str(path), "exists": path.exists()})
    tab_rows = []
    for label, rel in table_map.items():
        path = cfg.tables_dir / rel
        tab_rows.append({"label": label, "path": str(path), "exists": path.exists()})

    figs = pd.DataFrame(fig_rows)
    tabs = pd.DataFrame(tab_rows)
    save_csv(figs, cfg.results_dir / "publication_figure_index.csv")
    save_csv(tabs, cfg.results_dir / "publication_table_index.csv")
    save_json(
        {"figures": fig_rows, "tables": tab_rows},
        cfg.reports_dir / "publication_asset_index.json",
    )
    logger.info(
        "Publication assets indexed (%d/%d figures, %d/%d tables present).",
        int(figs["exists"].sum()),
        len(figs),
        int(tabs["exists"].sum()),
        len(tabs),
    )
    return {"figures": figs, "tables": tabs}
