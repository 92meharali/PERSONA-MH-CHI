"""Configuration for the PERSONA analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


@dataclass(frozen=True)
class AnalysisConfig:
    repo_root: Path
    data_csv: Path
    figures_dir: Path
    tables_dir: Path
    results_dir: Path
    reports_dir: Path
    random_seed: int
    n_bootstrap: int
    n_cv_folds: int
    n_permutation: int
    columns: dict[str, str]
    metrics: dict[str, str]
    parts: dict[str, bool]
    log_level: str
    dpi: int
    figsize: tuple[float, float]
    font_size: int


def _resolve(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (root / path).resolve()


def load_config(config_path: Path | str | None = None) -> AnalysisConfig:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    path = path.resolve()
    with path.open("r", encoding="utf-8") as handle:
        raw: dict[str, Any] = yaml.safe_load(handle) or {}

    repo_root = Path(raw.get("paths", {}).get("repo_root", ".")).resolve()
    if raw.get("paths", {}).get("repo_root", ".") in (".", "./"):
        repo_root = path.parent.parent.resolve()

    paths = raw.get("paths", {})
    repro = raw.get("reproducibility", {})
    plotting = raw.get("plotting", {})
    logging_cfg = raw.get("logging", {})

    figsize = plotting.get("figsize", [8, 5])
    return AnalysisConfig(
        repo_root=repo_root,
        data_csv=_resolve(repo_root, paths.get("data_csv", "annotations_csv/all_models_persona_annotations.csv")),
        figures_dir=_resolve(repo_root, paths.get("figures_dir", "figures")),
        tables_dir=_resolve(repo_root, paths.get("tables_dir", "tables")),
        results_dir=_resolve(repo_root, paths.get("results_dir", "results")),
        reports_dir=_resolve(repo_root, paths.get("reports_dir", "reports")),
        random_seed=int(repro.get("random_seed", 42)),
        n_bootstrap=int(repro.get("n_bootstrap", 500)),
        n_cv_folds=int(repro.get("n_cv_folds", 5)),
        n_permutation=int(repro.get("n_permutation", 50)),
        columns=dict(raw.get("columns", {})),
        metrics=dict(raw.get("metrics", {})),
        parts=dict(raw.get("parts", {})),
        log_level=str(logging_cfg.get("level", "INFO")).upper(),
        dpi=int(plotting.get("dpi", 300)),
        figsize=(float(figsize[0]), float(figsize[1])),
        font_size=int(plotting.get("font_size", 11)),
    )


def ensure_output_dirs(cfg: AnalysisConfig) -> None:
    for directory in (
        cfg.figures_dir,
        cfg.tables_dir,
        cfg.results_dir,
        cfg.reports_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)
        for sub in ("data_quality", "reliability", "model_comparison", "correlation",
                    "regression", "incremental", "feature_importance", "calibration",
                    "sensitivity", "ablation", "adversarial", "clustering", "latent",
                    "hypotheses"):
            (cfg.results_dir / sub).mkdir(parents=True, exist_ok=True)
            (cfg.figures_dir / sub).mkdir(parents=True, exist_ok=True)
            (cfg.tables_dir / sub).mkdir(parents=True, exist_ok=True)
