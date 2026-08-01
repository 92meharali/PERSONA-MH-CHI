"""Compare v1 (original prompt) vs v2 (relaxed prompt) PERSONA ratings."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .run import ROOT, SCORE_METRICS, cliffs_delta, holm_adjust

OUT = ROOT / "analysis_outputs_compare"
SHARED_MODELS = ["claude_opus_4_8", "glm"]


def _aggregate(ratings: pd.DataFrame, responses: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for item_id, group in ratings.groupby("annotation_item_id", sort=False):
        row: dict[str, object] = {"annotation_item_id": item_id}
        for metric in SCORE_METRICS:
            scores = group[f"{metric}_score"].to_numpy(dtype=float)
            row[metric] = float(np.mean(scores))
            row[f"{metric}_median"] = float(np.median(scores))
        rows.append(row)
    frame = responses.merge(pd.DataFrame(rows), on="annotation_item_id", validate="one_to_one")
    frame = frame.rename(columns={"humt_score": "HuMT"})
    frame["dataset"] = frame["source_set"].map(
        {"CounselBench-Eval": "EVAL", "CounselBench-Adv": "ADV"}
    )
    return frame


def _consensus_d_counts(ratings: pd.DataFrame) -> dict[int, int]:
    med = ratings.groupby("annotation_item_id")["D_score"].median()
    return {int(k): int(v) for k, v in med.value_counts().sort_index().items()}


def run_comparison() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    v1_ratings = pd.read_csv(ROOT / "data" / "ratings_long.csv")
    v2_ratings = pd.read_csv(ROOT / "data" / "ratings_long_v2.csv")
    v1_resp = pd.read_csv(ROOT / "data" / "responses.csv")
    v2_resp = pd.read_csv(ROOT / "data" / "responses_v2.csv")
    v1 = _aggregate(v1_ratings, v1_resp)
    v2 = _aggregate(v2_ratings, v2_resp)
    v1["condition"] = "v1_original_prompt"
    v2["condition"] = "v2_relaxed_prompt"

    # --- Corpus-level descriptives -------------------------------------------
    desc_rows = []
    for label, frame in [("v1", v1), ("v2", v2)]:
        for metric in ["HuMT", "OA", "E", "D", "F"]:
            desc_rows.append(
                {
                    "condition": label,
                    "metric": metric,
                    "n": len(frame),
                    "mean": float(frame[metric].mean()),
                    "sd": float(frame[metric].std(ddof=1)),
                    "median": float(frame[metric].median()),
                }
            )
    descriptives = pd.DataFrame(desc_rows)
    descriptives.to_csv(OUT / "table_condition_descriptives.csv", index=False)

    d_dist = pd.DataFrame(
        [
            {"condition": "v1", "D_median": k, "n_responses": v}
            for k, v in _consensus_d_counts(v1_ratings).items()
        ]
        + [
            {"condition": "v2", "D_median": k, "n_responses": v}
            for k, v in _consensus_d_counts(v2_ratings).items()
        ]
    )
    d_dist.to_csv(OUT / "table_condition_d_distribution.csv", index=False)

    # --- Unmatched corpus association (all responses) ------------------------
    # Prompts are shared, but model sets differ (gemini vs gpt). Treat full-
    # corpus tests as associative condition contrasts, then add shared-model
    # paired tests below.
    assoc_rows = []
    for metric in ["HuMT", "OA", "E", "D", "F"]:
        a = v1[metric].to_numpy()
        b = v2[metric].to_numpy()
        test = stats.mannwhitneyu(a, b, alternative="two-sided")
        assoc_rows.append(
            {
                "scope": "all_responses_unmatched_models",
                "metric": metric,
                "mean_v1": float(np.mean(a)),
                "mean_v2": float(np.mean(b)),
                "difference_v2_minus_v1": float(np.mean(b) - np.mean(a)),
                "mannwhitney_u": float(test.statistic),
                "p_raw": float(test.pvalue),
                "cliffs_delta_v2_vs_v1": cliffs_delta(b, a),
            }
        )
    assoc = pd.DataFrame(assoc_rows)
    assoc["p_holm"] = holm_adjust(assoc["p_raw"].tolist())
    assoc.to_csv(OUT / "table_condition_associations.csv", index=False)

    # --- Shared-model paired comparison by prompt ----------------------------
    # For each shared model, pair the same prompt across conditions.
    pair_rows = []
    for model in SHARED_MODELS:
        left = v1[v1["model"] == model].set_index("prompt_id")
        right = v2[v2["model"] == model].set_index("prompt_id")
        common = left.index.intersection(right.index)
        for metric in ["HuMT", "OA", "E", "D", "F"]:
            diff = right.loc[common, metric] - left.loc[common, metric]
            test = stats.wilcoxon(
                right.loc[common, metric],
                left.loc[common, metric],
            )
            pair_rows.append(
                {
                    "model": model,
                    "metric": metric,
                    "n_prompts": int(len(common)),
                    "mean_v1": float(left.loc[common, metric].mean()),
                    "mean_v2": float(right.loc[common, metric].mean()),
                    "mean_difference_v2_minus_v1": float(diff.mean()),
                    "median_difference_v2_minus_v1": float(diff.median()),
                    "wilcoxon_statistic": float(test.statistic),
                    "p_raw": float(test.pvalue),
                }
            )
    paired = pd.DataFrame(pair_rows)
    paired["p_holm_within_model"] = paired.groupby("model")["p_raw"].transform(
        lambda s: holm_adjust(s.tolist())
    )
    paired.to_csv(OUT / "table_condition_paired_shared_models.csv", index=False)

    # Aggregate shared-model prompt means (average across shared models) for a
    # single prompt-level condition contrast.
    prompt_rows = []
    for metric in ["HuMT", "OA", "E", "D", "F"]:
        v1_prompt = (
            v1[v1["model"].isin(SHARED_MODELS)]
            .groupby("prompt_id")[metric]
            .mean()
        )
        v2_prompt = (
            v2[v2["model"].isin(SHARED_MODELS)]
            .groupby("prompt_id")[metric]
            .mean()
        )
        common = v1_prompt.index.intersection(v2_prompt.index)
        diff = v2_prompt.loc[common] - v1_prompt.loc[common]
        test = stats.wilcoxon(v2_prompt.loc[common], v1_prompt.loc[common])
        prompt_rows.append(
            {
                "scope": "shared_models_prompt_mean",
                "metric": metric,
                "n_prompts": int(len(common)),
                "mean_v1": float(v1_prompt.loc[common].mean()),
                "mean_v2": float(v2_prompt.loc[common].mean()),
                "mean_difference_v2_minus_v1": float(diff.mean()),
                "wilcoxon_statistic": float(test.statistic),
                "p_raw": float(test.pvalue),
            }
        )
    prompt_cmp = pd.DataFrame(prompt_rows)
    prompt_cmp["p_holm"] = holm_adjust(prompt_cmp["p_raw"].tolist())
    prompt_cmp.to_csv(OUT / "table_condition_prompt_level.csv", index=False)

    # --- Figures -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    # Mean bars
    metrics = ["OA", "E", "D", "F"]
    x = np.arange(len(metrics))
    m1 = [v1[m].mean() for m in metrics]
    m2 = [v2[m].mean() for m in metrics]
    axes[0].bar(x - 0.18, m1, width=0.36, label="v1 original", color="#4C78A8")
    axes[0].bar(x + 0.18, m2, width=0.36, label="v2 relaxed", color="#E45756")
    axes[0].set_xticks(x, metrics)
    axes[0].set_ylim(1, 5)
    axes[0].set_ylabel("Mean five-rater score")
    axes[0].set_title("Corpus means")
    axes[0].legend(frameon=False)

    # D consensus distribution
    wide = (
        d_dist.pivot(index="D_median", columns="condition", values="n_responses")
        .fillna(0)
        .sort_index()
    )
    xpos = np.arange(len(wide.index))
    axes[1].bar(xpos - 0.18, wide.get("v1", 0), width=0.36, color="#4C78A8", label="v1")
    axes[1].bar(xpos + 0.18, wide.get("v2", 0), width=0.36, color="#E45756", label="v2")
    axes[1].set_xticks(xpos, [str(int(i)) for i in wide.index])
    axes[1].set_xlabel("Consensus median D")
    axes[1].set_ylabel("Responses")
    axes[1].set_title("Deception distribution")
    axes[1].legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "fig_condition_compare.png", dpi=240, bbox_inches="tight")
    plt.close(fig)

    # --- Summary markdown ----------------------------------------------------
    d_row = prompt_cmp[prompt_cmp["metric"] == "D"].iloc[0]
    oa_row = prompt_cmp[prompt_cmp["metric"] == "OA"].iloc[0]
    lines = [
        "# v1 vs v2 condition comparison",
        "",
        "v1 = original anti-anthropomorphism system prompt.",
        "v2 = relaxed professional-therapist system prompt.",
        "",
        "Prompts are shared (220). Model sets differ (v1 has gemini; v2 has gpt_5_6_sol).",
        "Primary confirmatory contrast uses shared models only: claude_opus_4_8 and glm.",
        "",
        "## Corpus means (all responses)",
        "",
    ]
    for metric in metrics:
        a = descriptives[
            (descriptives["condition"] == "v1") & (descriptives["metric"] == metric)
        ].iloc[0]
        b = descriptives[
            (descriptives["condition"] == "v2") & (descriptives["metric"] == metric)
        ].iloc[0]
        lines.append(
            f"- {metric}: v1={a['mean']:.3f}, v2={b['mean']:.3f} "
            f"(Δ={b['mean']-a['mean']:+.3f})"
        )
    lines.extend(
        [
            "",
            "## Shared-model prompt-level contrast",
            "",
            f"- D: v2−v1 = {d_row['mean_difference_v2_minus_v1']:+.3f} "
            f"(Wilcoxon p_holm={d_row['p_holm']:.3g})",
            f"- OA: v2−v1 = {oa_row['mean_difference_v2_minus_v1']:+.3f} "
            f"(Wilcoxon p_holm={oa_row['p_holm']:.3g})",
            "",
            "## Consensus median D counts",
            "",
            d_dist.to_string(index=False),
            "",
            "## Interpretation",
            "",
            "- The relaxed prompt increases deception-risk exposure relative to v1.",
            "- Use shared-model paired tests for condition claims; full-corpus tests mix different third models.",
        ]
    )
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Condition comparison complete: {OUT}")
    return OUT


if __name__ == "__main__":
    run_comparison()
