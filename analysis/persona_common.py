"""Shared configuration, IO, and statistical helpers for the PERSONA phase pipeline.

This module is intentionally dependency-light and deterministic. Every random
operation takes an explicit seed so that all paper-facing numbers are
reproducible from a clean environment.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
ANALYSIS_DIR = Path(__file__).resolve().parent
ROOT = ANALYSIS_DIR.parent
DATA_DIR = ROOT / "data"
CLEAN_DIR = DATA_DIR / "clean_domains"

PROCESSED_DIR = ANALYSIS_DIR / "processed"
OUT_DIR = ANALYSIS_DIR / "outputs"
TABLE_DIR = OUT_DIR / "tables"
FIGURE_DIR = OUT_DIR / "figures"
REPORT_DIR = OUT_DIR / "reports"

for _d in (PROCESSED_DIR, TABLE_DIR, FIGURE_DIR, REPORT_DIR):
    _d.mkdir(parents=True, exist_ok=True)

RATINGS_LONG = PROCESSED_DIR / "persona_ratings_long.csv"
CONSENSUS = PROCESSED_DIR / "persona_all.csv"

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
SEED = 42
N_BOOT = 1000
CV_FOLDS = 5
CV_REPEATS = 20

DIMENSIONS = ["OA", "E", "D", "F"]
PROFILE = ["H", "E", "D", "F"]
DOMAINS = ["mental_health", "education", "health"]
DOMAIN_LABEL = {
    "mental_health": "Mental health",
    "education": "Education",
    "health": "Health",
}
RATING_MIN, RATING_MAX = 1, 5

# Canonical model families. The three domains use different surface spellings
# for the same underlying systems; this maps them onto one label set.
MODEL_FAMILY = {
    "claude_opus_4_8": "claude_opus_4_8",
    "glm": "glm",
    "glm_5_2": "glm",
    "gpt_5_6_sol": "gpt_5_6",
    "gpt_5_6": "gpt_5_6",
}


# --------------------------------------------------------------------------
# Text normalisation (used for HuMT joins and prompt grouping)
# --------------------------------------------------------------------------
_QUOTES = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2026": "...",
    "\u00a0": " ",
}


def norm_text(value: object) -> str:
    """Aggressively normalise text so that cosmetic differences do not block joins."""
    text = unicodedata.normalize("NFKC", "" if value is None else str(value))
    for bad, good in _QUOTES.items():
        text = text.replace(bad, good)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# --------------------------------------------------------------------------
# Small IO helpers
# --------------------------------------------------------------------------
def save_table(frame: pd.DataFrame, name: str) -> Path:
    path = TABLE_DIR / f"{name}.csv"
    frame.to_csv(path, index=False)
    return path


def save_markdown(text: str, name: str) -> Path:
    path = REPORT_DIR / f"{name}.md"
    path.write_text(text, encoding="utf-8")
    return path


def save_json(payload: dict, name: str) -> Path:
    path = OUT_DIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, default=_json_default), encoding="utf-8")
    return path


def _json_default(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if math.isnan(float(value)) else float(value)
    if isinstance(value, (np.ndarray,)):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Not JSON serialisable: {type(value)}")


def load_consensus() -> pd.DataFrame:
    if not CONSENSUS.exists():
        raise FileNotFoundError(
            f"{CONSENSUS} missing. Run `python -m analysis.build_dataset` first."
        )
    return pd.read_csv(CONSENSUS)


def load_ratings() -> pd.DataFrame:
    if not RATINGS_LONG.exists():
        raise FileNotFoundError(
            f"{RATINGS_LONG} missing. Run `python -m analysis.build_dataset` first."
        )
    return pd.read_csv(RATINGS_LONG)


# --------------------------------------------------------------------------
# Deterministic grouped cross-validation
# --------------------------------------------------------------------------
def grouped_folds(groups: np.ndarray, n_splits: int, rng: np.random.Generator) -> list[np.ndarray]:
    """Assign every row a fold index, splitting on whole groups.

    Implemented locally rather than via sklearn's GroupKFold because the
    library's grouping heuristic has changed between versions, which made
    previously committed cross-validation numbers irreproducible.
    """
    groups = np.asarray(groups)
    unique = np.array(sorted(set(groups.tolist())))
    shuffled = unique.copy()
    rng.shuffle(shuffled)
    chunks = np.array_split(shuffled, n_splits)
    fold_of_group = {}
    for fold, chunk in enumerate(chunks):
        for g in chunk:
            fold_of_group[g] = fold
    return np.array([fold_of_group[g] for g in groups])


def ols_fit_predict(x_train, y_train, x_test):
    """Least-squares linear model with intercept; returns held-out predictions."""
    x_train = np.asarray(x_train, dtype=float)
    x_test = np.asarray(x_test, dtype=float)
    a_train = np.column_stack([np.ones(len(x_train)), x_train])
    a_test = np.column_stack([np.ones(len(x_test)), x_test])
    beta, *_ = np.linalg.lstsq(a_train, np.asarray(y_train, dtype=float), rcond=None)
    return a_test @ beta


# --------------------------------------------------------------------------
# Metrics
# --------------------------------------------------------------------------
def r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - y_true.mean()) ** 2))
    return float("nan") if ss_tot == 0 else 1.0 - ss_res / ss_tot


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true, float) - np.asarray(y_pred, float)) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(np.asarray(y_true, float) - np.asarray(y_pred, float))))


# --------------------------------------------------------------------------
# Cluster bootstrap
# --------------------------------------------------------------------------
def cluster_bootstrap_indices(
    groups: np.ndarray, rng: np.random.Generator, n_boot: int
):
    """Yield row-index arrays produced by resampling whole clusters with replacement."""
    groups = np.asarray(groups)
    unique = np.array(sorted(set(groups.tolist())))
    index_of_group = {g: np.flatnonzero(groups == g) for g in unique}
    for _ in range(n_boot):
        picked = rng.choice(unique, size=len(unique), replace=True)
        yield np.concatenate([index_of_group[g] for g in picked])


def percentile_ci(values, alpha: float = 0.05) -> tuple[float, float]:
    clean = np.asarray([v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))], dtype=float)
    if clean.size < 2:
        return (float("nan"), float("nan"))
    return (
        float(np.percentile(clean, 100 * alpha / 2)),
        float(np.percentile(clean, 100 * (1 - alpha / 2))),
    )


# --------------------------------------------------------------------------
# Multiple-comparison correction
# --------------------------------------------------------------------------
def holm_adjust(pvalues: list[float]) -> list[float]:
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    n = len(pvalues)
    adjusted = [float("nan")] * n
    running = 0.0
    for rank, idx in enumerate(order):
        value = (n - rank) * pvalues[idx]
        running = max(running, min(value, 1.0))
        adjusted[idx] = running
    return adjusted


def bh_adjust(pvalues: list[float]) -> list[float]:
    n = len(pvalues)
    order = sorted(range(n), key=lambda i: pvalues[i], reverse=True)
    adjusted = [float("nan")] * n
    running = 1.0
    for rank, idx in enumerate(order):
        value = pvalues[idx] * n / (n - rank)
        running = min(running, min(value, 1.0))
        adjusted[idx] = running
    return adjusted


def env_versions() -> dict[str, str]:
    import importlib

    versions = {}
    for name in ("numpy", "pandas", "scipy", "sklearn", "statsmodels", "matplotlib", "pingouin"):
        try:
            versions[name] = getattr(importlib.import_module(name), "__version__", "unknown")
        except Exception:  # pragma: no cover
            versions[name] = "not installed"
    try:
        import krippendorff  # noqa: F401

        versions["krippendorff"] = "installed"
    except Exception:  # pragma: no cover
        versions["krippendorff"] = "not installed"
    import sys

    versions["python"] = sys.version.split()[0]
    return versions
