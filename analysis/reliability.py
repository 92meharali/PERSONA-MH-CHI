"""Phase 2 - annotation reliability, one method applied to all three domains.

The repository previously used two different estimators: Krippendorff ordinal
alpha plus ICC for mental health (``analysis/run.py``) and Cronbach's alpha for
education and health (``analysis/analysis_domains.py``). Cronbach's alpha is an
internal-consistency coefficient, not an agreement coefficient, so the two were
never comparable even though the summary documents tabulated them side by side.
This module standardises on the mental-health method.

ICC(A,k) is the primary statistic because the analysis uses averaged ratings
from multiple raters who scored the same responses. ICC(A,1) and Krippendorff's
ordinal alpha are retained as supplementary diagnostics.

Outputs:
  analysis/outputs/tables/reliability.csv
  analysis/outputs/tables/reliability_by_scenario.csv
  analysis/outputs/reports/reliability.md
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .persona_common import (
    DIMENSIONS,
    DOMAINS,
    N_BOOT,
    SEED,
    load_ratings,
    percentile_ci,
    save_json,
    save_markdown,
    save_table,
)

try:
    import krippendorff
except ImportError:  # pragma: no cover
    krippendorff = None


# --------------------------------------------------------------------------
# Estimators
# --------------------------------------------------------------------------
def ordinal_alpha(matrix: np.ndarray) -> float:
    """Krippendorff's alpha, ordinal level of measurement. matrix is raters x items."""
    if krippendorff is None:
        return float("nan")
    if matrix.shape[1] < 2:
        return float("nan")
    try:
        return float(krippendorff.alpha(reliability_data=matrix, level_of_measurement="ordinal"))
    except Exception:
        return float("nan")


def icc_absolute(matrix: np.ndarray) -> tuple[float, float]:
    """ICC(A,1) and ICC(A,k): two-way mixed-effects, absolute agreement.

    Computed from the ANOVA mean squares directly rather than through pingouin
    so that thousands of bootstrap replicates stay cheap. Validated against
    pingouin.intraclass_corr in the module self-check.
    """
    data = np.asarray(matrix, dtype=float).T  # items x raters
    data = data[~np.isnan(data).any(axis=1)]
    n, k = data.shape
    if n < 2 or k < 2:
        return float("nan"), float("nan")

    grand = data.mean()
    row_means = data.mean(axis=1)
    col_means = data.mean(axis=0)

    ss_rows = k * np.sum((row_means - grand) ** 2)
    ss_cols = n * np.sum((col_means - grand) ** 2)
    ss_total = np.sum((data - grand) ** 2)
    ss_error = ss_total - ss_rows - ss_cols

    ms_rows = ss_rows / (n - 1)
    ms_cols = ss_cols / (k - 1)
    ms_error = ss_error / ((n - 1) * (k - 1))

    denom_single = ms_rows + (k - 1) * ms_error + k * (ms_cols - ms_error) / n
    denom_avg = ms_rows + (ms_cols - ms_error) / n
    single = (ms_rows - ms_error) / denom_single if denom_single != 0 else float("nan")
    average = (ms_rows - ms_error) / denom_avg if denom_avg != 0 else float("nan")
    return float(single), float(average)


def interpret_icc(value: float) -> str:
    if np.isnan(value):
        return "not estimable"
    if value >= 0.80:
        return "strong agreement"
    if value >= 0.60:
        return "moderate; below the conventional publication threshold"
    return "weak agreement"


# --------------------------------------------------------------------------
# Estimation with cluster bootstrap over items
# --------------------------------------------------------------------------
def estimate(matrix: np.ndarray, rng: np.random.Generator, n_boot: int) -> dict:
    alpha = ordinal_alpha(matrix)
    icc1, icck = icc_absolute(matrix)

    n_items = matrix.shape[1]
    boots_alpha, boots_icc1, boots_icck = [], [], []
    for _ in range(n_boot):
        pick = rng.integers(0, n_items, size=n_items)
        sample = matrix[:, pick]
        boots_alpha.append(ordinal_alpha(sample))
        a1, ak = icc_absolute(sample)
        boots_icc1.append(a1)
        boots_icck.append(ak)

    alpha_ci = percentile_ci(boots_alpha)
    icc1_ci = percentile_ci(boots_icc1)
    icck_ci = percentile_ci(boots_icck)
    return {
        "n_responses": int(n_items),
        "n_raters": int(matrix.shape[0]),
        "krippendorff_alpha_ordinal": alpha,
        "alpha_ci_low": alpha_ci[0],
        "alpha_ci_high": alpha_ci[1],
        "icc_a1": icc1,
        "icc_a1_ci_low": icc1_ci[0],
        "icc_a1_ci_high": icc1_ci[1],
        "icc_ak": icck,
        "icc_ak_ci_low": icck_ci[0],
        "icc_ak_ci_high": icck_ci[1],
        "primary_interpretation": interpret_icc(icck),
    }


def rater_matrix(frame: pd.DataFrame, dimension: str) -> np.ndarray:
    frame = frame.dropna(subset=[f"{dimension}_score"])
    pivot = frame.pivot_table(
        index="annotator_id", columns="annotation_item_id", values=f"{dimension}_score", aggfunc="first"
    )
    return pivot.to_numpy(dtype=float)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main(n_boot: int = N_BOOT) -> None:
    ratings = load_ratings()
    rng = np.random.default_rng(SEED)

    rows = []
    for domain in DOMAINS:
        block = ratings[ratings["domain"] == domain]
        for dimension in DIMENSIONS:
            matrix = rater_matrix(block, dimension)
            rows.append({"domain": domain, "dimension": dimension, **estimate(matrix, rng, n_boot)})
    table = pd.DataFrame(rows)
    save_table(table, "reliability")

    scenario_rows = []
    for domain in DOMAINS:
        block = ratings[ratings["domain"] == domain]
        for scenario, sub in block.groupby("scenario_type"):
            if sub["annotation_item_id"].nunique() < 20:
                continue
            for dimension in DIMENSIONS:
                matrix = rater_matrix(sub, dimension)
                scenario_rows.append(
                    {"domain": domain, "scenario_type": scenario, "dimension": dimension,
                     **estimate(matrix, rng, max(200, n_boot // 5))}
                )
    scenario_table = pd.DataFrame(scenario_rows)
    save_table(scenario_table, "reliability_by_scenario")

    save_markdown(render(table, scenario_table), "reliability")
    save_json({"reliability": table.to_dict(orient="records"),
               "reliability_by_scenario": scenario_table.to_dict(orient="records")},
              "phase2_results")
    print(f"Phase 2 complete: reliability for {len(table)} domain x dimension cells")


def render(table: pd.DataFrame, scenario: pd.DataFrame) -> str:
    lines = ["# Annotation reliability (Phase 2)", "",
             "The primary reliability statistic is `ICC(A,k)`: a two-way mixed-effects, "
             "absolute-agreement, average-measures intraclass correlation. This matches the "
             "annotation structure because multiple raters in the relevant pool scored the same "
             "responses and the analysis uses their averaged score. Confidence intervals are 95 "
             "per cent percentile intervals from a response-level bootstrap.", "",
             "`ICC(A,1)` is reported as the single-rater counterpart. Krippendorff's ordinal "
             "alpha is retained as a supplementary ordinal diagnostic, not as the primary "
             "inter-rater reliability statistic.", "",
             "| Domain | Dimension | N | Raters | Primary ICC(A,k) | 95% CI | ICC(A,1) | 95% CI | Supplementary alpha | 95% CI | Interpretation |",
             "|---|---|---:|---:|---:|---|---:|---|---:|---|---|"]
    for _, r in table.iterrows():
        lines.append(
            f"| {r['domain']} | {r['dimension']} | {r['n_responses']} | {r['n_raters']} | "
            f"{r['icc_ak']:.3f} | [{r['icc_ak_ci_low']:.3f}, {r['icc_ak_ci_high']:.3f}] | "
            f"{r['icc_a1']:.3f} | [{r['icc_a1_ci_low']:.3f}, {r['icc_a1_ci_high']:.3f}] | "
            f"{r['krippendorff_alpha_ordinal']:.3f} | [{r['alpha_ci_low']:.3f}, {r['alpha_ci_high']:.3f}] | "
            f"{r['primary_interpretation']} |"
        )

    lines += ["", "## Scenario-level reliability", "",
              "Reported for scenario types with at least 20 responses. ICC(A,k) remains the primary "
              "statistic; alpha is supplementary.", "",
              "| Domain | Scenario | Dimension | N | ICC(A,k) | 95% CI | alpha | 95% CI |",
              "|---|---|---|---:|---:|---|---:|---|"]
    for _, r in scenario.iterrows():
        lines.append(
            f"| {r['domain']} | {r['scenario_type']} | {r['dimension']} | {r['n_responses']} | "
            f"{r['icc_ak']:.3f} | [{r['icc_ak_ci_low']:.3f}, {r['icc_ak_ci_high']:.3f}] | "
            f"{r['krippendorff_alpha_ordinal']:.3f} | [{r['alpha_ci_low']:.3f}, {r['alpha_ci_high']:.3f}] |"
        )

    lines += ["", "## Method check", "",
              "- `OA` reliability is estimated from the Group A OA pool.",
              "- `E`, `D`, and `F` reliability are estimated from the Group B dimension pool.",
              "- The ICC formula is absolute-agreement average-measures ICC, so systematic rater "
              "level differences count against reliability rather than being ignored.",
              "- The number of raters is read from each domain x dimension matrix after filtering "
              "to rows where that score is present.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
