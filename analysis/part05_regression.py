"""Parts 5–6 — Nested regression, incremental validity, diagnostics."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.model_selection import KFold
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.regression")

NESTED_SPECS = [
    ("M1_HuMT", ["HuMT"]),
    ("M2_HuMT_E", ["HuMT", "E"]),
    ("M3_HuMT_E_D", ["HuMT", "E", "D"]),
    ("M4_HuMT_E_D_F", ["HuMT", "E", "D", "F"]),
]


def _fit_ols(df: pd.DataFrame, predictors: list[str]) -> Any:
    y = df["OA"]
    X = sm.add_constant(df[predictors])
    return sm.OLS(y, X).fit()


def _cv_metrics(df: pd.DataFrame, predictors: list[str], n_splits: int, seed: int) -> dict[str, float]:
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    rmses, maes, r2s = [], [], []
    for train_idx, test_idx in kf.split(df):
        train, test = df.iloc[train_idx], df.iloc[test_idx]
        model = _fit_ols(train, predictors)
        pred = model.predict(sm.add_constant(test[predictors], has_constant="add"))
        y = test["OA"].to_numpy()
        err = y - pred.to_numpy()
        rmses.append(np.sqrt(np.mean(err ** 2)))
        maes.append(np.mean(np.abs(err)))
        ss_res = np.sum(err ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r2s.append(1 - ss_res / ss_tot if ss_tot else np.nan)
    return {
        "cv_rmse": float(np.mean(rmses)),
        "cv_mae": float(np.mean(maes)),
        "cv_r2": float(np.nanmean(r2s)),
    }


def run_regression(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "regression"
    out_fig = cfg.figures_dir / "regression"
    out_tab = cfg.tables_dir / "regression"
    data = df[["OA", "HuMT", "E", "D", "F"]].dropna().copy()

    comparison_rows = []
    models = {}
    coef_rows = []

    for name, preds in NESTED_SPECS:
        fit = _fit_ols(data, preds)
        models[name] = fit
        cv = _cv_metrics(data, preds, cfg.n_cv_folds, cfg.random_seed)
        comparison_rows.append(
            {
                "model": name,
                "predictors": "+".join(preds),
                "r2": float(fit.rsquared),
                "adj_r2": float(fit.rsquared_adj),
                "aic": float(fit.aic),
                "bic": float(fit.bic),
                "rmse": float(np.sqrt(np.mean(fit.resid ** 2))),
                "mae": float(np.mean(np.abs(fit.resid))),
                "n": int(fit.nobs),
                **cv,
            }
        )
        for term, coef in fit.params.items():
            coef_rows.append(
                {
                    "model": name,
                    "term": term,
                    "coef": float(coef),
                    "std_err": float(fit.bse[term]),
                    "t": float(fit.tvalues[term]),
                    "p": float(fit.pvalues[term]),
                    "ci_low": float(fit.conf_int().loc[term, 0]),
                    "ci_high": float(fit.conf_int().loc[term, 1]),
                }
            )

    comparison = pd.DataFrame(comparison_rows)
    coefs = pd.DataFrame(coef_rows)
    save_csv(comparison, out_res / "nested_model_comparison.csv")
    save_csv(coefs, out_res / "coefficients.csv")
    dataframe_to_latex(comparison, out_tab / "nested_model_comparison.tex",
                       caption="Nested OLS models predicting OA.",
                       label="tab:nested_ols")
    dataframe_to_latex(coefs, out_tab / "regression_coefficients.tex",
                       caption="OLS coefficients with 95\\% CIs.",
                       label="tab:ols_coefs")

    # Likelihood-ratio / F nested comparisons sequential
    lrt_rows = []
    for (n1, p1), (n2, p2) in zip(NESTED_SPECS, NESTED_SPECS[1:]):
        m1, m2 = models[n1], models[n2]
        # F-test for nested models
        f_stat = ((m1.ssr - m2.ssr) / (m1.df_resid - m2.df_resid)) / (m2.ssr / m2.df_resid)
        df_diff = m1.df_resid - m2.df_resid
        p = 1 - stats.f.cdf(f_stat, df_diff, m2.df_resid)
        lrt_stat = 2 * (m2.llf - m1.llf)
        lrt_p = 1 - stats.chi2.cdf(lrt_stat, df_diff)
        lrt_rows.append(
            {
                "restricted": n1,
                "full": n2,
                "delta_r2": float(m2.rsquared - m1.rsquared),
                "delta_adj_r2": float(m2.rsquared_adj - m1.rsquared_adj),
                "f_change": float(f_stat),
                "f_p": float(p),
                "lrt": float(lrt_stat),
                "lrt_p": float(lrt_p),
            }
        )
    lrt = pd.DataFrame(lrt_rows)
    save_csv(lrt, out_res / "nested_lrt_fchange.csv")
    dataframe_to_latex(lrt, out_tab / "nested_lrt_fchange.tex",
                       caption="Nested model improvement tests.",
                       label="tab:nested_tests")

    # Diagnostics on full model
    full = models["M4_HuMT_E_D_F"]
    influence = OLSInfluence(full)
    resid = full.resid
    fitted = full.fittedvalues
    # BP heteroscedasticity
    bp_stat, bp_p, _, _ = het_breuschpagan(resid, full.model.exog)
    # Residual normality
    sw_stat, sw_p = stats.shapiro(resid.sample(n=min(len(resid), 500), random_state=cfg.random_seed))
    # VIF
    X = sm.add_constant(data[["HuMT", "E", "D", "F"]])
    vif_rows = []
    for i, col in enumerate(X.columns):
        if col == "const":
            continue
        vif_rows.append({"term": col, "vif": float(variance_inflation_factor(X.values, i))})
    vif = pd.DataFrame(vif_rows)
    save_csv(vif, out_res / "vif.csv")

    cook = influence.cooks_distance[0]
    leverage = influence.hat_matrix_diag
    diag = pd.DataFrame(
        {
            "resid": resid,
            "fitted": fitted,
            "cook_d": cook,
            "leverage": leverage,
        }
    )
    save_csv(diag, out_res / "residual_diagnostics_rows.csv")
    save_json(
        {
            "breusch_pagan_stat": float(bp_stat),
            "breusch_pagan_p": float(bp_p),
            "shapiro_resid_stat": float(sw_stat),
            "shapiro_resid_p": float(sw_p),
        },
        out_res / "diagnostic_tests.json",
    )

    # Diagnostic figures
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    axes[0].scatter(fitted, resid, s=10, alpha=0.4)
    axes[0].axhline(0, color="black", lw=1)
    axes[0].set_xlabel("Fitted")
    axes[0].set_ylabel("Residual")
    axes[0].set_title("Residuals vs fitted")
    stats.probplot(resid, plot=axes[1])
    axes[1].set_title("QQ residuals")
    axes[2].stem(np.arange(len(cook)), cook, linefmt="C0-", markerfmt="C0o", basefmt=" ")
    axes[2].set_title("Cook's distance")
    axes[2].set_xlabel("Index")
    save_fig(fig, out_fig / "fig_regression_diagnostics.png", dpi=cfg.dpi)

    # Coefficient plot for full model
    full_coefs = coefs[coefs["model"] == "M4_HuMT_E_D_F"]
    fig, ax = plt.subplots(figsize=(7, 4))
    y = np.arange(len(full_coefs))
    ax.errorbar(full_coefs["coef"], y,
                xerr=[full_coefs["coef"] - full_coefs["ci_low"],
                      full_coefs["ci_high"] - full_coefs["coef"]],
                fmt="o", color="#4C72B0")
    ax.axvline(0, color="black", lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels(full_coefs["term"])
    ax.set_xlabel("Coefficient")
    ax.set_title("Full model coefficients (95% CI)")
    save_fig(fig, out_fig / "fig_regression_coefficients.png", dpi=cfg.dpi)

    # Bootstrap coefficients for full model
    rng = np.random.default_rng(cfg.random_seed)
    boot = []
    n = len(data)
    for _ in range(cfg.n_bootstrap):
        idx = rng.integers(0, n, n)
        sample = data.iloc[idx]
        try:
            fit = _fit_ols(sample, ["HuMT", "E", "D", "F"])
            boot.append(fit.params.to_dict())
        except Exception:
            continue
    boot_df = pd.DataFrame(boot)
    boot_summary = boot_df.agg(["mean", "std", lambda s: s.quantile(0.025), lambda s: s.quantile(0.975)]).T
    boot_summary.columns = ["mean", "std", "ci_low", "ci_high"]
    boot_summary = boot_summary.reset_index().rename(columns={"index": "term"})
    save_csv(boot_summary, out_res / "bootstrap_coefficients.csv")

    logger.info("Part 5 regression complete.")
    return {"comparison": comparison, "lrt": lrt, "models": models}


def run_incremental_validity(df: pd.DataFrame, cfg: AnalysisConfig, regression_out: dict[str, Any]) -> dict[str, Any]:
    out_res = cfg.results_dir / "incremental"
    out_tab = cfg.tables_dir / "incremental"
    comparison = regression_out["comparison"]
    lrt = regression_out["lrt"]

    # Focused interpretation table: PERSONA beyond HuMT
    base = comparison.loc[comparison["model"] == "M1_HuMT"].iloc[0]
    full = comparison.loc[comparison["model"] == "M4_HuMT_E_D_F"].iloc[0]
    summary = pd.DataFrame(
        [
            {
                "comparison": "M4 vs M1",
                "base_adj_r2": base["adj_r2"],
                "full_adj_r2": full["adj_r2"],
                "delta_adj_r2": full["adj_r2"] - base["adj_r2"],
                "base_aic": base["aic"],
                "full_aic": full["aic"],
                "delta_aic": full["aic"] - base["aic"],
                "interpretation": (
                    "PERSONA dimensions add incremental validity beyond HuMT "
                    "if delta_adj_r2 > 0 and nested F/LRT are significant."
                ),
            }
        ]
    )
    # Attach cumulative F chain
    save_csv(summary, out_res / "incremental_validity_summary.csv")
    save_csv(lrt, out_res / "hierarchical_steps.csv")
    dataframe_to_latex(summary, out_tab / "incremental_validity.tex",
                       caption="Incremental validity of PERSONA over HuMT for predicting OA.",
                       label="tab:incremental")
    save_json(summary.to_dict(orient="records")[0], out_res / "incremental_validity.json")
    logger.info("Part 6 incremental validity complete.")
    return {"summary": summary}
