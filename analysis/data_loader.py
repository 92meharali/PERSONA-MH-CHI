"""Data loading and canonical column renaming for PERSONA analyses."""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

from .config import AnalysisConfig

logger = logging.getLogger("analysis.data")

CANONICAL_METRICS = ("HuMT", "E", "D", "F", "OA")


def load_annotation_frame(cfg: AnalysisConfig) -> pd.DataFrame:
    """Load annotation CSV and add canonical metric column aliases.

    Never modifies the source CSV on disk.
    """

    if not cfg.data_csv.exists():
        raise FileNotFoundError(f"Annotation CSV not found: {cfg.data_csv}")

    # Leading '# ...' provenance comments are allowed in annotation CSVs.
    df = pd.read_csv(cfg.data_csv, comment="#")
    logger.info("Loaded %d rows from %s", len(df), cfg.data_csv)

    rename_map = {
        cfg.metrics.get("HuMT", "humt_score"): "HuMT",
        cfg.metrics.get("E", "Empathy_score"): "E",
        cfg.metrics.get("D", "DeceptionRisk_score"): "D",
        cfg.metrics.get("F", "ContextualFit_score"): "F",
        cfg.metrics.get("OA", "OverallAppropriateness_score"): "OA",
    }
    missing = [src for src in rename_map if src not in df.columns]
    if missing:
        raise KeyError(f"Missing required metric columns: {missing}")

    out = df.copy()
    for src, dst in rename_map.items():
        out[dst] = pd.to_numeric(out[src], errors="coerce")

    # Unified category for prompt family / situation.
    if "topic" in out.columns:
        out["category"] = out["topic"].fillna("").astype(str)
    else:
        out["category"] = ""
    if "failure_mode" in out.columns:
        mask = out["failure_mode"].notna() & (out["failure_mode"].astype(str).str.strip() != "")
        out.loc[mask, "category"] = out.loc[mask, "failure_mode"].astype(str)

    if "source_set" in out.columns:
        out["dataset"] = out["source_set"].astype(str)
    else:
        out["dataset"] = "unknown"

    # Normalize dataset labels for adversarial analyses.
    out["dataset_family"] = out["dataset"].map(_dataset_family)

    # Final published scores are aggregated across 5 human annotators
    # (mean then integer-masked). Raw per-annotator columns are not present,
    # so reliability modules still cannot compute IRR from this frame alone.
    out["annotator_id"] = "human_aggregate_5rater"
    out["annotation_protocol"] = "5rater_mean_integer_mask"

    logger.info(
        "Models=%s | datasets=%s",
        sorted(out["model"].unique().tolist()),
        sorted(out["dataset_family"].unique().tolist()),
    )
    return out


def _dataset_family(value: str) -> str:
    text = str(value).lower()
    if "persona-adv" in text or "persona_adv" in text:
        return "PERSONA-ADV"
    if "adv" in text:
        return "CounselBench-ADV"
    if "eval" in text:
        return "CounselBench-EVAL"
    return str(value)


def metric_columns(df: Optional[pd.DataFrame] = None) -> list[str]:
    return list(CANONICAL_METRICS)
