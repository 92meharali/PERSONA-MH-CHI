"""Shared utilities: IO, stats helpers, latex tables, logging."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Iterable, Optional

import numpy as np
import pandas as pd


def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("analysis")
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level, logging.INFO))
    logger.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    )
    logger.addHandler(handler)
    return logger


def set_seed(seed: int) -> np.random.Generator:
    np.random.seed(seed)
    return np.random.default_rng(seed)


def save_csv(df: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def save_json(payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, default=_json_default)
        handle.write("\n")
    return path


def _json_default(obj: Any) -> Any:
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, Path):
        return str(obj)
    return str(obj)


def mean_ci(values: Iterable[float], alpha: float = 0.05) -> dict[str, float]:
    arr = np.asarray(list(values), dtype=float)
    arr = arr[~np.isnan(arr)]
    n = len(arr)
    if n == 0:
        return {"mean": np.nan, "std": np.nan, "median": np.nan, "iqr": np.nan,
                "ci_low": np.nan, "ci_high": np.nan, "n": 0}
    mean = float(np.mean(arr))
    std = float(np.std(arr, ddof=1)) if n > 1 else 0.0
    median = float(np.median(arr))
    q1, q3 = np.percentile(arr, [25, 75])
    se = std / np.sqrt(n) if n > 0 else np.nan
    # Normal approx CI; adequate for descriptive summaries.
    z = 1.959963984540054
    return {
        "mean": mean,
        "std": std,
        "median": median,
        "iqr": float(q3 - q1),
        "ci_low": mean - z * se,
        "ci_high": mean + z * se,
        "n": n,
    }


def dataframe_to_latex(
    df: pd.DataFrame,
    path: Path,
    *,
    caption: str,
    label: str,
    float_format: str = "%.3f",
) -> Path:
    """Write a simple booktabs-like LaTeX tabular without Jinja/Styler."""

    path.parent.mkdir(parents=True, exist_ok=True)
    frame = df.copy()
    for col in frame.columns:
        if pd.api.types.is_float_dtype(frame[col]):
            frame[col] = frame[col].map(lambda x: "" if pd.isna(x) else (float_format % x))
        else:
            frame[col] = frame[col].map(lambda x: "" if pd.isna(x) else str(x))

    cols = [str(c) for c in frame.columns]
    # Escape latex specials lightly
    def esc(text: str) -> str:
        return (
            text.replace("\\", "\\textbackslash{}")
            .replace("_", "\\_")
            .replace("%", "\\%")
            .replace("&", "\\&")
        )

    header = " & ".join(esc(c) for c in cols) + " \\\\"
    body_lines = []
    for _, row in frame.iterrows():
        body_lines.append(" & ".join(esc(str(v)) for v in row.tolist()) + " \\\\")
    colspec = "l" * len(cols)
    latex = "\n".join(
        [
            "\\begin{table}[t]",
            "\\centering",
            f"\\caption{{{esc(caption)}}}",
            f"\\label{{{label}}}",
            f"\\begin{{tabular}}{{{colspec}}}",
            "\\toprule",
            header,
            "\\midrule",
            *body_lines,
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            "",
        ]
    )
    path.write_text(latex, encoding="utf-8")
    return path


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[~np.isnan(a)]
    b = b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    pooled = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled == 0:
        return 0.0
    return float((np.mean(a) - np.mean(b)) / pooled)


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    d = cohens_d(a, b)
    n = len(a) + len(b)
    if n <= 2 or np.isnan(d):
        return float("nan")
    correction = 1 - (3 / (4 * (n - 2) - 1))
    return float(d * correction)


def cliffs_delta(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[~np.isnan(a)]
    b = b[~np.isnan(b)]
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    # Efficient pairwise domination count.
    more = 0
    less = 0
    for x in a:
        more += int(np.sum(x > b))
        less += int(np.sum(x < b))
    return float((more - less) / (len(a) * len(b)))


def safe_pvalue(p: Optional[float]) -> float:
    if p is None or (isinstance(p, float) and np.isnan(p)):
        return float("nan")
    return float(p)
