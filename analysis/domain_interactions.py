"""Phase 5 - domain interaction audit.

Tests whether associations between PERSONA dimensions and OA differ by domain.
This is not a new predictive model family; it is a targeted validation model
for the domain-variation claim.

Outputs:
  analysis/outputs/tables/domain_interactions.csv
  analysis/outputs/tables/domain_interaction_model_fit.csv
  analysis/outputs/reports/domain_interactions.md
  analysis/outputs/phase5_results.json
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .persona_common import (
    DIMENSIONS,
    DOMAINS,
    PROFILE,
    load_consensus,
    save_json,
    save_markdown,
    save_table,
)

REFERENCE_DOMAIN = "mental_health"


def prepare(data: pd.DataFrame) -> pd.DataFrame:
    frame = data.dropna(subset=["OA", "prompt_id"] + PROFILE).copy()
    for dim in PROFILE:
        sd = frame[dim].std(ddof=1)
        frame[f"z_{dim}"] = (frame[dim] - frame[dim].mean()) / sd if sd else 0.0
    for domain in DOMAINS:
        if domain == REFERENCE_DOMAIN:
            continue
        frame[f"domain_{domain}"] = (frame["domain"] == domain).astype(float)
    frame["cluster_id"] = frame["domain"].astype(str) + "::" + frame["prompt_id"].astype(str)
    return frame


def design_matrix(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    columns = [f"z_{dim}" for dim in PROFILE]
    domain_columns = [f"domain_{d}" for d in DOMAINS if d != REFERENCE_DOMAIN]
    columns.extend(domain_columns)
    interaction_columns = []
    for dim in PROFILE:
        for dom_col in domain_columns:
            name = f"z_{dim}:x:{dom_col}"
            frame[name] = frame[f"z_{dim}"] * frame[dom_col]
            interaction_columns.append(name)
    columns.extend(interaction_columns)
    x = sm.add_constant(frame[columns], has_constant="add")
    return x, interaction_columns


def fit_model(frame: pd.DataFrame):
    x, interaction_columns = design_matrix(frame)
    model = sm.OLS(frame["OA"].to_numpy(dtype=float), x.to_numpy(dtype=float))
    fit = model.fit(cov_type="cluster", cov_kwds={"groups": frame["cluster_id"]})
    names = list(x.columns)
    return fit, names, interaction_columns, x


def coefficient_table(fit, names: list[str], interaction_columns: list[str]) -> pd.DataFrame:
    rows = []
    ci = fit.conf_int()
    for i, name in enumerate(names):
        term_type = "interaction" if name in interaction_columns else "main_or_control"
        rows.append(
            {
                "term": name,
                "term_type": term_type,
                "estimate": float(fit.params[i]),
                "std_error_cluster_prompt": float(fit.bse[i]),
                "ci_low": float(ci[i, 0]),
                "ci_high": float(ci[i, 1]),
                "p_value": float(fit.pvalues[i]),
            }
        )
    return pd.DataFrame(rows)


def fit_table(fit, frame: pd.DataFrame, x: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "n": int(len(frame)),
                "domains": int(frame["domain"].nunique()),
                "prompt_clusters": int(frame["cluster_id"].nunique()),
                "r_squared": float(fit.rsquared),
                "adj_r_squared": float(fit.rsquared_adj),
                "condition_number": float(np.linalg.cond(x.to_numpy(dtype=float))),
                "covariance": "cluster-robust by domain::prompt_id",
                "reference_domain": REFERENCE_DOMAIN,
            }
        ]
    )


def render(coefs: pd.DataFrame, model_fit: pd.DataFrame) -> str:
    lines = [
        "# Domain interaction audit (Phase 5)",
        "",
        "This model tests whether the association between each PERSONA dimension and "
        "`OA` varies by domain. Predictors `H`, `E`, `D`, and `F` are z-scored over "
        "complete cases. Mental health is the reference domain. Uncertainty uses "
        "cluster-robust standard errors with clusters defined as `domain::prompt_id`.",
        "",
        "The model is interpretive, not causal. A domain interaction estimates how much "
        "the slope for a dimension differs from the mental-health slope in that domain.",
        "",
        "## Model fit",
        "",
        "| N | Prompt clusters | R² | Adj. R² | Condition number |",
        "|---:|---:|---:|---:|---:|",
    ]
    row = model_fit.iloc[0]
    lines.append(
        f"| {int(row['n'])} | {int(row['prompt_clusters'])} | {row['r_squared']:.3f} | "
        f"{row['adj_r_squared']:.3f} | {row['condition_number']:.2f} |"
    )

    lines += [
        "",
        "## Interaction terms",
        "",
        "| Term | Estimate | 95% CI | p | Interpretation |",
        "|---|---:|---|---:|---|",
    ]
    interactions = coefs[coefs["term_type"] == "interaction"]
    for _, r in interactions.iterrows():
        supported = "differs from mental-health slope" if r["p_value"] < 0.05 else "no clear slope difference"
        lines.append(
            f"| {r['term']} | {r['estimate']:.3f} | [{r['ci_low']:.3f}, {r['ci_high']:.3f}] | "
            f"{r['p_value']:.4f} | {supported} |"
        )

    lines += [
        "",
        "## All coefficients",
        "",
        "| Term | Type | Estimate | SE | 95% CI | p |",
        "|---|---|---:|---:|---|---:|",
    ]
    for _, r in coefs.iterrows():
        lines.append(
            f"| {r['term']} | {r['term_type']} | {r['estimate']:.3f} | "
            f"{r['std_error_cluster_prompt']:.3f} | [{r['ci_low']:.3f}, {r['ci_high']:.3f}] | "
            f"{r['p_value']:.4f} |"
        )

    lines += [
        "",
        "## Reading guidance",
        "",
        "- R² differences across domain-specific CV models are descriptive unless the interaction terms support slope differences.",
        "- Health remains constrained by its ceiling effect; interaction estimates should be interpreted with that limitation.",
        "- Significant interactions are associations, not evidence that a dimension causes appropriateness.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    frame = prepare(load_consensus())
    fit, names, interaction_columns, x = fit_model(frame)
    coefs = coefficient_table(fit, names, interaction_columns)
    model_fit = fit_table(fit, frame, x)

    save_table(coefs, "domain_interactions")
    save_table(model_fit, "domain_interaction_model_fit")
    save_markdown(render(coefs, model_fit), "domain_interactions")
    save_json(
        {
            "model_fit": model_fit.to_dict(orient="records"),
            "coefficients": coefs.to_dict(orient="records"),
            "method": {
                "model": "OLS: OA ~ z(H,E,D,F) * domain",
                "uncertainty": "cluster-robust standard errors by domain::prompt_id",
                "reference_domain": REFERENCE_DOMAIN,
            },
        },
        "phase5_results",
    )
    print(f"Phase 5 complete: domain interaction model on {len(frame)} complete cases")


if __name__ == "__main__":
    main()
