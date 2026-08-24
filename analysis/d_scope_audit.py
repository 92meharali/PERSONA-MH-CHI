"""Post-analysis audit of the linguistic mechanism behind high health D scores.

The cue-family labels are a transparent qualitative inspection layer, not a
replacement for the original ratings. They are fixed here so the sensitivity
numbers reported in the manuscript can be regenerated and reviewed.
"""

from __future__ import annotations

import pandas as pd
from scipy import stats

from .persona_common import load_consensus, save_markdown, save_table
from .predictive import repeated_grouped_cv


CUE_FAMILY = {
    "PHLT-0064": "affective_or_relational",
    "PHLT-0065": "affective_or_relational",
    "PHLT-0068": "affective_or_relational",
    "PHLT-0069": "affective_or_relational",
    "PHLT-0070": "affective_or_relational",
    "PHLT-0071": "affective_or_relational",
    "PHLT-0072": "affective_or_relational",
    "PHLT-0074": "affective_or_relational",
    "PHLT-0076": "affective_or_relational",
    "PHLT-0077": "affective_or_relational",
    "PHLT-0080": "affective_or_relational",
    "PHLT-0083": "affective_or_relational",
    "PHLT-0101": "clinician_identity_and_continuity",
    "PHLT-0133": "affective_or_relational",
    "PHLT-0139": "affective_or_relational",
    "PHLT-0140": "affective_or_relational",
    "PHLT-0141": "affective_or_relational",
    "PHLT-0146": "affective_or_relational",
    "PHLT-0147": "affective_or_relational",
    "PHLT-0149": "affective_or_relational",
    "PHLT-0252": "affective_or_relational",
    "PHLT-0289": "affective_or_relational",
    "PHLT-0433": "affective_or_relational",
}


def performance(label: str, frame: pd.DataFrame) -> dict:
    _, _, repeats, _ = repeated_grouped_cv(frame.reset_index(drop=True), ["D"])
    return {
        "analysis_set": label,
        "n": len(frame),
        "prompt_clusters": frame["prompt_id"].nunique(),
        "pearson_D_OA": stats.pearsonr(frame["D"], frame["OA"]).statistic,
        "spearman_D_OA": stats.spearmanr(frame["D"], frame["OA"]).statistic,
        "D_only_cv_r2": repeats["r2"].mean(),
        "D_only_cv_r2_sd": repeats["r2"].std(ddof=1),
    }


def main() -> None:
    data = load_consensus()
    health = data[data["domain"] == "health"].copy()
    high = health[health["D"] >= 3].copy()

    observed = set(high["annotation_item_id"])
    expected = set(CUE_FAMILY)
    if observed != expected:
        raise ValueError(
            f"High-D coding is stale; missing={sorted(observed - expected)}, "
            f"extra={sorted(expected - observed)}"
        )

    high["dominant_cue_family"] = high["annotation_item_id"].map(CUE_FAMILY)
    audit = high[[
        "annotation_item_id", "prompt_id", "scenario_type", "D", "OA", "F",
        "dominant_cue_family",
    ]].sort_values(["dominant_cue_family", "D"], ascending=[True, False])

    authority_id = "PHLT-0101"
    authority_prompt = health.loc[
        health["annotation_item_id"] == authority_id, "prompt_id"
    ].iloc[0]
    sensitivity = pd.DataFrame([
        performance("all_health", health),
        performance(
            "minus_clinician_identity_response",
            health[health["annotation_item_id"] != authority_id],
        ),
        performance(
            "minus_clinician_identity_prompt_cluster",
            health[health["prompt_id"] != authority_prompt],
        ),
        performance(
            "minus_other_scenarios",
            health[health["scenario_type"] != "other"],
        ),
    ])

    save_table(audit, "d_scope_response_audit")
    save_table(sensitivity, "d_scope_sensitivity")
    save_markdown(render(audit, sensitivity), "d_scope_audit")
    print("D scope audit complete: cue-family trace and sensitivity checks")


def render(audit: pd.DataFrame, sensitivity: pd.DataFrame) -> str:
    counts = audit["dominant_cue_family"].value_counts()
    lines = [
        "# D scope audit",
        "",
        "This is a post-analysis qualitative inspection of health responses with consensus `D >= 3`.",
        "It does not alter the original human ratings or create a new D subtype measure.",
        "",
        "## Cue-family counts",
        "",
        f"- Affective or relational: {int(counts.get('affective_or_relational', 0))}",
        f"- Clinician identity and continuity: {int(counts.get('clinician_identity_and_continuity', 0))}",
        "",
        "## Sensitivity",
        "",
        "| Analysis set | N | Clusters | Pearson | Spearman | D-only CV R2 | SD |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sensitivity.itertuples():
        lines.append(
            f"| {row.analysis_set} | {row.n} | {row.prompt_clusters} | "
            f"{row.pearson_D_OA:.3f} | {row.spearman_D_OA:.3f} | "
            f"{row.D_only_cv_r2:.3f} | {row.D_only_cv_r2_sd:.3f} |"
        )
    lines += [
        "",
        "The professional-role sensitivity removes the sole high-D response whose dominant mechanism was "
        "an enacted clinician identity and false continuity. The `other` sensitivity shows that the "
        "health D-only result is concentrated in the relational adversarial subset.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
