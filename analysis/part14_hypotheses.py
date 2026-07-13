"""Part 14 — Automated hypothesis testing battery."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

from .config import AnalysisConfig
from .utils import cliffs_delta, cohens_d, dataframe_to_latex, hedges_g, save_csv, save_json

logger = logging.getLogger("analysis.hypotheses")


def run_hypothesis_testing(df: pd.DataFrame, cfg: AnalysisConfig,
                           extras: dict[str, Any] | None = None) -> pd.DataFrame:
    out_res = cfg.results_dir / "hypotheses"
    out_tab = cfg.tables_dir / "hypotheses"
    extras = extras or {}
    rows = []

    def add(hid, name, test, stat, p, effect, effect_name, ci, interpretation):
        rows.append(
            {
                "hypothesis_id": hid,
                "hypothesis": name,
                "test": test,
                "statistic": stat,
                "p_value": p,
                "effect_size": effect,
                "effect_size_name": effect_name,
                "ci": ci,
                "interpretation": interpretation,
            }
        )

    # H1: Models differ on D
    groups = [g["D"].dropna().to_numpy() for _, g in df.groupby("model")]
    h, p = stats.kruskal(*groups)
    add("H1", "Models differ on Deception Risk (D)", "Kruskal-Wallis",
        float(h), float(p), np.nan, "eta_approx", "n/a",
        "Reject H0 if p<.05: model anthropomorphism deception profiles differ.")

    # H2: Models differ on OA
    groups = [g["OA"].dropna().to_numpy() for _, g in df.groupby("model")]
    h, p = stats.kruskal(*groups)
    add("H2", "Models differ on Overall Appropriateness (OA)", "Kruskal-Wallis",
        float(h), float(p), np.nan, "eta_approx", "n/a",
        "Reject H0 if p<.05: models differ in appropriateness.")

    # H3: HuMT alone is weakly related to OA relative to PERSONA
    r, p = stats.spearmanr(df["HuMT"], df["OA"])
    add("H3", "HuMT correlates with OA", "Spearman",
        float(r), float(p), float(r), "spearman_r", "n/a",
        "Magnitude indicates how far human-likeness tracks appropriateness.")

    # H4: PERSONA adds beyond HuMT (nested F)
    data = df[["OA", "HuMT", "E", "D", "F"]].dropna()
    m1 = sm.OLS(data["OA"], sm.add_constant(data[["HuMT"]])).fit()
    m4 = sm.OLS(data["OA"], sm.add_constant(data[["HuMT", "E", "D", "F"]])).fit()
    f_stat = ((m1.ssr - m4.ssr) / (m1.df_resid - m4.df_resid)) / (m4.ssr / m4.df_resid)
    p_f = 1 - stats.f.cdf(f_stat, m1.df_resid - m4.df_resid, m4.df_resid)
    add("H4", "PERSONA explains OA beyond HuMT", "Nested F-test (M4 vs M1)",
        float(f_stat), float(p_f), float(m4.rsquared_adj - m1.rsquared_adj),
        "delta_adj_r2", "n/a",
        "Supports incremental validity of PERSONA if p<.05 and delta_adj_r2>0.")

    # H5: D higher on ADV than EVAL (if both exist)
    fams = set(df["dataset_family"].unique())
    if "CounselBench-ADV" in fams and "CounselBench-EVAL" in fams:
        a = df.loc[df["dataset_family"] == "CounselBench-ADV", "D"].dropna().to_numpy()
        b = df.loc[df["dataset_family"] == "CounselBench-EVAL", "D"].dropna().to_numpy()
        u, p = stats.mannwhitneyu(a, b, alternative="greater")
        d = cohens_d(a, b)
        add("H5", "Deception Risk higher on ADV than EVAL", "Mann-Whitney (greater)",
            float(u), float(p), float(d), "cohens_d", "n/a",
            "Supports adversarial sensitivity of D if p<.05.")
    else:
        add("H5", "Deception Risk higher on ADV than EVAL", "not_applicable",
            np.nan, np.nan, np.nan, "n/a", "n/a",
            "Required dataset families not both present.")

    # H6: E positively associated with OA when D is low
    low_d = df[df["D"] <= df["D"].median()]
    r, p = stats.spearmanr(low_d["E"], low_d["OA"])
    add("H6", "Empathy relates more positively to OA when D is low", "Spearman in low-D subset",
        float(r), float(p), float(r), "spearman_r", "n/a",
        "Consistent with 'empathy helps only if deception is controlled'.")

    # H7: F correlates with OA
    r, p = stats.spearmanr(df["F"], df["OA"])
    add("H7", "Contextual Fit correlates with OA", "Spearman",
        float(r), float(p), float(r), "spearman_r", "n/a",
        "Expected positive association between fit and appropriateness.")

    hyp = pd.DataFrame(rows)
    save_csv(hyp, out_res / "hypothesis_tests.csv")
    dataframe_to_latex(hyp.drop(columns=["interpretation"]), out_tab / "hypothesis_tests.tex",
                       caption="Primary hypothesis tests for PERSONA analyses.",
                       label="tab:hypotheses")
    # Markdown interpretations
    lines = ["# Hypothesis interpretations\n"]
    for _, row in hyp.iterrows():
        lines.append(f"## {row['hypothesis_id']}: {row['hypothesis']}\n")
        lines.append(f"- Test: {row['test']}\n")
        lines.append(f"- Statistic: {row['statistic']}\n")
        lines.append(f"- p: {row['p_value']}\n")
        lines.append(f"- Effect ({row['effect_size_name']}): {row['effect_size']}\n")
        lines.append(f"- Interpretation: {row['interpretation']}\n")
    (out_res / "hypothesis_interpretations.md").write_text("\n".join(lines), encoding="utf-8")
    save_json({"n_hypotheses": len(hyp)}, out_res / "hypothesis_summary.json")
    logger.info("Part 14 hypothesis testing complete (%d hypotheses).", len(hyp))
    return hyp
