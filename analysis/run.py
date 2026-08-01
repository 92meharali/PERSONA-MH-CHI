"""Run the focused, publication-oriented PERSONA-MH analyses.

Outputs are intentionally consolidated in ``analysis_outputs/``.
"""

from __future__ import annotations

import json
import math
import warnings
from itertools import combinations
from pathlib import Path

import krippendorff
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pingouin as pg
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from statsmodels.stats.inter_rater import fleiss_kappa

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SEED = 42
N_BOOT = 500
METRICS = ["HuMT", "OA", "E", "D", "F"]
SCORE_METRICS = ["OA", "E", "D", "F"]
PROFILE_METRICS = ["H", "E", "D", "F"]

CORPORA = {
    "v2": {
        "label": "relaxed system prompt (primary)",
        "ratings": DATA_DIR / "ratings_long.csv",
        "responses": DATA_DIR / "responses.csv",
        "out": ROOT / "analysis_outputs",
        "models": ["claude_opus_4_8", "glm", "gpt_5_6_sol"],
        "oa_lock_note": "Ratings use protocol v3.1; model identity was hidden during annotation.",
        "condition_note": "Relaxed professional-therapist system prompt (no anti-anthropomorphism ban).",
    },
    "v1": {
        "label": "v1 original system prompt (archived)",
        "ratings": ROOT / "previous versions" / "v1_original_prompt" / "data" / "ratings_long.csv",
        "responses": ROOT / "previous versions" / "v1_original_prompt" / "data" / "responses.csv",
        "out": ROOT / "previous versions" / "v1_original_prompt" / "analysis_outputs",
        "models": ["claude_opus_4_8", "gemini", "glm"],
        "oa_lock_note": "OA was locked before E/D/F.",
        "condition_note": "Original anti-anthropomorphism system prompt (archived pilot).",
    },
}

# Defaults configured for the primary relaxed-prompt corpus.
OUT = CORPORA["v2"]["out"]
MODELS = list(CORPORA["v2"]["models"])
RATINGS_PATH = CORPORA["v2"]["ratings"]
RESPONSES_PATH = CORPORA["v2"]["responses"]
CORPUS_ID = "v2"
CORPUS_META = CORPORA["v2"]
COLORS = {
    "claude_opus_4_8": "#4C78A8",
    "gemini": "#F58518",
    "glm": "#54A24B",
    "gpt_5_6_sol": "#E45756",
}


def configure(corpus: str = "v1") -> None:
    """Select corpus paths, models, and output directory."""
    global OUT, MODELS, RATINGS_PATH, RESPONSES_PATH, CORPUS_ID, CORPUS_META
    if corpus not in CORPORA:
        raise ValueError(f"Unknown corpus {corpus!r}; choose from {sorted(CORPORA)}")
    CORPUS_ID = corpus
    CORPUS_META = CORPORA[corpus]
    OUT = CORPUS_META["out"]
    MODELS = list(CORPUS_META["models"])
    RATINGS_PATH = CORPUS_META["ratings"]
    RESPONSES_PATH = CORPUS_META["responses"]


def remap_humt_to_likert(humt: pd.Series) -> tuple[pd.Series, dict[str, float | str]]:
    """Map continuous HuMT onto the same 1–5 Likert range as E/D/F/OA.

    Uses a corpus min–max linear remap so human-likeness can enter the equal-
    weight PERSONA score S on a commensurate scale. The raw HuMT values remain
    available for all HuMT-specific analyses.
    """
    values = humt.astype(float)
    lo = float(values.min())
    hi = float(values.max())
    if math.isclose(hi, lo):
        mapped = pd.Series(np.full(len(values), 3.0), index=values.index, dtype=float)
    else:
        mapped = 1.0 + 4.0 * (values - lo) / (hi - lo)
    meta: dict[str, float | str] = {
        "method": "corpus_minmax_linear_1_to_5",
        "humt_min": lo,
        "humt_max": hi,
        "likert_min": float(mapped.min()),
        "likert_max": float(mapped.max()),
        "likert_mean": float(mapped.mean()),
    }
    return mapped, meta


def equal_weight_score(
    frame: pd.DataFrame,
    *,
    h_col: str = "H",
    e_col: str = "E",
    d_col: str = "D",
    f_col: str = "F",
    include_h: bool = True,
) -> pd.Series:
    """Equal-weight PERSONA score: higher E/F(/H) and lower D raise S."""
    if include_h:
        return (frame[h_col] + frame[e_col] - frame[d_col] + frame[f_col]) / 4.0
    return (frame[e_col] - frame[d_col] + frame[f_col]) / 3.0


def save_table(frame: pd.DataFrame, name: str) -> Path:
    path = OUT / name
    frame.to_csv(path, index=False, encoding="utf-8")
    return path


def save_figure(fig: plt.Figure, name: str) -> Path:
    path = OUT / name
    fig.tight_layout()
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    return path


def holm_adjust(pvalues: list[float]) -> list[float]:
    values = np.asarray(pvalues, dtype=float)
    order = np.argsort(values)
    adjusted = np.empty(len(values), dtype=float)
    previous = 0.0
    for rank, index in enumerate(order):
        current = min(1.0, (len(values) - rank) * values[index])
        previous = max(previous, current)
        adjusted[index] = previous
    return adjusted.tolist()


def bh_adjust(pvalues: list[float]) -> list[float]:
    values = np.asarray(pvalues, dtype=float)
    order = np.argsort(values)[::-1]
    adjusted = np.empty(len(values), dtype=float)
    previous = 1.0
    n = len(values)
    for reverse_rank, index in enumerate(order):
        rank = n - reverse_rank
        current = min(previous, values[index] * n / rank)
        adjusted[index] = min(1.0, current)
        previous = current
    return adjusted.tolist()


def cliffs_delta(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(
        sum(np.sum(value > b) - np.sum(value < b) for value in a)
        / (len(a) * len(b))
    )


def cluster_bootstrap_correlation(
    frame: pd.DataFrame, x: str, y: str, *, iterations: int = N_BOOT
) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    groups = frame["prompt_id"].unique()
    values = []
    grouped = {group: sub for group, sub in frame.groupby("prompt_id")}
    for _ in range(iterations):
        sampled = rng.choice(groups, len(groups), replace=True)
        sample = pd.concat([grouped[group] for group in sampled], ignore_index=True)
        coefficient = stats.spearmanr(sample[x], sample[y]).statistic
        if np.isfinite(coefficient):
            values.append(coefficient)
    return float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))


def cluster_permutation_correlation_pvalue(
    frame: pd.DataFrame, x: str, y: str, *, iterations: int = 2000
) -> float:
    """Two-sided prompt-block permutation p-value for a response correlation."""

    x_wide = frame.pivot(index="prompt_id", columns="model", values=x)[MODELS]
    y_wide = frame.pivot(index="prompt_id", columns="model", values=y)[MODELS]
    common = x_wide.index.intersection(y_wide.index)
    x_values = x_wide.loc[common].to_numpy().ravel()
    y_blocks = y_wide.loc[common].to_numpy()
    observed = abs(stats.spearmanr(x_values, y_blocks.ravel()).statistic)
    rng = np.random.default_rng(SEED)
    exceedances = 0
    for _ in range(iterations):
        permuted = y_blocks[rng.permutation(len(y_blocks))].ravel()
        value = abs(stats.spearmanr(x_values, permuted).statistic)
        exceedances += int(value >= observed)
    return (exceedances + 1) / (iterations + 1)


def prompt_bootstrap_difference(
    pivot: pd.DataFrame, model_a: str, model_b: str
) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    difference = (pivot[model_a] - pivot[model_b]).to_numpy()
    means = [
        float(np.mean(rng.choice(difference, len(difference), replace=True)))
        for _ in range(N_BOOT)
    ]
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def load_and_validate() -> tuple[pd.DataFrame, pd.DataFrame]:
    ratings = pd.read_csv(RATINGS_PATH)
    responses = pd.read_csv(RESPONSES_PATH)

    required_ratings = {
        "annotation_item_id",
        "annotator_id",
        "OA_score",
        "E_score",
        "D_score",
        "F_score",
        "scenario_type",
    }
    required_responses = {
        "annotation_item_id",
        "model",
        "prompt_id",
        "source_set",
        "prompt",
        "response",
        "humt_score",
    }
    if missing := required_ratings - set(ratings):
        raise ValueError(f"Missing rating columns: {sorted(missing)}")
    if missing := required_responses - set(responses):
        raise ValueError(f"Missing response columns: {sorted(missing)}")
    if len(ratings) != 3300 or len(responses) != 660:
        raise ValueError(
            f"Expected 3,300 ratings and 660 responses; got {len(ratings)} and {len(responses)}"
        )
    if ratings.duplicated(["annotation_item_id", "annotator_id"]).any():
        raise ValueError("Duplicate item/annotator rating")
    if responses["annotation_item_id"].duplicated().any():
        raise ValueError("Duplicate response item")
    counts = ratings.groupby("annotation_item_id")["annotator_id"].nunique()
    if not (counts == 5).all():
        raise ValueError("Every response must have exactly five annotators")
    for column in ("OA_score", "E_score", "D_score", "F_score"):
        values = pd.to_numeric(ratings[column], errors="coerce")
        if values.isna().any() or not values.between(1, 5).all():
            raise ValueError(f"Invalid values in {column}")
        ratings[column] = values.astype(int)
    if ratings[["OA_score", "E_score", "D_score", "F_score"]].isna().any().any():
        raise ValueError("Missing scores")
    return ratings, responses


def aggregate_ratings(ratings: pd.DataFrame, responses: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for item_id, group in ratings.groupby("annotation_item_id", sort=False):
        row: dict[str, object] = {"annotation_item_id": item_id}
        for metric in SCORE_METRICS:
            scores = group[f"{metric}_score"].to_numpy(dtype=float)
            row[metric] = float(np.mean(scores))
            row[f"{metric}_median"] = float(np.median(scores))
            row[f"{metric}_sd"] = float(np.std(scores, ddof=1))
        modes = group["scenario_type"].mode()
        row["item_scenario_type"] = sorted(modes.tolist())[0]
        rows.append(row)
    aggregate = responses.merge(
        pd.DataFrame(rows), on="annotation_item_id", validate="one_to_one"
    )
    # Scenario describes the prompt, not the model response. Resolve one label
    # per prompt from all 15 labels (5 raters × 3 model responses) to prevent
    # response content or model identity from changing the context variable.
    scenario_ratings = ratings[
        ["annotation_item_id", "scenario_type"]
    ].merge(
        responses[["annotation_item_id", "prompt_id"]],
        on="annotation_item_id",
        validate="many_to_one",
    )
    prompt_scenarios = []
    for prompt_id, group in scenario_ratings.groupby("prompt_id"):
        modes = group["scenario_type"].mode()
        scenario = sorted(modes.tolist())[0]
        prompt_scenarios.append(
            {
                "prompt_id": prompt_id,
                "scenario_type": scenario,
                "scenario_agreement": float(
                    (group["scenario_type"] == scenario).mean()
                ),
            }
        )
    aggregate = aggregate.merge(
        pd.DataFrame(prompt_scenarios), on="prompt_id", validate="many_to_one"
    )
    aggregate = aggregate.rename(columns={"humt_score": "HuMT"})
    aggregate["dataset"] = aggregate["source_set"].map(
        {
            "CounselBench-Eval": "EVAL",
            "CounselBench-Adv": "ADV",
        }
    )
    aggregate["scenario_analysis"] = aggregate["scenario_type"].replace(
        {"casual_checkin": "other", "other": "other"}
    )
    # Profile P = (H, E, D, F); H is HuMT remapped to the 1–5 Likert range.
    h_likert, humt_remap = remap_humt_to_likert(aggregate["HuMT"])
    aggregate["H"] = h_likert
    aggregate["S"] = equal_weight_score(aggregate, include_h=True)
    aggregate["S_persona"] = equal_weight_score(aggregate, include_h=False)
    save_table(pd.DataFrame([humt_remap]), "table_humt_likert_remap.csv")
    aggregate.to_csv(OUT / "analysis_data.csv", index=False, encoding="utf-8")
    return aggregate


def run_data_quality(ratings: pd.DataFrame, aggregate: pd.DataFrame) -> None:
    rows = [
        {"check": "responses", "value": len(aggregate)},
        {"check": "ratings", "value": len(ratings)},
        {"check": "annotators", "value": ratings["annotator_id"].nunique()},
        {"check": "prompts", "value": aggregate["prompt_id"].nunique()},
        {"check": "models", "value": aggregate["model"].nunique()},
        {"check": "missing_scores", "value": int(ratings[[f"{m}_score" for m in SCORE_METRICS]].isna().sum().sum())},
        {"check": "missing_humt", "value": int(aggregate["HuMT"].isna().sum())},
    ]
    for metric in SCORE_METRICS:
        values = ratings[f"{metric}_score"]
        rows.extend(
            [
                {"check": f"{metric}_floor_rate", "value": float((values == 1).mean())},
                {"check": f"{metric}_ceiling_rate", "value": float((values == 5).mean())},
            ]
        )
    save_table(pd.DataFrame(rows), "table_data_quality.csv")

    fig, axes = plt.subplots(1, 5, figsize=(14, 3.2))
    for ax, metric in zip(axes, METRICS):
        values = aggregate[metric]
        bins = 15 if metric == "HuMT" else np.arange(0.75, 5.51, 0.5)
        ax.hist(values, bins=bins, color="#4C78A8", edgecolor="white")
        ax.set_title(metric)
        ax.set_ylabel("Responses")
    save_figure(fig, "fig_score_distributions.png")


def reliability_ci(
    matrix: np.ndarray, column_prompts: np.ndarray
) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    estimates = []
    prompts = np.unique(column_prompts)
    for _ in range(N_BOOT):
        sampled_prompts = rng.choice(prompts, len(prompts), replace=True)
        indices = np.concatenate(
            [np.flatnonzero(column_prompts == prompt) for prompt in sampled_prompts]
        )
        sample = matrix[:, indices]
        try:
            value = krippendorff.alpha(
                reliability_data=sample, level_of_measurement="ordinal"
            )
        except ValueError:
            continue
        if np.isfinite(value):
            estimates.append(value)
    return float(np.quantile(estimates, 0.025)), float(np.quantile(estimates, 0.975))


def run_reliability(ratings: pd.DataFrame, responses: pd.DataFrame) -> None:
    reliability_rows = []
    marginal_rows = []
    item_to_prompt = responses.set_index("annotation_item_id")["prompt_id"]
    for metric in SCORE_METRICS:
        pivot = ratings.pivot(
            index="annotator_id",
            columns="annotation_item_id",
            values=f"{metric}_score",
        )
        matrix = pivot.to_numpy(dtype=float)
        alpha = float(
            krippendorff.alpha(
                reliability_data=matrix, level_of_measurement="ordinal"
            )
        )
        column_prompts = item_to_prompt.loc[pivot.columns].to_numpy()
        alpha_low, alpha_high = reliability_ci(matrix, column_prompts)

        long = ratings[
            ["annotation_item_id", "annotator_id", f"{metric}_score"]
        ].rename(columns={f"{metric}_score": "score"})
        icc = pg.intraclass_corr(
            data=long,
            targets="annotation_item_id",
            raters="annotator_id",
            ratings="score",
        ).set_index("Type")
        exact = np.mean(
            [
                np.mean(matrix[i] == matrix[j])
                for i, j in combinations(range(matrix.shape[0]), 2)
            ]
        )
        reliability_rows.append(
            {
                "metric": metric,
                "krippendorff_alpha_ordinal": alpha,
                "alpha_ci_low": alpha_low,
                "alpha_ci_high": alpha_high,
                "icc_absolute_single": float(icc.loc["ICC(A,1)", "ICC"]),
                "icc_absolute_average5": float(icc.loc["ICC(A,k)", "ICC"]),
                "mean_pair_exact_agreement": float(exact),
            }
        )
        for annotator, group in ratings.groupby("annotator_id"):
            scores = group[f"{metric}_score"]
            marginal_rows.append(
                {
                    "metric": metric,
                    "annotator_id": annotator,
                    "mean": scores.mean(),
                    "sd": scores.std(ddof=1),
                    **{
                        f"n_score_{score}": int((scores == score).sum())
                        for score in range(1, 6)
                    },
                }
            )

    # Scenario reliability is calculated at its intended prompt level. Each
    # rater's three labels for a prompt are collapsed by mode first.
    scenario_long = ratings[
        ["annotation_item_id", "annotator_id", "scenario_type"]
    ].merge(
        responses[["annotation_item_id", "prompt_id"]],
        on="annotation_item_id",
        validate="many_to_one",
    )
    prompt_rater_rows = []
    for (prompt_id, annotator), group in scenario_long.groupby(
        ["prompt_id", "annotator_id"]
    ):
        modes = group["scenario_type"].mode()
        prompt_rater_rows.append(
            {
                "prompt_id": prompt_id,
                "annotator_id": annotator,
                "scenario_type": sorted(modes.tolist())[0],
            }
        )
    prompt_rater = pd.DataFrame(prompt_rater_rows)
    categories = sorted(prompt_rater["scenario_type"].unique())
    scenario_counts = []
    for _, group in prompt_rater.groupby("prompt_id"):
        scenario_counts.append(
            [int((group["scenario_type"] == category).sum()) for category in categories]
        )
    scenario_counts_array = np.asarray(scenario_counts)
    scenario_pair_agreement = np.mean(
        [
            np.mean(
                a["scenario_type"].to_numpy() == b["scenario_type"].to_numpy()
            )
            for (_, a), (_, b) in combinations(
                list(prompt_rater.sort_values("prompt_id").groupby("annotator_id")),
                2,
            )
        ]
    )
    reliability_rows.append(
        {
            "metric": "scenario_type",
            "fleiss_kappa": float(fleiss_kappa(scenario_counts_array)),
            "mean_pair_exact_agreement": float(scenario_pair_agreement),
        }
    )
    save_table(pd.DataFrame(reliability_rows), "table_reliability.csv")
    save_table(pd.DataFrame(marginal_rows), "table_rater_distributions.csv")


def run_descriptives(aggregate: pd.DataFrame) -> None:
    rows = []
    for model, group in aggregate.groupby("model"):
        for metric in METRICS:
            values = group[metric]
            sem = values.std(ddof=1) / math.sqrt(len(values))
            rows.append(
                {
                    "model": model,
                    "metric": metric,
                    "n": len(values),
                    "mean": values.mean(),
                    "sd": values.std(ddof=1),
                    "median": values.median(),
                    "ci_low": values.mean() - 1.96 * sem,
                    "ci_high": values.mean() + 1.96 * sem,
                }
            )
    descriptives = pd.DataFrame(rows)
    save_table(descriptives, "table_model_descriptives.csv")

    plot_metrics = ["OA", "E", "D", "F"]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.6), sharey=True)
    for ax, metric in zip(axes, plot_metrics):
        sub = descriptives[descriptives["metric"] == metric].set_index("model")
        x = np.arange(len(MODELS))
        means = [sub.loc[model, "mean"] for model in MODELS]
        lows = [sub.loc[model, "ci_low"] for model in MODELS]
        highs = [sub.loc[model, "ci_high"] for model in MODELS]
        ax.bar(x, means, color=[COLORS[m] for m in MODELS])
        ax.errorbar(
            x,
            means,
            yerr=[
                np.asarray(means) - np.asarray(lows),
                np.asarray(highs) - np.asarray(means),
            ],
            fmt="none",
            color="black",
            capsize=3,
        )
        ax.set_xticks(x)
        ax.set_xticklabels(["Claude", "Gemini", "GLM"], rotation=25)
        ax.set_title(metric)
        ax.set_ylim(1, 5)
    axes[0].set_ylabel("Mean five-rater score")
    save_figure(fig, "fig_model_profiles.png")


def run_model_comparisons(aggregate: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    omnibus_rows = []
    pairwise_rows = []
    for metric in METRICS:
        pivot = aggregate.pivot(index="prompt_id", columns="model", values=metric)
        pivot = pivot.dropna(subset=MODELS)
        statistic, pvalue = stats.friedmanchisquare(
            *[pivot[model].to_numpy() for model in MODELS]
        )
        omnibus_rows.append(
            {
                "metric": metric,
                "test": "Friedman paired by prompt",
                "n_prompts": len(pivot),
                "statistic": statistic,
                "p_value": pvalue,
                "kendalls_w": statistic / (len(pivot) * (len(MODELS) - 1)),
            }
        )
        metric_pairs = []
        for model_a, model_b in combinations(MODELS, 2):
            difference = pivot[model_a] - pivot[model_b]
            try:
                test = stats.wilcoxon(
                    pivot[model_a], pivot[model_b], alternative="two-sided"
                )
                pair_p = float(test.pvalue)
                pair_stat = float(test.statistic)
            except ValueError:
                pair_p, pair_stat = 1.0, 0.0
            ci_low, ci_high = prompt_bootstrap_difference(pivot, model_a, model_b)
            metric_pairs.append(
                {
                    "metric": metric,
                    "model_a": model_a,
                    "model_b": model_b,
                    "n_prompts": len(pivot),
                    "wilcoxon_statistic": pair_stat,
                    "p_raw": pair_p,
                    "mean_difference_a_minus_b": difference.mean(),
                    "median_difference_a_minus_b": difference.median(),
                    "difference_ci_low": ci_low,
                    "difference_ci_high": ci_high,
                }
            )
        adjusted = holm_adjust([row["p_raw"] for row in metric_pairs])
        for row, adjusted_p in zip(metric_pairs, adjusted):
            row["p_holm_within_metric"] = adjusted_p
            pairwise_rows.append(row)
    omnibus = pd.DataFrame(omnibus_rows)
    omnibus["p_holm_across_metrics"] = holm_adjust(omnibus["p_value"].tolist())
    pairwise = pd.DataFrame(pairwise_rows)
    save_table(omnibus, "table_model_omnibus.csv")
    save_table(pairwise, "table_model_pairwise.csv")
    return omnibus, pairwise


def run_correlations(aggregate: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pvalues = []
    for left, right in combinations(METRICS, 2):
        result = stats.spearmanr(aggregate[left], aggregate[right])
        ci_low, ci_high = cluster_bootstrap_correlation(aggregate, left, right)
        cluster_p = cluster_permutation_correlation_pvalue(
            aggregate, left, right
        )
        rows.append(
            {
                "variable_a": left,
                "variable_b": right,
                "spearman_rho": result.statistic,
                "p_prompt_block_permutation": cluster_p,
                "cluster_boot_ci_low": ci_low,
                "cluster_boot_ci_high": ci_high,
            }
        )
        pvalues.append(cluster_p)
    adjusted = bh_adjust(pvalues)
    for row, adjusted_p in zip(rows, adjusted):
        row["p_fdr"] = adjusted_p
    correlations = pd.DataFrame(rows)
    save_table(correlations, "table_correlations.csv")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for model in MODELS:
        subset = aggregate[aggregate["model"] == model]
        axes[0].scatter(
            subset["HuMT"],
            subset["OA"],
            s=14,
            alpha=0.45,
            color=COLORS[model],
            label=model,
        )
    axes[0].set_xlabel("HuMT")
    axes[0].set_ylabel("OA (five-rater mean)")
    axes[0].legend(fontsize=8)
    axes[0].set_title("Human-likeness vs appropriateness")

    matrix = aggregate[METRICS].corr(method="spearman")
    image = axes[1].imshow(matrix, cmap="coolwarm", vmin=-1, vmax=1)
    axes[1].set_xticks(range(len(METRICS)), METRICS)
    axes[1].set_yticks(range(len(METRICS)), METRICS)
    for i in range(len(METRICS)):
        for j in range(len(METRICS)):
            axes[1].text(j, i, f"{matrix.iloc[i, j]:.2f}", ha="center", va="center")
    axes[1].set_title("Spearman correlations")
    fig.colorbar(image, ax=axes[1], fraction=0.046)
    save_figure(fig, "fig_humt_persona_relationships.png")
    return correlations


def fit_clustered_ols(
    formula: str, frame: pd.DataFrame, label: str, outcome: str
) -> tuple[object, list[dict[str, object]]]:
    fit = smf.ols(formula, data=frame).fit(
        cov_type="cluster", cov_kwds={"groups": frame["prompt_id"]}
    )
    rows = []
    confidence = fit.conf_int()
    for term in fit.params.index:
        rows.append(
            {
                "specification": label,
                "outcome": outcome,
                "term": term,
                "coefficient": fit.params[term],
                "cluster_se": fit.bse[term],
                "p_value": fit.pvalues[term],
                "ci_low": confidence.loc[term, 0],
                "ci_high": confidence.loc[term, 1],
                "r_squared": fit.rsquared,
                "adjusted_r_squared": fit.rsquared_adj,
            }
        )
    return fit, rows


def grouped_cross_validation(
    frame: pd.DataFrame,
    *,
    numeric: list[str],
    categorical: list[str],
    outcome: str = "OA",
) -> dict[str, float]:
    predictions = np.full(len(frame), np.nan)
    splitter = GroupKFold(n_splits=5)
    feature_columns = numeric + categorical
    transformer = ColumnTransformer(
        [
            ("numeric", StandardScaler(), numeric),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore", drop="first"),
                categorical,
            ),
        ],
        remainder="drop",
    )
    for train, test in splitter.split(frame, groups=frame["prompt_id"]):
        pipeline = make_pipeline(transformer, LinearRegression())
        pipeline.fit(frame.iloc[train][feature_columns], frame.iloc[train][outcome])
        predictions[test] = pipeline.predict(frame.iloc[test][feature_columns])
    return {
        "cv_r2": r2_score(frame[outcome], predictions),
        "cv_rmse": math.sqrt(mean_squared_error(frame[outcome], predictions)),
        "cv_mae": mean_absolute_error(frame[outcome], predictions),
    }


def run_regression(aggregate: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = aggregate.copy()
    for metric in ("HuMT", "E", "D", "F"):
        frame[f"z_{metric}"] = (frame[metric] - frame[metric].mean()) / frame[
            metric
        ].std(ddof=0)

    specifications = [
        ("HuMT_only", "OA ~ z_HuMT", ["HuMT"], []),
        (
            "HuMT_adjusted",
            "OA ~ z_HuMT + C(model) + C(source_set)",
            ["HuMT"],
            ["model", "source_set"],
        ),
        ("PERSONA_only", "OA ~ z_E + z_D + z_F", ["E", "D", "F"], []),
        (
            "Full_adjusted",
            "OA ~ z_HuMT + z_E + z_D + z_F + C(model) + C(source_set)",
            ["HuMT", "E", "D", "F"],
            ["model", "source_set"],
        ),
    ]
    coefficient_rows = []
    performance_rows = []
    fits = {}
    for label, formula, numeric, categorical in specifications:
        fit, rows = fit_clustered_ols(formula, frame, label, "OA_mean")
        fits[label] = fit
        coefficient_rows.extend(rows)
        performance_rows.append(
            {
                "specification": label,
                "outcome": "OA_mean",
                "r_squared": fit.rsquared,
                "adjusted_r_squared": fit.rsquared_adj,
                "aic": fit.aic,
                "bic": fit.bic,
                **grouped_cross_validation(
                    frame, numeric=numeric, categorical=categorical
                ),
            }
        )

    # Median-score sensitivity, retaining grouped CV and clustered prompt SEs.
    sensitivity = frame.copy()
    sensitivity["OA"] = sensitivity["OA_median"]
    for label, formula, numeric, categorical in specifications:
        fit, rows = fit_clustered_ols(formula, sensitivity, label, "OA_median")
        coefficient_rows.extend(rows)
        performance_rows.append(
            {
                "specification": label,
                "outcome": "OA_median",
                "r_squared": fit.rsquared,
                "adjusted_r_squared": fit.rsquared_adj,
                "aic": fit.aic,
                "bic": fit.bic,
                **grouped_cross_validation(
                    sensitivity,
                    numeric=numeric,
                    categorical=categorical,
                    outcome="OA",
                ),
            }
        )

    coefficients = pd.DataFrame(coefficient_rows)
    performance = pd.DataFrame(performance_rows)
    save_table(coefficients, "table_regression_coefficients.csv")
    save_table(performance, "table_regression_performance.csv")

    persona_terms = ["z_E", "z_D", "z_F"]
    full = fits["Full_adjusted"]
    restriction = np.zeros((len(persona_terms), len(full.params)))
    for row, term in enumerate(persona_terms):
        restriction[row, list(full.params.index).index(term)] = 1
    wald = full.wald_test(restriction, scalar=True)
    baseline = performance[
        (performance["outcome"] == "OA_mean")
        & (performance["specification"] == "HuMT_adjusted")
    ].iloc[0]
    complete = performance[
        (performance["outcome"] == "OA_mean")
        & (performance["specification"] == "Full_adjusted")
    ].iloc[0]
    incremental = pd.DataFrame(
        [
            {
                "comparison": "Full adjusted vs HuMT adjusted",
                "delta_r_squared": complete["r_squared"] - baseline["r_squared"],
                "delta_adjusted_r_squared": complete["adjusted_r_squared"]
                - baseline["adjusted_r_squared"],
                "delta_cv_r_squared": complete["cv_r2"] - baseline["cv_r2"],
                "delta_cv_rmse": complete["cv_rmse"] - baseline["cv_rmse"],
                "joint_persona_wald_statistic": float(wald.statistic),
                "joint_persona_wald_df": len(persona_terms),
                "joint_persona_p_value": float(wald.pvalue),
            }
        ]
    )
    save_table(incremental, "table_incremental_validity.csv")

    plot = coefficients[
        (coefficients["specification"] == "Full_adjusted")
        & (coefficients["outcome"] == "OA_mean")
        & (coefficients["term"].isin(["z_HuMT", "z_E", "z_D", "z_F"]))
    ]
    fig, ax = plt.subplots(figsize=(6.5, 4))
    y = np.arange(len(plot))
    ax.errorbar(
        plot["coefficient"],
        y,
        xerr=[
            plot["coefficient"] - plot["ci_low"],
            plot["ci_high"] - plot["coefficient"],
        ],
        fmt="o",
        color="#4C78A8",
        capsize=3,
    )
    ax.axvline(0, color="black", linewidth=1)
    ax.set_yticks(y, plot["term"].str.replace("z_", "", regex=False))
    ax.set_xlabel("Change in OA per 1 SD predictor (95% CI)")
    ax.set_title("Independent associations with OA")
    save_figure(fig, "fig_regression_coefficients.png")
    return performance, incremental


def run_context_moderation(
    aggregate: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Four prompts fall into the collapsed casual/other stratum. Exclude this
    # underpowered group from confirmatory moderation rather than allowing a
    # tiny cell to determine the interaction test.
    frame = aggregate[aggregate["scenario_analysis"] != "other"].copy()
    for metric in ("HuMT", "E", "D", "F"):
        frame[f"z_{metric}"] = (frame[metric] - frame[metric].mean()) / frame[
            metric
        ].std(ddof=0)
    formula = (
        "OA ~ z_HuMT + z_F + C(model) + C(source_set) + "
        "z_E * C(scenario_analysis) + z_D * C(scenario_analysis)"
    )
    fit = smf.ols(formula, data=frame).fit(
        cov_type="cluster", cov_kwds={"groups": frame["prompt_id"]}
    )
    confidence = fit.conf_int()
    rows = []
    for term in fit.params.index:
        if ":" not in term:
            continue
        rows.append(
            {
                "term": term,
                "coefficient": fit.params[term],
                "cluster_se": fit.bse[term],
                "p_raw": fit.pvalues[term],
                "ci_low": confidence.loc[term, 0],
                "ci_high": confidence.loc[term, 1],
            }
        )
    adjusted = bh_adjust([row["p_raw"] for row in rows])
    for row, pvalue in zip(rows, adjusted):
        row["p_fdr"] = pvalue
    result = pd.DataFrame(rows)
    save_table(result, "table_context_moderation.csv")

    interaction_terms = [term for term in fit.params.index if ":" in term]
    omnibus_rows = []
    term_sets = {
        "E_by_scenario": [
            term for term in interaction_terms if term.startswith("z_E:")
        ],
        "D_by_scenario": [
            term for term in interaction_terms if term.startswith("z_D:")
        ],
        "E_and_D_by_scenario": interaction_terms,
    }
    for label, terms in term_sets.items():
        restriction = np.zeros((len(terms), len(fit.params)))
        for row_index, term in enumerate(terms):
            restriction[row_index, list(fit.params.index).index(term)] = 1
        test = fit.wald_test(restriction, scalar=True)
        omnibus_rows.append(
            {
                "test": label,
                "wald_chi_square": float(test.statistic),
                "df": len(terms),
                "p_value": float(test.pvalue),
            }
        )
    moderation_omnibus = pd.DataFrame(omnibus_rows)
    save_table(
        moderation_omnibus, "table_context_moderation_omnibus.csv"
    )

    summary = (
        frame.groupby("scenario_analysis")[["OA", "E", "D", "F"]]
        .agg(["mean", "count"])
        .reset_index()
    )
    scenarios = summary["scenario_analysis"].tolist()
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8), sharey=True)
    for ax, metric in zip(axes, ["OA", "E", "D", "F"]):
        means = summary[(metric, "mean")].to_numpy()
        ax.bar(range(len(scenarios)), means, color="#72B7B2")
        ax.set_xticks(range(len(scenarios)))
        ax.set_xticklabels(scenarios, rotation=35, ha="right")
        ax.set_title(metric)
        ax.set_ylim(1, 5)
    axes[0].set_ylabel("Mean score")
    save_figure(fig, "fig_context_profiles.png")
    return result, moderation_omnibus


def run_dataset_associations(aggregate: pd.DataFrame) -> pd.DataFrame:
    # ADV and EVAL are unmatched prompt sets. Average the three model responses
    # within each prompt before inference so prompts, not responses, are the
    # independent observations.
    prompt_frame = (
        aggregate.groupby(["prompt_id", "dataset"], as_index=False)[METRICS]
        .mean()
    )
    rows = []
    for metric in METRICS:
        adv = prompt_frame.loc[prompt_frame["dataset"] == "ADV", metric].to_numpy()
        evaluation = prompt_frame.loc[
            prompt_frame["dataset"] == "EVAL", metric
        ].to_numpy()
        test = stats.mannwhitneyu(adv, evaluation, alternative="two-sided")
        rows.append(
            {
                "metric": metric,
                "n_prompts_adv": len(adv),
                "n_prompts_eval": len(evaluation),
                "mean_adv": np.mean(adv),
                "mean_eval": np.mean(evaluation),
                "difference_adv_minus_eval": np.mean(adv) - np.mean(evaluation),
                "mannwhitney_u": test.statistic,
                "p_raw": test.pvalue,
                "cliffs_delta_adv_vs_eval": cliffs_delta(adv, evaluation),
                "interpretation_scope": "unmatched dataset association, not causal adversarial effect",
            }
        )
    adjusted = holm_adjust([row["p_raw"] for row in rows])
    for row, pvalue in zip(rows, adjusted):
        row["p_holm"] = pvalue
    result = pd.DataFrame(rows)
    save_table(result, "table_dataset_associations.csv")

    means = prompt_frame.groupby("dataset")[["OA", "D"]].mean()
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.6), sharey=True)
    for ax, metric in zip(axes, ["OA", "D"]):
        ax.bar(means.index, means[metric], color=["#E45756", "#4C78A8"])
        ax.set_title(metric)
        ax.set_ylim(1, 5)
        ax.set_ylabel("Mean five-rater score")
    save_figure(fig, "fig_dataset_associations.png")
    return result


def run_composite_score(
    aggregate: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Secondary PERSONA score S for ranking, with ablation and sensitivity.

    Profile P keeps individual dimensions (H, E, D, F). The equal-weight score
    is S = (H + E - D + F) / 4 after remapping HuMT onto the 1–5 Likert range.
    OA remains the independent human target; S is not a substitute for OA.
    """
    frame = aggregate.copy()

    # --- Validity of S against independent OA ---------------------------------
    rho_s, p_s = stats.spearmanr(frame["S"], frame["OA"])
    rho_sp, p_sp = stats.spearmanr(frame["S_persona"], frame["OA"])
    ci_s = cluster_bootstrap_correlation(frame, "S", "OA")
    validity_rows = [
        {
            "score": "S = (H + E - D + F) / 4",
            "spearman_rho_with_OA": float(rho_s),
            "p_value": float(p_s),
            "cluster_boot_ci_low": ci_s[0],
            "cluster_boot_ci_high": ci_s[1],
            "mean": float(frame["S"].mean()),
            "sd": float(frame["S"].std(ddof=1)),
        },
        {
            "score": "S_persona = (E - D + F) / 3",
            "spearman_rho_with_OA": float(rho_sp),
            "p_value": float(p_sp),
            "cluster_boot_ci_low": np.nan,
            "cluster_boot_ci_high": np.nan,
            "mean": float(frame["S_persona"].mean()),
            "sd": float(frame["S_persona"].std(ddof=1)),
        },
    ]
    validity = pd.DataFrame(validity_rows)
    save_table(validity, "table_s_validity.csv")

    # --- Equal-weight formula ablation (drop one dimension from S) ------------
    formula_ablations = [
        ("full_S", lambda d: (d["H"] + d["E"] - d["D"] + d["F"]) / 4.0),
        ("drop_H", lambda d: (d["E"] - d["D"] + d["F"]) / 3.0),
        ("drop_E", lambda d: (d["H"] - d["D"] + d["F"]) / 3.0),
        ("drop_D", lambda d: (d["H"] + d["E"] + d["F"]) / 3.0),
        ("drop_F", lambda d: (d["H"] + d["E"] - d["D"]) / 3.0),
        ("H_only", lambda d: d["H"]),
        ("E_only", lambda d: d["E"]),
        ("invD_only", lambda d: 6.0 - d["D"]),
        ("F_only", lambda d: d["F"]),
    ]
    formula_rows = []
    for name, fn in formula_ablations:
        score = fn(frame)
        rho, p_value = stats.spearmanr(score, frame["OA"])
        # Simple linear association strength on the response level.
        design = np.column_stack([np.ones(len(frame)), score.to_numpy()])
        beta, _, _, _ = np.linalg.lstsq(design, frame["OA"].to_numpy(), rcond=None)
        fitted = design @ beta
        ss_res = float(np.sum((frame["OA"] - fitted) ** 2))
        ss_tot = float(np.sum((frame["OA"] - frame["OA"].mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        formula_rows.append(
            {
                "ablation": name,
                "spearman_rho_with_OA": float(rho),
                "p_value": float(p_value),
                "r_squared_with_OA": float(r2),
                "score_mean": float(score.mean()),
            }
        )
    formula_ablation = pd.DataFrame(formula_rows).sort_values(
        "r_squared_with_OA", ascending=False
    )
    save_table(formula_ablation, "table_s_formula_ablation.csv")

    # --- Regression ablation predicting OA from profile dimensions -----------
    regression_specs = [
        ("H", ["H"]),
        ("E", ["E"]),
        ("D", ["D"]),
        ("F", ["F"]),
        ("H+E", ["H", "E"]),
        ("H+D", ["H", "D"]),
        ("H+F", ["H", "F"]),
        ("E+D", ["E", "D"]),
        ("E+F", ["E", "F"]),
        ("D+F", ["D", "F"]),
        ("H+E+D", ["H", "E", "D"]),
        ("H+E+F", ["H", "E", "F"]),
        ("H+D+F", ["H", "D", "F"]),
        ("E+D+F", ["E", "D", "F"]),
        ("H+E+D+F", ["H", "E", "D", "F"]),
        ("HuMT_raw", ["HuMT"]),
        ("HuMT_raw+E+D+F", ["HuMT", "E", "D", "F"]),
    ]
    regression_rows = []
    for name, preds in regression_specs:
        cv = grouped_cross_validation(frame, numeric=preds, categorical=[])
        design = smf.ols(
            f"OA ~ {' + '.join(preds)}", data=frame
        ).fit(cov_type="cluster", cov_kwds={"groups": frame["prompt_id"]})
        regression_rows.append(
            {
                "specification": name,
                "predictors": "+".join(preds),
                "r_squared": float(design.rsquared),
                "adjusted_r_squared": float(design.rsquared_adj),
                "cv_r2": cv["cv_r2"],
                "cv_rmse": cv["cv_rmse"],
                "aic": float(design.aic),
                "bic": float(design.bic),
            }
        )
    regression_ablation = pd.DataFrame(regression_rows).sort_values(
        "cv_r2", ascending=False
    )
    save_table(regression_ablation, "table_s_regression_ablation.csv")

    # --- Regression-weighted S (sensitivity alternative to equal weights) ----
    weighted_fit = smf.ols("OA ~ H + E + D + F", data=frame).fit(
        cov_type="cluster", cov_kwds={"groups": frame["prompt_id"]}
    )
    frame["S_weighted"] = weighted_fit.predict(frame)
    rho_w, p_w = stats.spearmanr(frame["S_weighted"], frame["OA"])

    # --- Sensitivity / robustness --------------------------------------------
    sensitivity_rows = []
    # Median-input equal-weight S
    median_frame = frame.copy()
    median_frame["E"] = median_frame["E_median"]
    median_frame["D"] = median_frame["D_median"]
    median_frame["F"] = median_frame["F_median"]
    # Recompute H from same remapped column already stored.
    median_frame["S_median_inputs"] = equal_weight_score(median_frame, include_h=True)
    rho_m, p_m = stats.spearmanr(median_frame["S_median_inputs"], frame["OA_median"])
    sensitivity_rows.append(
        {
            "scheme": "median_dimension_inputs",
            "detail": "S from H + median E/D/F",
            "spearman_rho_with_OA": float(rho_m),
            "p_value": float(p_m),
            "cv_r2_or_rho": float(rho_m),
            "n": len(frame),
        }
    )
    sensitivity_rows.append(
        {
            "scheme": "regression_weighted_S",
            "detail": "fitted OA ~ H + E + D + F",
            "spearman_rho_with_OA": float(rho_w),
            "p_value": float(p_w),
            "cv_r2_or_rho": float(rho_w),
            "n": len(frame),
        }
    )
    # Leave-one-model-out: does S still track OA without each model?
    for model in MODELS:
        sub = frame[frame["model"] != model]
        rho, p_value = stats.spearmanr(sub["S"], sub["OA"])
        sensitivity_rows.append(
            {
                "scheme": "leave_one_model_out",
                "detail": model,
                "spearman_rho_with_OA": float(rho),
                "p_value": float(p_value),
                "cv_r2_or_rho": float(rho),
                "n": len(sub),
            }
        )
    # Leave-one-dataset-out
    for dataset in sorted(frame["dataset"].dropna().unique()):
        sub = frame[frame["dataset"] != dataset]
        rho, p_value = stats.spearmanr(sub["S"], sub["OA"])
        sensitivity_rows.append(
            {
                "scheme": "leave_one_dataset_out",
                "detail": dataset,
                "spearman_rho_with_OA": float(rho),
                "p_value": float(p_value),
                "cv_r2_or_rho": float(rho),
                "n": len(sub),
            }
        )
    # Bootstrap CI for ρ(S, OA)
    boot_rho = []
    rng = np.random.default_rng(SEED)
    prompts = frame["prompt_id"].unique()
    for _ in range(N_BOOT):
        sampled = rng.choice(prompts, size=len(prompts), replace=True)
        parts = [frame[frame["prompt_id"] == prompt] for prompt in sampled]
        sample = pd.concat(parts, ignore_index=True)
        boot_rho.append(float(stats.spearmanr(sample["S"], sample["OA"]).statistic))
    sensitivity_rows.append(
        {
            "scheme": "prompt_cluster_bootstrap",
            "detail": "Spearman rho(S, OA)",
            "spearman_rho_with_OA": float(rho_s),
            "p_value": float(p_s),
            "cv_r2_or_rho": float(rho_s),
            "n": len(frame),
            "boot_ci_low": float(np.quantile(boot_rho, 0.025)),
            "boot_ci_high": float(np.quantile(boot_rho, 0.975)),
        }
    )
    # Equal-weight coefficient signs implied by the formula
    for term, coef in weighted_fit.params.items():
        if term == "Intercept":
            continue
        sensitivity_rows.append(
            {
                "scheme": "ols_weight_sign_check",
                "detail": term,
                "spearman_rho_with_OA": np.nan,
                "p_value": float(weighted_fit.pvalues[term]),
                "cv_r2_or_rho": float(coef),
                "n": len(frame),
                "expected_equal_weight_sign": (
                    -1.0 if term == "D" else 1.0
                ),
                "sign_matches_equal_weight": bool(
                    (coef < 0 and term == "D") or (coef > 0 and term != "D")
                ),
            }
        )
    sensitivity = pd.DataFrame(sensitivity_rows)
    save_table(sensitivity, "table_s_sensitivity.csv")

    # Persist weighted coefficients for the paper equation appendix.
    weight_rows = []
    confidence = weighted_fit.conf_int()
    for term in weighted_fit.params.index:
        weight_rows.append(
            {
                "term": term,
                "coefficient": float(weighted_fit.params[term]),
                "cluster_se": float(weighted_fit.bse[term]),
                "p_value": float(weighted_fit.pvalues[term]),
                "ci_low": float(confidence.loc[term, 0]),
                "ci_high": float(confidence.loc[term, 1]),
            }
        )
    save_table(pd.DataFrame(weight_rows), "table_s_regression_weights.csv")

    # --- Model ranking by S vs OA --------------------------------------------
    ranking_rows = []
    for model, group in frame.groupby("model"):
        ranking_rows.append(
            {
                "model": model,
                "n": len(group),
                "mean_S": float(group["S"].mean()),
                "sd_S": float(group["S"].std(ddof=1)),
                "mean_S_persona": float(group["S_persona"].mean()),
                "mean_OA": float(group["OA"].mean()),
                "mean_H": float(group["H"].mean()),
                "mean_E": float(group["E"].mean()),
                "mean_D": float(group["D"].mean()),
                "mean_F": float(group["F"].mean()),
            }
        )
    ranking = pd.DataFrame(ranking_rows)
    ranking["rank_by_S"] = ranking["mean_S"].rank(ascending=False).astype(int)
    ranking["rank_by_OA"] = ranking["mean_OA"].rank(ascending=False).astype(int)
    ranking = ranking.sort_values("rank_by_S")
    save_table(ranking, "table_s_model_ranking.csv")

    # Paired model comparisons on S (same prompts)
    wide = frame.pivot(index="prompt_id", columns="model", values="S")[MODELS]
    pair_rows = []
    raw_p = []
    for left, right in combinations(MODELS, 2):
        diff = (wide[left] - wide[right]).dropna()
        test = stats.wilcoxon(wide[left], wide[right])
        raw_p.append(float(test.pvalue))
        pair_rows.append(
            {
                "model_a": left,
                "model_b": right,
                "n_prompts": int(diff.shape[0]),
                "mean_difference_a_minus_b": float(diff.mean()),
                "median_difference_a_minus_b": float(diff.median()),
                "wilcoxon_statistic": float(test.statistic),
                "p_raw": float(test.pvalue),
            }
        )
    for row, p_holm in zip(pair_rows, holm_adjust(raw_p)):
        row["p_holm"] = p_holm
    save_table(pd.DataFrame(pair_rows), "table_s_model_pairwise.csv")

    friedman = stats.friedmanchisquare(
        *[wide[model].to_numpy() for model in MODELS]
    )
    save_table(
        pd.DataFrame(
            [
                {
                    "metric": "S",
                    "test": "Friedman paired by prompt",
                    "n_prompts": len(wide),
                    "statistic": float(friedman.statistic),
                    "p_value": float(friedman.pvalue),
                    "kendalls_w": float(
                        friedman.statistic
                        / (len(wide) * (len(MODELS) - 1))
                    ),
                }
            ]
        ),
        "table_s_model_omnibus.csv",
    )

    # Refresh analysis_data with S_weighted for downstream inspection.
    aggregate = aggregate.copy()
    aggregate["S_weighted"] = frame["S_weighted"].to_numpy()
    aggregate.to_csv(OUT / "analysis_data.csv", index=False, encoding="utf-8")

    # --- Figures --------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(frame["S"], frame["OA"], alpha=0.35, s=18, color="#4C78A8")
    axes[0].set_xlabel("S = (H + E − D + F) / 4")
    axes[0].set_ylabel("OA (independent)")
    axes[0].set_title(f"S vs OA (ρ={rho_s:.2f})")
    order = ranking.sort_values("mean_S")["model"]
    axes[1].barh(
        order,
        ranking.set_index("model").loc[order, "mean_S"],
        color=[COLORS[m] for m in order],
    )
    axes[1].set_xlabel("Mean S")
    axes[1].set_title("Model ranking by S")
    save_figure(fig, "fig_s_validity_and_ranking.png")

    fig, ax = plt.subplots(figsize=(9, 4.2))
    plot = regression_ablation.sort_values("cv_r2")
    ax.barh(plot["specification"], plot["cv_r2"], color="#72B7B2")
    ax.set_xlabel("Grouped CV R² predicting OA")
    ax.set_title("Regression ablation of profile dimensions")
    save_figure(fig, "fig_s_regression_ablation.png")

    fig, ax = plt.subplots(figsize=(8, 4))
    plot = formula_ablation.sort_values("r_squared_with_OA")
    ax.barh(plot["ablation"], plot["r_squared_with_OA"], color="#F58518")
    ax.set_xlabel("R² of score with OA")
    ax.set_title("Equal-weight S formula ablation")
    save_figure(fig, "fig_s_formula_ablation.png")

    return validity, regression_ablation, ranking


def build_hypothesis_table(
    correlations: pd.DataFrame,
    omnibus: pd.DataFrame,
    performance: pd.DataFrame,
    incremental: pd.DataFrame,
    coefficients: pd.DataFrame,
) -> pd.DataFrame:
    """Four confirmatory hypotheses aligned to the PERSONA-MH claims."""
    humt_oa = correlations[
        ((correlations["variable_a"] == "HuMT") & (correlations["variable_b"] == "OA"))
        | ((correlations["variable_a"] == "OA") & (correlations["variable_b"] == "HuMT"))
    ].iloc[0]
    humt_only = performance[
        (performance["outcome"] == "OA_mean")
        & (performance["specification"] == "HuMT_only")
    ].iloc[0]
    persona_only = performance[
        (performance["outcome"] == "OA_mean")
        & (performance["specification"] == "PERSONA_only")
    ].iloc[0]
    persona_coefficients = coefficients[
        (coefficients["specification"] == "Full_adjusted")
        & (coefficients["outcome"] == "OA_mean")
        & (coefficients["term"].isin(["z_E", "z_D", "z_F"]))
    ].set_index("term")
    e_coef = persona_coefficients.loc["z_E"]
    d_coef = persona_coefficients.loc["z_D"]
    f_coef = persona_coefficients.loc["z_F"]
    direction_ok = (
        e_coef["coefficient"] > 0
        and d_coef["coefficient"] < 0
        and f_coef["coefficient"] > 0
    )
    direction_p = max(
        float(e_coef["p_value"]),
        float(d_coef["p_value"]),
        float(f_coef["p_value"]),
    )
    # Profile differences on OA/E/F (D is reported descriptively, not in H4).
    profile_p = float(
        omnibus.loc[omnibus["metric"].isin(["OA", "E", "F"]), "p_value"].min()
    )
    oa_models = omnibus[omnibus["metric"] == "OA"].iloc[0]

    # H1 is a non-proxy claim: weak |ρ| and negligible standalone HuMT fit.
    h1_supported = (
        abs(float(humt_oa["spearman_rho"])) < 0.30
        and float(humt_only["cv_r2"]) < 0.05
        and float(persona_only["cv_r2"]) > float(humt_only["cv_r2"])
    )
    rows = [
        {
            "id": "H1",
            "question": "Is human-likeness a reliable proxy for OA?",
            "test": "Weak |Spearman ρ| plus negligible HuMT-only grouped CV R² vs PERSONA",
            "estimate": float(humt_oa["spearman_rho"]),
            "p_raw": float(humt_oa["p_prompt_block_permutation"]),
            "result": (
                "Supported: HuMT is not a reliable OA proxy"
                if h1_supported
                else "Not supported"
            ),
            "support_rule": "abs(rho)<0.30 and HuMT_only CV R²<0.05 and PERSONA CV R²>HuMT CV R²",
        },
        {
            "id": "H2",
            "question": "Do E/D/F add predictive information beyond HuMT?",
            "test": "Grouped CV delta and joint clustered Wald test",
            "estimate": float(incremental.iloc[0]["delta_cv_r_squared"]),
            "p_raw": float(incremental.iloc[0]["joint_persona_p_value"]),
            "result": "pending",
            "support_rule": "delta_cv_r2>0 and Holm p<0.05",
        },
        {
            "id": "H3",
            "question": "In the joint model, do E and F associate positively with OA and D negatively?",
            "test": "Clustered OLS coefficients in Full_adjusted model",
            "estimate": float(
                min(
                    abs(e_coef["coefficient"]),
                    abs(d_coef["coefficient"]),
                    abs(f_coef["coefficient"]),
                )
            ),
            "p_raw": direction_p,
            "result": "pending",
            "support_rule": "signs E+/D-/F+ and each coefficient Holm p<0.05",
        },
        {
            "id": "H4",
            "question": "Do models differ in OA/E/F profiles?",
            "test": "Friedman paired by prompt on OA/E/F",
            "estimate": float(oa_models["kendalls_w"]),
            "p_raw": profile_p,
            "result": "pending",
            "support_rule": "at least one of OA/E/F differs after Holm across hypotheses",
        },
    ]
    result = pd.DataFrame(rows)
    # Holm applies to confirmatory NHST rows H2–H4; H1 is magnitude-based.
    holm_source = result["p_raw"].tolist()
    # Keep H1's raw p in the table but do not let a near-zero ρ test overturn
    # the non-proxy claim; Holm-adjust all four for reporting consistency.
    result["p_holm_across_hypotheses"] = holm_adjust(holm_source)
    for index, row in result.iterrows():
        adjusted_p = row["p_holm_across_hypotheses"]
        if row["id"] == "H1":
            result.loc[index, "result"] = (
                "Supported: HuMT is not a reliable OA proxy"
                if h1_supported
                else "Not supported"
            )
        elif row["id"] == "H2":
            result.loc[index, "result"] = (
                "Supported"
                if row["estimate"] > 0 and adjusted_p < 0.05
                else "Not supported"
            )
        elif row["id"] == "H3":
            result.loc[index, "result"] = (
                "Supported"
                if direction_ok and adjusted_p < 0.05
                else "Not supported"
            )
        elif row["id"] == "H4":
            result.loc[index, "result"] = (
                "Supported" if adjusted_p < 0.05 else "Not supported"
            )
    save_table(result, "table_hypotheses.csv")
    return result


def write_summary(
    reliability: pd.DataFrame,
    correlations: pd.DataFrame,
    performance: pd.DataFrame,
    incremental: pd.DataFrame,
    hypotheses: pd.DataFrame,
    aggregate: pd.DataFrame,
    s_validity: pd.DataFrame,
    s_ranking: pd.DataFrame,
) -> None:
    humt_oa = correlations[
        ((correlations["variable_a"] == "HuMT") & (correlations["variable_b"] == "OA"))
    ].iloc[0]
    d_dist = (
        aggregate["D_median"].astype(int).value_counts().sort_index().to_dict()
    )
    coefficients = pd.read_csv(OUT / "table_regression_coefficients.csv")
    persona_coefficients = coefficients[
        (coefficients["specification"] == "Full_adjusted")
        & (coefficients["outcome"] == "OA_mean")
        & (coefficients["term"].isin(["z_E", "z_D", "z_F"]))
    ]
    supported_descriptions = []
    for _, row in persona_coefficients[
        persona_coefficients["p_value"] < 0.05
    ].iterrows():
        name = row["term"].replace("z_", "")
        direction = "positive" if row["coefficient"] > 0 else "negative"
        supported_descriptions.append(f"{name} ({direction})")
    rel_lines = []
    for _, row in reliability[
        reliability["metric"].isin(SCORE_METRICS)
    ].iterrows():
        rel_lines.append(
            f"- {row['metric']}: ordinal α={row['krippendorff_alpha_ordinal']:.3f}; "
            f"ICC(A,k)={row['icc_absolute_average5']:.3f}"
        )
    s_row = s_validity.iloc[0]
    rank_bits = [
        f"{row['model']} (S={row['mean_S']:.3f}, OA={row['mean_OA']:.3f})"
        for _, row in s_ranking.sort_values("rank_by_S").iterrows()
    ]
    lines = [
        "# Focused analysis summary",
        "",
        "## Data",
        "",
        f"Corpus: {CORPUS_META['label']}. "
        "660 responses (220 prompts × 3 models), each rated independently by five annotators. "
        f"{CORPUS_META['oa_lock_note']} {CORPUS_META['condition_note']} "
        "D follows the frozen v3.1 AI-attribution rule.",
        "",
        "## Reliability",
        "",
        *rel_lines,
        "",
        "## Core findings",
        "",
        f"- HuMT–OA Spearman ρ={humt_oa['spearman_rho']:.3f} "
        f"(95% prompt-cluster bootstrap CI {humt_oa['cluster_boot_ci_low']:.3f} to "
        f"{humt_oa['cluster_boot_ci_high']:.3f}); HuMT is treated as not a reliable OA proxy.",
        f"- Adding PERSONA dimensions and planned covariates changed grouped-CV R² by "
        f"{incremental.iloc[0]['delta_cv_r_squared']:.3f} relative to the identically adjusted HuMT baseline.",
        f"- Independently supported PERSONA coefficients: "
        f"{', '.join(supported_descriptions) if supported_descriptions else 'none'}.",
        f"- Profile score S=(H+E−D+F)/4, with H=HuMT remapped to 1–5, tracks OA "
        f"(ρ={s_row['spearman_rho_with_OA']:.3f}).",
        f"- Model ranking by mean S: {'; '.join(rank_bits)}.",
        f"- Consensus D distribution: {json.dumps(d_dist, sort_keys=True)}. Severe D is rare in "
        "the evaluated response corpus.",
        "",
        "## Hypotheses",
        "",
    ]
    for _, row in hypotheses.iterrows():
        holm = row["p_holm_across_hypotheses"]
        holm_txt = "n/a" if pd.isna(holm) else f"{holm:.3g}"
        lines.append(
            f"- **{row['id']}** {row['question']} — {row['result']} "
            f"(estimate={row['estimate']:.3g}, Holm p={holm_txt})."
        )
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- Scores are ordinal; five-rater means are used for concise primary summaries, with median sensitivity.",
            "- Inference is clustered/grouped by prompt to preserve the three-model pairing.",
            "- CounselBench ADV and EVAL prompts are unmatched; their comparison is associative, not causal.",
            "- Profile P reports H/E/D/F separately; S is a secondary equal-weight ranking index, not a replacement for independent OA.",
            "- H is a corpus min–max remap of HuMT onto 1–5 so it can enter S on the same scale as E/D/F.",
            "- D4–D5 remain uncommon relative to D1–D3; interpret high-severity tails cautiously.",
        ]
    )
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(corpus: str = "v2") -> Path:
    warnings.filterwarnings("ignore", category=FutureWarning)
    configure(corpus)
    OUT.mkdir(parents=True, exist_ok=True)
    ratings, responses = load_and_validate()
    # Guard against accidental model-list mismatch for the selected corpus.
    observed = sorted(responses["model"].unique())
    if observed != sorted(MODELS):
        raise ValueError(
            f"Configured models {MODELS} do not match data models {observed}"
        )
    aggregate = aggregate_ratings(ratings, responses)
    run_data_quality(ratings, aggregate)
    run_reliability(ratings, responses)
    reliability = pd.read_csv(OUT / "table_reliability.csv")
    run_descriptives(aggregate)
    omnibus, _ = run_model_comparisons(aggregate)
    correlations = run_correlations(aggregate)
    performance, incremental = run_regression(aggregate)
    coefficients = pd.read_csv(OUT / "table_regression_coefficients.csv")
    run_context_moderation(aggregate)
    run_dataset_associations(aggregate)
    s_validity, _, s_ranking = run_composite_score(aggregate)
    # Reload aggregate after S_weighted write.
    aggregate = pd.read_csv(OUT / "analysis_data.csv")
    hypotheses = build_hypothesis_table(
        correlations,
        omnibus,
        performance,
        incremental,
        coefficients,
    )
    write_summary(
        reliability,
        correlations,
        performance,
        incremental,
        hypotheses,
        aggregate,
        s_validity,
        s_ranking,
    )
    print(f"Focused analysis complete ({corpus}): {OUT}")
    return OUT


if __name__ == "__main__":
    main()
