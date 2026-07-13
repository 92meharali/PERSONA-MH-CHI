"""Orchestrate the full PERSONA analysis pipeline."""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

from tqdm import tqdm

from .config import AnalysisConfig, ensure_output_dirs, load_config
from .data_loader import load_annotation_frame
from .part01_data_quality import run_data_quality
from .part02_reliability import run_reliability
from .part03_model_comparison import run_model_comparison
from .part04_correlation import run_correlation
from .part05_regression import run_incremental_validity, run_regression
from .part07_feature_importance import run_feature_importance
from .part08_calibration import run_calibration
from .part09_sensitivity import run_sensitivity
from .part10_ablation import run_ablation
from .part11_adversarial import run_adversarial
from .part12_clustering import run_clustering
from .part13_latent import run_latent_structure
from .part14_hypotheses import run_hypothesis_testing
from .part15_publication_assets import compile_publication_index
from .part17_report import generate_report
from .plotting import apply_style
from .utils import save_json, set_seed, setup_logging

logger = logging.getLogger("analysis.pipeline")


def run_all(cfg: Optional[AnalysisConfig] = None) -> dict[str, Any]:
    cfg = cfg or load_config()
    setup_logging(cfg.log_level)
    apply_style(cfg.font_size)
    set_seed(cfg.random_seed)
    ensure_output_dirs(cfg)

    logger.info("Loading data from %s", cfg.data_csv)
    df = load_annotation_frame(cfg)

    outputs: dict[str, Any] = {}
    steps = [
        ("data_quality", lambda: run_data_quality(df, cfg)),
        ("reliability", lambda: run_reliability(df, cfg)),
        ("model_comparison", lambda: run_model_comparison(df, cfg)),
        ("correlation", lambda: run_correlation(df, cfg)),
        ("regression", lambda: run_regression(df, cfg)),
        ("feature_importance", lambda: run_feature_importance(df, cfg)),
        ("calibration", lambda: run_calibration(df, cfg)),
        ("sensitivity", lambda: run_sensitivity(df, cfg)),
        ("ablation", lambda: run_ablation(df, cfg)),
        ("adversarial", lambda: run_adversarial(df, cfg)),
        ("clustering", lambda: run_clustering(df, cfg)),
        ("latent_structure", lambda: run_latent_structure(df, cfg)),
    ]

    # Filter by config flags when present
    enabled = []
    for name, fn in steps:
        flag = cfg.parts.get(name, True)
        # config uses incremental_validity separately
        if name == "regression":
            flag = cfg.parts.get("regression", True)
        if flag:
            enabled.append((name, fn))

    start = time.time()
    regression_out = None
    for name, fn in tqdm(enabled, desc="PERSONA analysis parts"):
        logger.info("Running part: %s", name)
        t0 = time.time()
        result = fn()
        outputs[name] = result
        if name == "regression":
            regression_out = result
            if cfg.parts.get("incremental_validity", True):
                outputs["incremental_validity"] = run_incremental_validity(df, cfg, regression_out)
        logger.info("Finished %s in %.1fs", name, time.time() - t0)

    if cfg.parts.get("hypothesis_testing", True):
        outputs["hypotheses"] = run_hypothesis_testing(df, cfg, outputs)

    if cfg.parts.get("figures", True) or cfg.parts.get("tables", True):
        outputs["publication_assets"] = compile_publication_index(cfg)

    if cfg.parts.get("report", True):
        report_path = generate_report(cfg)
        outputs["report_path"] = str(report_path)

    summary = {
        "n_rows": int(len(df)),
        "parts_run": list(outputs.keys()),
        "elapsed_sec": time.time() - start,
        "figures_dir": str(cfg.figures_dir),
        "tables_dir": str(cfg.tables_dir),
        "results_dir": str(cfg.results_dir),
        "reports_dir": str(cfg.reports_dir),
    }
    save_json(summary, cfg.reports_dir / "run_summary.json")
    logger.info("Full analysis complete in %.1fs", summary["elapsed_sec"])
    return summary
