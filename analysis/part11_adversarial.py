"""Part 11 — Adversarial dataset comparisons (EVAL vs ADV / PERSONA-ADV)."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .config import AnalysisConfig
from .data_loader import CANONICAL_METRICS
from .plotting import boxplot_by_group, save_fig
from .utils import cliffs_delta, cohens_d, dataframe_to_latex, hedges_g, mean_ci, save_csv, save_json

logger = logging.getLogger("analysis.adversarial")


def run_adversarial(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "adversarial"
    out_fig = cfg.figures_dir / "adversarial"
    out_tab = cfg.tables_dir / "adversarial"

    families = sorted(df["dataset_family"].unique().tolist())
    desc_rows = []
    for fam in families:
        for metric in CANONICAL_METRICS:
            stats_m = mean_ci(df.loc[df["dataset_family"] == fam, metric])
            desc_rows.append({"dataset_family": fam, "metric": metric, **stats_m})
    desc = pd.DataFrame(desc_rows)
    save_csv(desc, out_res / "dataset_descriptives.csv")

    # Pairwise family contrasts
    pair_rows = []
    unique = families
    for i, a in enumerate(unique):
        for b in unique[i + 1 :]:
            for metric in CANONICAL_METRICS:
                xa = df.loc[df["dataset_family"] == a, metric].dropna().to_numpy()
                xb = df.loc[df["dataset_family"] == b, metric].dropna().to_numpy()
                if len(xa) < 2 or len(xb) < 2:
                    continue
                u, p = stats.mannwhitneyu(xa, xb, alternative="two-sided")
                pair_rows.append(
                    {
                        "metric": metric,
                        "dataset_a": a,
                        "dataset_b": b,
                        "mean_a": float(np.mean(xa)),
                        "mean_b": float(np.mean(xb)),
                        "u_stat": float(u),
                        "p": float(p),
                        "cohens_d": cohens_d(xa, xb),
                        "hedges_g": hedges_g(xa, xb),
                        "cliffs_delta": cliffs_delta(xa, xb),
                    }
                )
    pairs = pd.DataFrame(pair_rows)
    save_csv(pairs, out_res / "dataset_pairwise.csv")
    dataframe_to_latex(pairs, out_tab / "adversarial_pairwise.tex",
                       caption="Pairwise dataset contrasts for HuMT and PERSONA metrics.",
                       label="tab:adv_pairwise")

    # Focal hypothesis: D increases on adversarial prompts
    focal = pairs[(pairs["metric"] == "D")].copy()
    save_csv(focal, out_res / "deception_adversarial_tests.csv")

    for metric in ["D", "OA", "E", "F", "HuMT"]:
        boxplot_by_group(df, metric, "dataset_family",
                         out_fig / f"fig_adv_box_{metric}.png", dpi=cfg.dpi,
                         title=f"{metric} by dataset family")

    # Bar mean D by dataset
    dmeans = desc[desc["metric"] == "D"]
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.bar(dmeans["dataset_family"], dmeans["mean"],
           yerr=[dmeans["mean"] - dmeans["ci_low"], dmeans["ci_high"] - dmeans["mean"]],
           color="#C44E52", capsize=4)
    ax.set_ylabel("Mean Deception Risk (D)")
    ax.set_title("Deception Risk across dataset families")
    ax.tick_params(axis="x", rotation=20)
    save_fig(fig, out_fig / "fig_adv_deception_means.png", dpi=cfg.dpi)

    note = ""
    if "PERSONA-ADV" not in families:
        note = "PERSONA-ADV prompts are not yet present; comparisons use available dataset families."
    summary = {"families": families, "note": note}
    save_json(summary, out_res / "adversarial_summary.json")
    logger.info("Part 11 adversarial complete. %s", note)
    return {"pairs": pairs, "desc": desc}
