"""Part 17 — Auto-generated analysis report."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

import pandas as pd

from .config import AnalysisConfig

logger = logging.getLogger("analysis.report")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_csv(path: Path) -> Optional[pd.DataFrame]:
    if not path.exists():
        return None
    return pd.read_csv(path)


def generate_report(cfg: AnalysisConfig) -> Path:
    out = cfg.reports_dir / "analysis_report.md"
    lines: list[str] = []
    lines.append("# PERSONA Analysis Report\n")
    lines.append(
        "Automated statistical analysis of HuMT human-likeness and PERSONA "
        "dimensions (E, D, F, OA) for mental-health AI responses.\n"
    )

    # Data quality
    lines.append("## 1. Major findings\n")
    dq = _read_json(cfg.results_dir / "data_quality" / "data_quality_summary.json")
    lines.append(f"- Analyzed **{dq.get('n_rows', 'N/A')}** annotated responses.\n")

    hyp = _read_csv(cfg.results_dir / "hypotheses" / "hypothesis_tests.csv")
    if hyp is not None:
        lines.append("### Hypothesis outcomes\n")
        for _, row in hyp.iterrows():
            p = row["p_value"]
            sig = "significant" if pd.notna(p) and p < 0.05 else "not significant / N/A"
            lines.append(
                f"- **{row['hypothesis_id']}** ({row['hypothesis']}): "
                f"{row['test']} = {row['statistic']}, p={row['p_value']} → {sig}.\n"
            )

    inc = _read_json(cfg.results_dir / "incremental" / "incremental_validity.json")
    if inc:
        lines.append("### Incremental validity\n")
        lines.append(
            f"- Δ Adjusted R² (M4 PERSONA full vs M1 HuMT-only) = "
            f"**{inc.get('delta_adj_r2', 'N/A')}** "
            f"(base={inc.get('base_adj_r2')}, full={inc.get('full_adj_r2')}).\n"
        )
        lines.append(f"- {inc.get('interpretation', '')}\n")

    abl = _read_csv(cfg.results_dir / "ablation" / "ablation_results.csv")
    if abl is not None and len(abl):
        best = abl.sort_values("adj_r2", ascending=False).iloc[0]
        lines.append(
            f"- Best ablation specification: **{best['specification']}** "
            f"(adj R²={best['adj_r2']:.3f}).\n"
        )

    calib = _read_json(cfg.results_dir / "calibration" / "calibration_summary.json")
    if calib:
        lines.append("### Calibration (HuMT vs OA)\n")
        lines.append(
            f"- Pearson(HuMT, OA)={calib.get('pearson_humt_oa')}, "
            f"ECE={calib.get('ece')}, MCE={calib.get('mce')}, Brier={calib.get('brier')}.\n"
        )
        lines.append(
            "- If calibration error is high / correlation modest, human-likeness is "
            "**not** a reliable proxy for appropriateness.\n"
        )

    adv = _read_json(cfg.results_dir / "adversarial" / "adversarial_summary.json")
    if adv:
        lines.append("### Adversarial datasets\n")
        lines.append(f"- Dataset families present: {adv.get('families')}.\n")
        if adv.get("note"):
            lines.append(f"- Note: {adv['note']}\n")

    rel = _read_json(cfg.results_dir / "reliability" / "reliability_summary.json")
    if rel:
        lines.append("### Annotation reliability\n")
        lines.append(f"- Status: {rel.get('status')}. {rel.get('note', '')}\n")

    lines.append("## 2. Statistical significance and effect sizes\n")
    lines.append(
        "- See `results/hypotheses/hypothesis_tests.csv` and "
        "`results/model_comparison/effect_sizes.csv` for full effect-size reporting "
        "(Cohen's d, Hedges' g, Cliff's delta, η²/ω²).\n"
    )

    lines.append("## 3. Interpretation\n")
    lines.append(
        "- PERSONA disentangles empathy, deception risk, and contextual fit rather than "
        "treating anthropomorphism as a single 'human-like is better' axis.\n"
        "- Primary claim under test: PERSONA dimensions explain Overall Appropriateness "
        "beyond HuMT alone (incremental validity / nested models / ablation).\n"
        "- Model profile differences (radar / omnibus tests) support model-specific "
        "anthropomorphism signatures.\n"
    )

    lines.append("## 4. Potential threats to validity\n")
    lines.append(
        "- Current PERSONA scores are produced by an automated response-grounded pilot "
        "(`persona_rubric_v1_response_grounded`), not multi-rater clinician annotation.\n"
        "- Single-annotator limitation prevents IRR estimates (Krippendorff/Kappa/ICC).\n"
        "- PERSONA-ADV prompt set is not yet in the CSV inventory.\n"
        "- HuMT and Likert PERSONA scales have different metric properties; comparisons "
        "use standardized/robust methods where possible.\n"
        "- Cross-sectional single-turn responses underrepresent multi-turn attachment dynamics.\n"
    )

    lines.append("## 5. Reviewer discussion points\n")
    lines.append(
        "- Why OA is judged holistically rather than as a mean of E/D/F.\n"
        "- Why incremental R² over HuMT is the key claim versus raw correlations.\n"
        "- Distinguishing descriptive human-likeness (H/HuMT) from normative appropriateness.\n"
        "- Planned multi-annotator reliability once expert labels arrive.\n"
    )

    lines.append("## 6. Limitations\n")
    lines.append(
        "- Automated labels may under-detect rare severe deception patterns.\n"
        "- No original CounselBench clinician metrics joined yet for Exp.1-style convergence tests.\n"
        "- Clustering/EFA with few dimensions is exploratory.\n"
    )

    lines.append("## 7. Future work\n")
    lines.append(
        "- Multi-rater expert annotation + IRR.\n"
        "- Add PERSONA-ADV prompts and re-run adversarial contrasts.\n"
        "- Join CounselBench expert Quality/Empathy ratings for convergent validity.\n"
        "- Multi-turn extensions and user-study validation of Relational Expectation (R).\n"
    )

    lines.append("## 8. Artifact index\n")
    lines.append("- Figures: `figures/`\n- Tables: `tables/`\n- Numeric results: `results/`\n")

    out.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote report → %s", out)
    return out
