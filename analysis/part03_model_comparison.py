"""Part 3 — Model comparison with assumption checks, post-hoc tests, effect sizes."""

from __future__ import annotations

import logging
from itertools import combinations
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from .config import AnalysisConfig
from .data_loader import CANONICAL_METRICS
from .plotting import bar_values, boxplot_by_group, radar_chart
from .utils import (
    cliffs_delta,
    cohens_d,
    dataframe_to_latex,
    hedges_g,
    mean_ci,
    save_csv,
    save_json,
    safe_pvalue,
)

logger = logging.getLogger("analysis.model_comparison")


def _normality_by_group(df: pd.DataFrame, metric: str, group: str) -> pd.DataFrame:
    rows = []
    for name, sub in df.groupby(group):
        vals = sub[metric].dropna()
        if len(vals) < 3:
            rows.append({"metric": metric, "group": name, "test": "shapiro", "stat": np.nan, "p": np.nan})
            continue
        # Shapiro on sample size capped for performance.
        sample = vals.sample(n=min(len(vals), 200), random_state=0)
        w, p = stats.shapiro(sample)
        rows.append({"metric": metric, "group": name, "test": "shapiro", "stat": float(w), "p": float(p)})
    return pd.DataFrame(rows)


def _levene(df: pd.DataFrame, metric: str, group: str) -> dict[str, float]:
    samples = [g[metric].dropna().to_numpy() for _, g in df.groupby(group)]
    samples = [s for s in samples if len(s)]
    if len(samples) < 2:
        return {"stat": np.nan, "p": np.nan}
    stat, p = stats.levene(*samples)
    return {"stat": float(stat), "p": float(p)}


def _omega_squared(anova_table: pd.DataFrame) -> float:
    # Expect statsmodels-like columns if available; else nan.
    try:
        ss_between = float(anova_table.loc["C(model)", "sum_sq"])
        ss_resid = float(anova_table.loc["Residual", "sum_sq"])
        df_between = float(anova_table.loc["C(model)", "df"])
        ms_resid = float(anova_table.loc["Residual", "mean_sq"])
        return float((ss_between - df_between * ms_resid) / (ss_between + ss_resid + ms_resid))
    except Exception:
        return float("nan")


def run_model_comparison(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "model_comparison"
    out_fig = cfg.figures_dir / "model_comparison"
    out_tab = cfg.tables_dir / "model_comparison"

    models = sorted(df["model"].unique().tolist())
    omnibus_rows = []
    posthoc_rows = []
    ranking_rows = []
    effect_rows = []

    for metric in CANONICAL_METRICS:
        # Assumption checks
        normality = _normality_by_group(df, metric, "model")
        save_csv(normality, out_res / f"assumptions_normality_{metric}.csv")
        levene = _levene(df, metric, "model")
        save_json(levene, out_res / f"assumptions_levene_{metric}.json")

        groups = [df.loc[df["model"] == m, metric].dropna().to_numpy() for m in models]
        normal_ok = bool((normality["p"] > 0.05).all()) if len(normality) else False
        var_ok = bool(levene.get("p", 0) > 0.05) if not np.isnan(levene.get("p", np.nan)) else False

        # Omnibus tests
        f_stat, f_p = stats.f_oneway(*groups)
        # Welch ANOVA approximation via scipy.stats doesn't include Welch directly;
        # use Kruskal always + ANOVA; note Welch via pingouin if available.
        try:
            import pingouin as pg

            welch = pg.welch_anova(dv=metric, between="model", data=df[[metric, "model"]].dropna())
            welch_p = float(welch["p_unc"].iloc[0])
            welch_stat = float(welch["F"].iloc[0])
        except Exception:
            welch_stat, welch_p = np.nan, np.nan

        h_stat, h_p = stats.kruskal(*groups)

        if normal_ok and var_ok:
            primary = "ANOVA"
            primary_stat, primary_p = float(f_stat), float(f_p)
        elif normal_ok and not var_ok:
            primary = "WelchANOVA"
            primary_stat, primary_p = welch_stat, welch_p
        else:
            primary = "KruskalWallis"
            primary_stat, primary_p = float(h_stat), float(h_p)

        # Eta squared from ANOVA SS
        try:
            import statsmodels.api as sm
            from statsmodels.formula.api import ols

            model = ols(f"{metric} ~ C(model)", data=df).fit()
            anova_tbl = sm.stats.anova_lm(model, typ=2)
            ss_b = float(anova_tbl.loc["C(model)", "sum_sq"])
            ss_t = float(anova_tbl["sum_sq"].sum())
            eta_sq = ss_b / ss_t if ss_t else np.nan
            anova_tbl = anova_tbl.copy()
            anova_tbl["mean_sq"] = anova_tbl["sum_sq"] / anova_tbl["df"]
            omega_sq = _omega_squared(anova_tbl)
        except Exception:
            eta_sq, omega_sq = np.nan, np.nan

        omnibus_rows.append(
            {
                "metric": metric,
                "primary_test": primary,
                "primary_stat": primary_stat,
                "primary_p": primary_p,
                "anova_F": float(f_stat),
                "anova_p": float(f_p),
                "welch_F": welch_stat,
                "welch_p": welch_p,
                "kruskal_H": float(h_stat),
                "kruskal_p": float(h_p),
                "eta_squared": eta_sq,
                "omega_squared": omega_sq,
                "normality_ok": normal_ok,
                "equal_variance_ok": var_ok,
            }
        )

        # Rankings
        for m in models:
            stats_m = mean_ci(df.loc[df["model"] == m, metric])
            ranking_rows.append({"metric": metric, "model": m, **stats_m})

        # Pairwise effect sizes + Dunn/Tukey-like Mann-Whitney with Holm
        pairs = list(combinations(models, 2))
        pvals = []
        pair_pack = []
        for a, b in pairs:
            xa = df.loc[df["model"] == a, metric].dropna().to_numpy()
            xb = df.loc[df["model"] == b, metric].dropna().to_numpy()
            u, p = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            pvals.append(p)
            pair_pack.append((a, b, xa, xb, u, p))

        # Holm correction
        order = np.argsort(pvals)
        adjusted = np.empty(len(pvals))
        mcount = len(pvals)
        prev = 0.0
        for rank, idx in enumerate(order):
            adj = (mcount - rank) * pvals[idx]
            adj = min(adj, 1.0)
            adj = max(adj, prev)
            adjusted[idx] = adj
            prev = adj

        for i, (a, b, xa, xb, u, p) in enumerate(pair_pack):
            posthoc_rows.append(
                {
                    "metric": metric,
                    "model_a": a,
                    "model_b": b,
                    "test": "mannwhitney_dunn_style",
                    "stat": float(u),
                    "p_raw": float(p),
                    "p_holm": float(adjusted[i]),
                    "cohens_d": cohens_d(xa, xb),
                    "hedges_g": hedges_g(xa, xb),
                    "cliffs_delta": cliffs_delta(xa, xb),
                }
            )
            effect_rows.append(
                {
                    "metric": metric,
                    "model_a": a,
                    "model_b": b,
                    "cohens_d": cohens_d(xa, xb),
                    "hedges_g": hedges_g(xa, xb),
                    "cliffs_delta": cliffs_delta(xa, xb),
                }
            )

        boxplot_by_group(df, metric, "model", out_fig / f"fig_model_box_{metric}.png", dpi=cfg.dpi)

    omnibus = pd.DataFrame(omnibus_rows)
    posthoc = pd.DataFrame(posthoc_rows)
    ranking = pd.DataFrame(ranking_rows)
    effects = pd.DataFrame(effect_rows)

    save_csv(omnibus, out_res / "omnibus_tests.csv")
    save_csv(posthoc, out_res / "posthoc_pairwise.csv")
    save_csv(ranking, out_res / "model_rankings.csv")
    save_csv(effects, out_res / "effect_sizes.csv")

    dataframe_to_latex(omnibus, out_tab / "omnibus_tests.tex",
                       caption="Omnibus model comparisons across PERSONA metrics and HuMT.",
                       label="tab:model_omnibus")
    dataframe_to_latex(
        ranking.pivot_table(index="model", columns="metric", values="mean"),
        out_tab / "model_ranking_means.tex",
        caption="Mean metric values by model.",
        label="tab:model_means",
    )

    # Radar of mean metrics (exclude raw scale mismatch carefully: HuMT is continuous small)
    # Standardize means per metric for radar.
    means = ranking.pivot_table(index="model", columns="metric", values="mean")
    z = means.copy()
    for col in z.columns:
        mu, sd = z[col].mean(), z[col].std(ddof=0)
        z[col] = 0.0 if sd == 0 else (z[col] - mu) / sd
    series = {idx: z.loc[idx, list(CANONICAL_METRICS)].tolist() for idx in z.index}
    radar_chart(list(CANONICAL_METRICS), series, out_fig / "fig_model_radar.png",
                dpi=cfg.dpi, title="Standardized model profiles")

    # Simple ranking bars for OA
    oa_means = ranking[ranking["metric"] == "OA"].sort_values("mean", ascending=False)
    bar_values(oa_means["model"].tolist(), oa_means["mean"].tolist(),
               out_fig / "fig_oa_model_ranking.png", ylabel="Mean OA",
               title="Model ranking by Overall Appropriateness", dpi=cfg.dpi)

    summary = {"n_models": len(models), "models": models}
    save_json(summary, out_res / "model_comparison_summary.json")
    logger.info("Part 3 model comparison complete.")
    return {"omnibus": omnibus, "posthoc": posthoc, "ranking": ranking}
