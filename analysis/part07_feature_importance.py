"""Part 7 — Feature importance with RF / XGBoost / LightGBM (+ SHAP if available)."""

from __future__ import annotations

import logging
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

from .config import AnalysisConfig
from .plotting import save_fig
from .utils import dataframe_to_latex, save_csv, save_json

logger = logging.getLogger("analysis.feature_importance")

FEATURES = ["HuMT", "E", "D", "F"]


def run_feature_importance(df: pd.DataFrame, cfg: AnalysisConfig) -> dict[str, Any]:
    out_res = cfg.results_dir / "feature_importance"
    out_fig = cfg.figures_dir / "feature_importance"
    out_tab = cfg.tables_dir / "feature_importance"

    data = df[FEATURES + ["OA"]].dropna()
    X = data[FEATURES]
    y = data["OA"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=cfg.random_seed
    )

    models: dict[str, Any] = {
        "RandomForest": RandomForestRegressor(
            n_estimators=300, random_state=cfg.random_seed, n_jobs=-1
        )
    }
    try:
        from xgboost import XGBRegressor

        models["XGBoost"] = XGBRegressor(
            n_estimators=300,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=cfg.random_seed,
            n_jobs=-1,
            objective="reg:squarederror",
        )
    except Exception as exc:
        logger.warning("XGBoost unavailable: %s", exc)
    try:
        from lightgbm import LGBMRegressor

        models["LightGBM"] = LGBMRegressor(
            n_estimators=300,
            learning_rate=0.05,
            random_state=cfg.random_seed,
            n_jobs=-1,
            verbosity=-1,
        )
    except Exception as exc:
        logger.warning("LightGBM unavailable: %s", exc)

    rows = []
    shap_rows = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        rmse = float(np.sqrt(np.mean((y_test - pred) ** 2)))
        r2 = float(1 - np.sum((y_test - pred) ** 2) / np.sum((y_test - y_test.mean()) ** 2))

        if hasattr(model, "feature_importances_"):
            for f, imp in zip(FEATURES, model.feature_importances_):
                rows.append({"model": name, "feature": f, "importance_type": "native", "importance": float(imp),
                             "test_rmse": rmse, "test_r2": r2})

        perm = permutation_importance(
            model, X_test, y_test, n_repeats=cfg.n_permutation, random_state=cfg.random_seed, n_jobs=-1
        )
        for f, mean_imp, std_imp in zip(FEATURES, perm.importances_mean, perm.importances_std):
            rows.append(
                {
                    "model": name,
                    "feature": f,
                    "importance_type": "permutation",
                    "importance": float(mean_imp),
                    "importance_std": float(std_imp),
                    "test_rmse": rmse,
                    "test_r2": r2,
                }
            )

        # SHAP if available
        try:
            import shap

            # Use a small background for speed
            background = shap.sample(X_train, min(100, len(X_train)), random_state=cfg.random_seed)
            explainer = shap.Explainer(model.predict, background)
            shap_values = explainer(X_test.iloc[: min(150, len(X_test))])
            mean_abs = np.abs(shap_values.values).mean(axis=0)
            for f, v in zip(FEATURES, mean_abs):
                shap_rows.append({"model": name, "feature": f, "mean_abs_shap": float(v)})
        except Exception as exc:
            logger.warning("SHAP skipped for %s: %s", name, exc)

    importance = pd.DataFrame(rows)
    save_csv(importance, out_res / "feature_importance.csv")
    dataframe_to_latex(
        importance[importance["importance_type"] == "permutation"],
        out_tab / "permutation_importance.tex",
        caption="Permutation feature importance for predicting OA.",
        label="tab:perm_importance",
    )

    # Plot permutation importance for RF
    rf = importance[(importance["model"] == "RandomForest") & (importance["importance_type"] == "permutation")]
    if len(rf):
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.barh(rf["feature"], rf["importance"], xerr=rf.get("importance_std"), color="#4C72B0")
        ax.set_xlabel("Permutation importance")
        ax.set_title("RandomForest permutation importance")
        save_fig(fig, out_fig / "fig_permutation_importance_rf.png", dpi=cfg.dpi)

    if shap_rows:
        shap_df = pd.DataFrame(shap_rows)
        save_csv(shap_df, out_res / "shap_mean_abs.csv")
        for model_name, sub in shap_df.groupby("model"):
            fig, ax = plt.subplots(figsize=(6.5, 4))
            ax.barh(sub["feature"], sub["mean_abs_shap"], color="#C44E52")
            ax.set_xlabel("Mean |SHAP|")
            ax.set_title(f"SHAP importance — {model_name}")
            save_fig(fig, out_fig / f"fig_shap_{model_name}.png", dpi=cfg.dpi)
    else:
        shap_df = pd.DataFrame()

    save_json({"models": list(models.keys())}, out_res / "feature_importance_summary.json")
    logger.info("Part 7 feature importance complete.")
    return {"importance": importance, "shap": shap_df}
