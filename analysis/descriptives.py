"""Phase 3 - descriptive statistics and dimension separability.

This phase runs before the predictive work on purpose. Restricted variance
decides what Phase 4 is entitled to conclude: a predictor with almost no spread
cannot show a relationship, and an outcome sitting on its ceiling cannot be
explained by anything. Both conditions are present in this corpus, so they are
quantified here rather than mentioned as an afterthought.

Outputs:
  analysis/outputs/tables/descriptives_by_domain.csv
  analysis/outputs/tables/descriptives_by_model.csv
  analysis/outputs/tables/ceiling_floor.csv
  analysis/outputs/tables/correlations.csv
  analysis/outputs/tables/collinearity_vif.csv
  analysis/outputs/tables/collinearity_condition.csv
  analysis/outputs/figures/fig_distributions_by_domain.png
  analysis/outputs/figures/fig_correlation_matrix.png
  analysis/outputs/figures/fig_h_vs_oa.png
  analysis/outputs/figures/fig_f_vs_oa.png
  analysis/outputs/reports/descriptives.md
"""

from __future__ import annotations

import itertools

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .persona_common import (
    DIMENSIONS,
    DOMAIN_LABEL,
    DOMAINS,
    FIGURE_DIR,
    N_BOOT,
    PROFILE,
    RATING_MAX,
    RATING_MIN,
    SEED,
    bh_adjust,
    cluster_bootstrap_indices,
    load_consensus,
    percentile_ci,
    save_json,
    save_markdown,
    save_table,
)

COLORS = {"mental_health": "#4C78A8", "education": "#F58518", "health": "#54A24B"}


# --------------------------------------------------------------------------
# Descriptives
# --------------------------------------------------------------------------
def describe(series: pd.Series) -> dict:
    clean = series.dropna()
    if clean.empty:
        return {}
    q1, q3 = np.percentile(clean, [25, 75])
    return {
        "n": int(clean.size),
        "mean": float(clean.mean()),
        "median": float(clean.median()),
        "sd": float(clean.std(ddof=1)),
        "iqr": float(q3 - q1),
        "q1": float(q1),
        "q3": float(q3),
        "min": float(clean.min()),
        "max": float(clean.max()),
        "skew": float(stats.skew(clean)),
    }


def run_descriptives(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for domain in DOMAINS:
        block = data[data["domain"] == domain]
        for measure in ["OA", "E", "D", "F", "H"]:
            rows.append({"domain": domain, "measure": measure, **describe(block[measure])})
    by_domain = pd.DataFrame(rows)

    model_rows = []
    for (domain, model), block in data.dropna(subset=["model"]).groupby(["domain", "model"]):
        entry = {"domain": domain, "model": model, "n": len(block)}
        for measure in ["OA", "E", "D", "F", "H"]:
            entry[f"{measure}_mean"] = float(block[measure].mean())
            entry[f"{measure}_sd"] = float(block[measure].std(ddof=1))
        model_rows.append(entry)
    by_model = pd.DataFrame(model_rows)
    return by_domain, by_model


def run_ceiling_floor(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain in DOMAINS:
        block = data[data["domain"] == domain]
        for dim in DIMENSIONS:
            values = block[dim].dropna()
            rows.append({
                "domain": domain,
                "measure": dim,
                "n": int(values.size),
                "at_scale_max": int((values >= RATING_MAX - 1e-9).sum()),
                "pct_at_scale_max": round(float((values >= RATING_MAX - 1e-9).mean() * 100), 2),
                "at_scale_min": int((values <= RATING_MIN + 1e-9).sum()),
                "pct_at_scale_min": round(float((values <= RATING_MIN + 1e-9).mean() * 100), 2),
                "pct_in_top_quintile": round(float((values >= 4.2).mean() * 100), 2),
                "sd": round(float(values.std(ddof=1)), 3),
                "sd_as_pct_of_scale_range": round(float(values.std(ddof=1)) / (RATING_MAX - RATING_MIN) * 100, 2),
            })
        humt = block["H"].dropna()
        if humt.size:
            spread = float(humt.max() - humt.min())
            rows.append({
                "domain": domain, "measure": "H", "n": int(humt.size),
                "at_scale_max": np.nan, "pct_at_scale_max": np.nan,
                "at_scale_min": np.nan, "pct_at_scale_min": np.nan,
                "pct_in_top_quintile": np.nan,
                "sd": round(float(humt.std(ddof=1)), 4),
                "sd_as_pct_of_scale_range": round(float(humt.std(ddof=1)) / spread * 100, 2) if spread else np.nan,
            })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Separability
# --------------------------------------------------------------------------
def run_correlations(data: pd.DataFrame, rng: np.random.Generator, n_boot: int) -> pd.DataFrame:
    rows = []
    for domain in DOMAINS:
        block = data[data["domain"] == domain]
        for left, right in itertools.combinations(["H"] + DIMENSIONS, 2):
            sub = block[[left, right, "prompt_id"]].dropna()
            if len(sub) < 10:
                continue
            rho, p_rho = stats.spearmanr(sub[left], sub[right])
            r, p_r = stats.pearsonr(sub[left], sub[right])
            boots = []
            groups = sub["prompt_id"].to_numpy()
            for idx in cluster_bootstrap_indices(groups, rng, n_boot):
                sample = sub.iloc[idx]
                if sample[left].nunique() < 2 or sample[right].nunique() < 2:
                    continue
                boots.append(stats.spearmanr(sample[left], sample[right]).statistic)
            low, high = percentile_ci(boots)
            rows.append({
                "domain": domain, "variable_a": left, "variable_b": right, "n": len(sub),
                "spearman_rho": float(rho), "spearman_p": float(p_rho),
                "cluster_boot_ci_low": low, "cluster_boot_ci_high": high,
                "pearson_r": float(r), "pearson_p": float(p_r),
            })
    frame = pd.DataFrame(rows)
    frame["spearman_p_fdr"] = bh_adjust(frame["spearman_p"].tolist())
    frame["ci_excludes_zero"] = (frame["cluster_boot_ci_low"] > 0) | (frame["cluster_boot_ci_high"] < 0)
    return frame


def run_vif(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain in DOMAINS:
        block = data[data["domain"] == domain][PROFILE].dropna()
        for target in PROFILE:
            others = [c for c in PROFILE if c != target]
            x = np.column_stack([np.ones(len(block))] + [block[c].to_numpy() for c in others])
            y = block[target].to_numpy()
            beta, *_ = np.linalg.lstsq(x, y, rcond=None)
            resid = y - x @ beta
            ss_tot = float(np.sum((y - y.mean()) ** 2))
            r_squared = 1 - float(np.sum(resid ** 2)) / ss_tot if ss_tot else np.nan
            rows.append({
                "domain": domain, "dimension": target, "n": len(block),
                "r_squared_on_others": round(float(r_squared), 4),
                "vif": round(float(1 / (1 - r_squared)), 3) if r_squared < 1 else np.inf,
            })
    return pd.DataFrame(rows)


def run_condition_number(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for domain in DOMAINS:
        block = data[data["domain"] == domain][PROFILE].dropna()
        x = block.to_numpy(dtype=float)
        if len(block) < 2:
            condition = np.nan
        else:
            scaled = (x - x.mean(axis=0)) / x.std(axis=0, ddof=1)
            condition = float(np.linalg.cond(scaled))
        rows.append({"domain": domain, "n": len(block), "condition_number": condition})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------
def figure_distributions(data: pd.DataFrame) -> None:
    measures = ["OA", "E", "D", "F", "H"]
    fig, axes = plt.subplots(1, 5, figsize=(17, 4.2))
    for ax, measure in zip(axes, measures):
        series = [data[data["domain"] == d][measure].dropna().to_numpy() for d in DOMAINS]
        parts = ax.violinplot(series, showmeans=True, showextrema=False, widths=0.85)
        for body, domain in zip(parts["bodies"], DOMAINS):
            body.set_facecolor(COLORS[domain])
            body.set_alpha(0.65)
        ax.set_xticks(range(1, len(DOMAINS) + 1))
        ax.set_xticklabels([DOMAIN_LABEL[d].replace(" ", "\n") for d in DOMAINS], fontsize=9)
        ax.set_title(measure if measure != "H" else "H (HuMT)", fontsize=12)
        if measure != "H":
            ax.set_ylim(0.8, 5.2)
            ax.axhline(RATING_MAX, color="#999", linestyle=":", linewidth=1)
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle("Consensus score distributions by domain (dotted line = scale ceiling)", fontsize=13)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_distributions_by_domain.png", dpi=160)
    plt.close(fig)


def figure_correlation_matrix(data: pd.DataFrame) -> None:
    measures = ["H", "E", "D", "F", "OA"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    for ax, domain in zip(axes, DOMAINS):
        block = data[data["domain"] == domain][measures].dropna()
        matrix = block.corr(method="spearman").to_numpy()
        im = ax.imshow(matrix, vmin=-1, vmax=1, cmap="RdBu_r")
        ax.set_xticks(range(len(measures)), measures)
        ax.set_yticks(range(len(measures)), measures)
        for i in range(len(measures)):
            for j in range(len(measures)):
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=9,
                        color="white" if abs(matrix[i, j]) > 0.55 else "black")
        ax.set_title(f"{DOMAIN_LABEL[domain]} (n={len(block)})", fontsize=11)
    fig.colorbar(im, ax=axes, shrink=0.8, label="Spearman rho")
    fig.suptitle("Dimension separability: consensus-level Spearman correlations", fontsize=13)
    fig.savefig(FIGURE_DIR / "fig_correlation_matrix.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def figure_scatter(data: pd.DataFrame, predictor: str, filename: str, title: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
    for ax, domain in zip(axes, DOMAINS):
        block = data[data["domain"] == domain][[predictor, "OA"]].dropna()
        ax.scatter(block[predictor], block["OA"], s=16, alpha=0.45, color=COLORS[domain],
                   edgecolor="none")
        if len(block) > 2 and block[predictor].nunique() > 1:
            slope, intercept = np.polyfit(block[predictor], block["OA"], 1)
            xs = np.linspace(block[predictor].min(), block[predictor].max(), 50)
            ax.plot(xs, slope * xs + intercept, color="#333", linewidth=1.6)
            rho = stats.spearmanr(block[predictor], block["OA"]).statistic
            ax.set_title(f"{DOMAIN_LABEL[domain]}  rho={rho:.3f}  n={len(block)}", fontsize=11)
        ax.set_xlabel(predictor if predictor != "H" else "H (HuMT)")
        ax.grid(alpha=0.25)
    axes[0].set_ylabel("Consensus OA")
    fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / filename, dpi=160)
    plt.close(fig)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main(n_boot: int = N_BOOT) -> None:
    data = load_consensus()
    rng = np.random.default_rng(SEED)

    by_domain, by_model = run_descriptives(data)
    ceiling = run_ceiling_floor(data)
    correlations = run_correlations(data, rng, n_boot)
    vif = run_vif(data)
    condition = run_condition_number(data)

    save_table(by_domain, "descriptives_by_domain")
    save_table(by_model, "descriptives_by_model")
    save_table(ceiling, "ceiling_floor")
    save_table(correlations, "correlations")
    save_table(vif, "collinearity_vif")
    save_table(condition, "collinearity_condition")

    figure_distributions(data)
    figure_correlation_matrix(data)
    figure_scatter(data, "H", "fig_h_vs_oa.png", "Human-likeness against independently rated appropriateness")
    figure_scatter(data, "F", "fig_f_vs_oa.png", "Contextual fit against independently rated appropriateness")

    save_markdown(render(by_domain, by_model, ceiling, correlations, vif, condition), "descriptives")
    save_json({"descriptives_by_domain": by_domain.to_dict(orient="records"),
               "descriptives_by_model": by_model.to_dict(orient="records"),
               "ceiling_floor": ceiling.to_dict(orient="records"),
               "correlations": correlations.to_dict(orient="records"),
               "vif": vif.to_dict(orient="records"),
               "condition_number": condition.to_dict(orient="records")}, "phase3_results")
    print("Phase 3 complete: descriptives, separability, 4 figures")


def render(by_domain, by_model, ceiling, correlations, vif, condition) -> str:
    lines = ["# Descriptive statistics and dimension separability (Phase 3)", ""]

    lines += ["## Consensus score distributions by domain", "",
              "| Domain | Measure | N | Mean | Median | SD | IQR | Min | Max | Skew |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for _, r in by_domain.iterrows():
        lines.append(f"| {r['domain']} | {r['measure']} | {int(r['n'])} | {r['mean']:.3f} | {r['median']:.3f} | "
                     f"{r['sd']:.3f} | {r['iqr']:.3f} | {r['min']:.3f} | {r['max']:.3f} | {r['skew']:.2f} |")

    lines += ["", "## Ceiling and floor diagnostics", "",
              "`pct_at_scale_max` counts responses whose five-rater consensus sits exactly on the top of "
              "the scale. A high value means the outcome has almost no variance left to explain.", "",
              "| Domain | Measure | N | % at ceiling | % at floor | % >= 4.2 | SD | SD as % of range |",
              "|---|---|---:|---:|---:|---:|---:|---:|"]
    for _, r in ceiling.iterrows():
        def fmt(v):
            return "-" if pd.isna(v) else f"{v}"
        lines.append(f"| {r['domain']} | {r['measure']} | {int(r['n'])} | {fmt(r['pct_at_scale_max'])} | "
                     f"{fmt(r['pct_at_scale_min'])} | {fmt(r['pct_in_top_quintile'])} | {r['sd']} | "
                     f"{fmt(r['sd_as_pct_of_scale_range'])} |")

    lines += ["", "## Model profiles", "",
              "| Domain | Model | N | OA | E | D | F | H |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for _, r in by_model.iterrows():
        lines.append(f"| {r['domain']} | {r['model']} | {int(r['n'])} | {r['OA_mean']:.3f} | {r['E_mean']:.3f} | "
                     f"{r['D_mean']:.3f} | {r['F_mean']:.3f} | {r['H_mean']:.4f} |")

    lines += ["", "## Pairwise associations", "",
              "Spearman rho with 95 per cent prompt-cluster bootstrap intervals and Benjamini-Hochberg "
              "corrected p-values.", "",
              "| Domain | Pair | N | rho | 95% CI | FDR p | CI excludes 0 |",
              "|---|---|---:|---:|---|---:|---|"]
    for _, r in correlations.iterrows():
        lines.append(f"| {r['domain']} | {r['variable_a']}-{r['variable_b']} | {int(r['n'])} | "
                     f"{r['spearman_rho']:.3f} | [{r['cluster_boot_ci_low']:.3f}, {r['cluster_boot_ci_high']:.3f}] | "
                     f"{r['spearman_p_fdr']:.4f} | {'yes' if r['ci_excludes_zero'] else 'no'} |")

    lines += ["", "## Collinearity among profile dimensions", "",
              "| Domain | Dimension | N | R2 on the other three | VIF |", "|---|---|---:|---:|---:|"]
    for _, r in vif.iterrows():
        lines.append(f"| {r['domain']} | {r['dimension']} | {int(r['n'])} | {r['r_squared_on_others']} | {r['vif']} |")

    lines += ["", "## Condition number", "",
              "Condition numbers are computed on z-scored `H`, `E`, `D`, and `F` within each domain. "
              "They are reported as a diagnostic, not as a pass/fail threshold.", "",
              "| Domain | N | Condition number |", "|---|---:|---:|"]
    for _, r in condition.iterrows():
        lines.append(f"| {r['domain']} | {int(r['n'])} | {r['condition_number']:.3f} |")

    lines += ["", "## Figures", "",
              "- `fig_distributions_by_domain.png` - consensus distributions for OA/E/D/F/H",
              "- `fig_correlation_matrix.png` - separability matrix per domain",
              "- `fig_h_vs_oa.png` - human-likeness against OA",
              "- `fig_f_vs_oa.png` - contextual fit against OA", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
