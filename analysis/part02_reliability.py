"""Part 2 — Annotation reliability (multi-annotator).

Gracefully skips formal IRR if only a single automated annotator is present.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from .config import AnalysisConfig
from .data_loader import CANONICAL_METRICS
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.reliability")


def _krippendorff_alpha_interval(reliability_data: np.ndarray) -> float:
    """Krippendorff's alpha for interval data (metrics as rows, units as columns).

    Implementation follows the coincidence-matrix formulation.
    """

    data = reliability_data.astype(float)
    # Drop units with fewer than 2 ratings
    mask = np.sum(~np.isnan(data), axis=0) >= 2
    data = data[:, mask]
    if data.size == 0:
        return float("nan")

    values = data[~np.isnan(data)]
    if len(values) == 0:
        return float("nan")
    unique = np.unique(values)
    value_map = {v: i for i, v in enumerate(unique)}
    m = len(unique)
    coincidence = np.zeros((m, m), dtype=float)

    n_units = data.shape[1]
    for unit in range(n_units):
        ratings = data[:, unit]
        ratings = ratings[~np.isnan(ratings)]
        n_u = len(ratings)
        if n_u < 2:
            continue
        for i in range(n_u):
            for j in range(n_u):
                if i == j:
                    continue
                vi = value_map[ratings[i]]
                vj = value_map[ratings[j]]
                coincidence[vi, vj] += 1.0 / (n_u - 1)

    n_pair = coincidence.sum()
    if n_pair == 0:
        return float("nan")
    # Observed disagreement
    do = 0.0
    de = 0.0
    n_c = coincidence.sum(axis=1)
    for i in range(m):
        for j in range(m):
            delta = (unique[i] - unique[j]) ** 2
            do += coincidence[i, j] * delta
            de += n_c[i] * n_c[j] * delta
    do /= n_pair
    de /= (n_pair * (n_pair - 1)) if n_pair > 1 else np.nan
    if de == 0 or np.isnan(de):
        return float("nan")
    return float(1 - do / de)


def run_reliability(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "reliability"
    out_tab = cfg.tables_dir / "reliability"

    n_annotators = df["annotator_id"].nunique(dropna=True)
    summary: dict[str, Any] = {
        "n_annotators": int(n_annotators),
        "status": "skipped_single_annotator",
        "note": (
            "Current PERSONA CSVs contain a single automated pilot annotator. "
            "Krippendorff/Kappa/ICC will be computed when multi-annotator columns are present."
        ),
    }

    if n_annotators < 2:
        # Still write placeholder tables for paper reproducibility scaffolding.
        placeholder = pd.DataFrame(
            [
                {
                    "metric": m,
                    "krippendorff_alpha": np.nan,
                    "cohen_kappa": np.nan,
                    "weighted_kappa": np.nan,
                    "icc": np.nan,
                    "status": "insufficient_annotators",
                }
                for m in CANONICAL_METRICS
                if m != "HuMT"
            ]
        )
        save_csv(placeholder, out_res / "reliability_metrics.csv")
        dataframe_to_latex(
            placeholder,
            out_tab / "reliability_metrics.tex",
            caption="Inter-rater reliability (pending multi-annotator labels).",
            label="tab:reliability",
        )
        save_json(summary, out_res / "reliability_summary.json")
        logger.warning("Part 2 reliability skipped: only %d annotator(s).", n_annotators)
        return summary

    # Multi-annotator path (future-proof).
    rows = []
    for metric in [m for m in CANONICAL_METRICS if m != "HuMT"]:
        # Expect columns like metric rated per annotator wide format or long format.
        # Here we assume long format with one score column shared.
        pivoted = df.pivot_table(
            index=["prompt_id", "model"],
            columns="annotator_id",
            values=metric,
            aggfunc="mean",
        )
        mat = pivoted.to_numpy().T  # annotators x units
        alpha = _krippendorff_alpha_interval(mat)
        rows.append({"metric": metric, "krippendorff_alpha": alpha})
    result = pd.DataFrame(rows)
    save_csv(result, out_res / "reliability_metrics.csv")
    summary["status"] = "computed"
    summary["metrics"] = result.to_dict(orient="records")
    save_json(summary, out_res / "reliability_summary.json")
    logger.info("Part 2 reliability complete.")
    return summary
