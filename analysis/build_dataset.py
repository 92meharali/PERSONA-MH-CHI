"""Phase 1 - build one canonical multi-domain PERSONA dataset and audit it.

Reads the five annotator CSVs in each ``data/clean_domains/<domain>/`` folder and
produces:

  analysis/processed/persona_ratings_long.csv   one row per (domain, item, rater)
  analysis/processed/persona_all.csv            one row per response (consensus)
  analysis/outputs/tables/data_audit.csv        machine-readable audit
  analysis/outputs/tables/humt_join_report.csv  per-tier join provenance
  analysis/outputs/reports/data_audit.md        human-readable audit

Two structural gaps in the committed education/health files are repaired here,
both deterministically and both recorded in the audit:

1. ``prompt_id`` does not exist in those files. Prompt text partitions cleanly
   into groups of three responses, so a stable prompt id is reconstructed from
   the normalised prompt text. Without this, grouped cross-validation silently
   degrades to ungrouped cross-validation and sibling responses leak across folds.

2. ``model`` does not exist in those files. It is recovered from the
   ``source_file`` column of the domain HuMT export via a cascading text join,
   then completed by elimination inside prompt groups that are already
   partially identified.

Nothing is dropped. Rows that cannot be matched are carried with explicit
missing values and counted.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd

from .persona_common import (
    CLEAN_DIR,
    CONSENSUS,
    DIMENSIONS,
    DOMAINS,
    MODEL_FAMILY,
    PROCESSED_DIR,
    RATINGS_LONG,
    RATING_MAX,
    RATING_MIN,
    env_versions,
    norm_text,
    save_json,
    save_markdown,
    save_table,
)

ID_PREFIX = {"mental_health": "MH", "education": "EDU", "health": "HLT"}
# Cascading join tiers: full normalised text first, then shrinking prefixes.
JOIN_TIERS = [("full", None), ("prefix_300", 300), ("prefix_200", 200), ("prefix_120", 120), ("prefix_80", 80)]
FUZZY_WINDOW = 400   # characters compared in the final near-duplicate tier
FUZZY_MIN = 0.95     # minimum similarity to accept a fuzzy match
FUZZY_MARGIN = 0.05  # required gap over the runner-up candidate


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------
def annotator_files(domain: str) -> list[Path]:
    folder = CLEAN_DIR / domain
    return sorted(f for f in folder.glob("*.csv") if not f.name.startswith("humt_"))


def humt_file(domain: str) -> Path | None:
    folder = CLEAN_DIR / domain
    return next(iter(sorted(folder.glob("humt_*.csv"))), None)


def load_domain_ratings(domain: str) -> pd.DataFrame:
    frames = []
    for path in annotator_files(domain):
        frame = pd.read_csv(path, encoding="utf-8-sig")
        frame["source_file"] = path.name
        if "annotator_id" not in frame.columns:
            frame["annotator_id"] = path.stem
        frames.append(frame)
    combined = pd.concat(frames, ignore_index=True)
    combined["domain"] = domain
    return combined


# --------------------------------------------------------------------------
# HuMT join
# --------------------------------------------------------------------------
def parse_humt_source(source: str) -> tuple[str, str]:
    """Turn e.g. 'adv_glm_5_2_text_humt (1).csv' into ('glm_5_2', 'adversarial')."""
    stem = re.sub(r"\.csv$", "", str(source))
    stem = re.sub(r"\s*\(\d+\)$", "", stem)
    stem = re.sub(r"-\d+$", "", stem)
    stem = re.sub(r"_text_humt.*$", "", stem)
    condition = "adversarial" if stem.startswith("adv_") else "natural"
    model = re.sub(r"^adv_", "", stem)
    return model, condition


def join_humt(responses: pd.Series, humt: pd.DataFrame) -> pd.DataFrame:
    """Cascading, ambiguity-aware 1:1 join of responses onto HuMT rows.

    At each tier only unmatched responses and unused HuMT rows are considered,
    and a candidate key is accepted only when it identifies exactly one response
    and exactly one HuMT row. Everything else is left unmatched and reported.
    """
    resp_norm = responses.map(norm_text)
    humt_norm = humt["text"].map(norm_text)

    result = pd.DataFrame(
        {
            "humt": np.nan,
            "humt_std": np.nan,
            "humt_source_file": pd.Series([None] * len(responses), dtype=object),
            "humt_join_tier": pd.Series([None] * len(responses), dtype=object),
        },
        index=responses.index,
    )
    ambiguous = 0
    used_humt: set[int] = set()

    for tier_name, width in JOIN_TIERS:
        open_rows = result.index[result["humt_join_tier"].isna()]
        if len(open_rows) == 0:
            break
        free_humt = [i for i in humt.index if i not in used_humt]
        if not free_humt:
            break

        def key(series, idx):
            values = series.loc[idx]
            return values if width is None else values.str[:width]

        resp_keys = key(resp_norm, open_rows)
        humt_keys = key(humt_norm, pd.Index(free_humt))

        resp_counts = resp_keys.value_counts()
        humt_counts = humt_keys.value_counts()
        humt_lookup = {k: i for i, k in humt_keys.items() if humt_counts[k] == 1}

        for row_idx, k in resp_keys.items():
            if k not in humt_lookup:
                continue
            if resp_counts[k] != 1:
                ambiguous += 1
                continue
            h_idx = humt_lookup[k]
            model, condition = parse_humt_source(humt.loc[h_idx, "source_file"])
            result.loc[row_idx, "humt"] = humt.loc[h_idx, "humt_text"]
            result.loc[row_idx, "humt_std"] = humt.loc[h_idx].get("std_humt_text", np.nan)
            result.loc[row_idx, "humt_source_file"] = humt.loc[h_idx, "source_file"]
            result.loc[row_idx, "humt_join_tier"] = tier_name
            result.loc[row_idx, "model_raw"] = model
            result.loc[row_idx, "condition"] = condition
            used_humt.add(h_idx)

    # Final conservative tier: mutually-best near-duplicate match. Only accepted
    # when similarity clears FUZZY_MIN and beats the runner-up by FUZZY_MARGIN,
    # so it cannot quietly attach the wrong HuMT score to a response.
    open_rows = list(result.index[result["humt_join_tier"].isna()])
    free_humt = [i for i in humt.index if i not in used_humt]
    if open_rows and free_humt:
        scores = np.zeros((len(open_rows), len(free_humt)))
        resp_snip = {r: resp_norm.loc[r][:FUZZY_WINDOW] for r in open_rows}
        humt_snip = {h: humt_norm.loc[h][:FUZZY_WINDOW] for h in free_humt}
        for i, r in enumerate(open_rows):
            for j, h in enumerate(free_humt):
                scores[i, j] = SequenceMatcher(None, resp_snip[r], humt_snip[h]).ratio()
        for i, r in enumerate(open_rows):
            order = np.argsort(scores[i])[::-1]
            best, second = order[0], (order[1] if len(order) > 1 else None)
            best_score = scores[i, best]
            runner_up = scores[i, second] if second is not None else 0.0
            if best_score < FUZZY_MIN or best_score - runner_up < FUZZY_MARGIN:
                continue
            if np.argmax(scores[:, best]) != i:  # must be mutually best
                ambiguous += 1
                continue
            h_idx = free_humt[best]
            if h_idx in used_humt:
                continue
            model, condition = parse_humt_source(humt.loc[h_idx, "source_file"])
            result.loc[r, "humt"] = humt.loc[h_idx, "humt_text"]
            result.loc[r, "humt_std"] = humt.loc[h_idx].get("std_humt_text", np.nan)
            result.loc[r, "humt_source_file"] = humt.loc[h_idx, "source_file"]
            result.loc[r, "humt_join_tier"] = "fuzzy"
            result.loc[r, "model_raw"] = model
            result.loc[r, "condition"] = condition
            used_humt.add(h_idx)

    result.attrs["ambiguous"] = ambiguous
    result.attrs["humt_rows"] = len(humt)
    result.attrs["humt_used"] = len(used_humt)
    return result


# --------------------------------------------------------------------------
# Per-domain assembly
# --------------------------------------------------------------------------
def build_domain(domain: str, audit: list[dict], join_rows: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    ratings = load_domain_ratings(domain)
    prefix = ID_PREFIX[domain]

    # ---- one row per response, carrying the shared metadata -------------
    items = (
        ratings.sort_values("annotation_item_id")
        .groupby("annotation_item_id", as_index=False)
        .agg(prompt=("prompt", "first"), response=("response", "first"),
             scenario_type=("scenario_type", "first"))
    )
    items["domain"] = domain

    # ---- prompt_id ------------------------------------------------------
    if "prompt_id" in ratings.columns:
        native = ratings.groupby("annotation_item_id")["prompt_id"].first()
        items["prompt_id"] = items["annotation_item_id"].map(native)
        items["prompt_id_source"] = "native_column"
    else:
        items["_pnorm"] = items["prompt"].map(norm_text)
        ordered = sorted(items["_pnorm"].unique())
        lookup = {p: f"{prefix}-P{i + 1:03d}" for i, p in enumerate(ordered)}
        items["prompt_id"] = items["_pnorm"].map(lookup)
        items["prompt_id_source"] = "reconstructed_from_prompt_text"
        items = items.drop(columns=["_pnorm"])

    # ---- HuMT + model ---------------------------------------------------
    hfile = humt_file(domain)
    if hfile is not None:
        humt = pd.read_csv(hfile, encoding="utf-8-sig")
        joined = join_humt(items["response"], humt)
        for column in ("humt", "humt_std", "humt_source_file", "humt_join_tier", "model_raw", "condition"):
            items[column] = joined.get(column, pd.Series(index=items.index, dtype=object))
        items["model_source"] = np.where(items["model_raw"].notna(), "humt_source_file", None)
        tier_counts = joined["humt_join_tier"].value_counts(dropna=True).to_dict()
        ambiguous = joined.attrs.get("ambiguous", 0)
    else:
        # Mental health carries HuMT and model natively.
        embedded = ratings.groupby("annotation_item_id").first()
        items["humt"] = items["annotation_item_id"].map(embedded["humt_score"])
        items["humt_std"] = items["annotation_item_id"].map(embedded.get("humt_std"))
        items["humt_source_file"] = "embedded_in_annotator_files"
        items["humt_join_tier"] = "embedded"
        items["model_raw"] = items["annotation_item_id"].map(embedded["model"])
        items["model_source"] = "native_column"
        items["condition"] = items["annotation_item_id"].map(
            embedded["prompt_type"].map(
                {"adversarial_expert_authored": "adversarial", "normal_real_patient": "natural"}
            )
        )
        tier_counts = {"embedded": int(items["humt"].notna().sum())}
        ambiguous = 0

    # ---- complete model / condition by elimination inside prompt groups --
    items["model"] = items["model_raw"].map(MODEL_FAMILY)
    domain_families = set(items["model"].dropna().unique())
    recovered = 0
    for _, block in items.groupby("prompt_id"):
        known = block["model"].dropna()
        missing = block.index[block["model"].isna()]
        # Each prompt has exactly one response per model, so a group with a
        # single hole and distinct known families determines the missing one.
        if len(missing) == 1 and len(known) == len(block) - 1 and known.nunique() == len(known):
            candidates = domain_families - set(known)
            if len(candidates) == 1:
                items.loc[missing[0], "model"] = candidates.pop()
                items.loc[missing[0], "model_source"] = "elimination_within_prompt_group"
                recovered += 1
        # condition is a property of the prompt, so it propagates within a group
        cond = block["condition"].dropna()
        if len(cond) and items.loc[block.index, "condition"].isna().any():
            if cond.nunique() == 1:
                items.loc[block.index, "condition"] = cond.iloc[0]

    join_rows.append(
        {
            "domain": domain,
            "responses": len(items),
            "humt_rows_available": 0 if hfile is None else len(pd.read_csv(hfile, encoding="utf-8-sig")),
            **{f"matched_{name}": int(tier_counts.get(name, 0)) for name, _ in JOIN_TIERS},
            "matched_fuzzy": int(tier_counts.get("fuzzy", 0)),
            "matched_embedded": int(tier_counts.get("embedded", 0)),
            "matched_total": int(items["humt"].notna().sum()),
            "unmatched": int(items["humt"].isna().sum()),
            "ambiguous_keys_rejected": int(ambiguous),
            "model_recovered_by_elimination": int(recovered),
            "model_unknown": int(items["model"].isna().sum()),
        }
    )

    # ---- consensus ------------------------------------------------------
    stats = ratings.groupby("annotation_item_id")[[f"{d}_score" for d in DIMENSIONS]].agg(
        ["mean", "median", "std", "count"]
    )
    stats.columns = [f"{c[0].replace('_score', '')}_{c[1]}" for c in stats.columns]
    stats = stats.rename(columns={f"{d}_mean": d for d in DIMENSIONS})
    consensus = items.merge(stats, left_on="annotation_item_id", right_index=True, how="left")
    consensus["n_raters"] = ratings.groupby("annotation_item_id").size().reindex(consensus["annotation_item_id"]).to_numpy()
    consensus["H"] = consensus["humt"]

    # ---- audit rows -----------------------------------------------------
    def add(check: str, value, detail: str = "") -> None:
        audit.append({"domain": domain, "check": check, "value": value, "detail": detail})

    add("responses", len(items))
    add("rating_rows", len(ratings))
    add("annotators", ratings["annotator_id"].nunique())
    add("duplicate_response_ids", int(items["annotation_item_id"].duplicated().sum()))
    add("missing_response_ids", int(items["annotation_item_id"].isna().sum()))
    add("duplicate_annotations", int(ratings.duplicated(["annotation_item_id", "annotator_id"]).sum()))
    counts = ratings.groupby("annotation_item_id").size()
    add("raters_per_response_min", int(counts.min()))
    add("raters_per_response_max", int(counts.max()))
    add("responses_with_incomplete_raters", int((counts != counts.max()).sum()))
    for dim in DIMENSIONS:
        column = ratings[f"{dim}_score"]
        add(f"missing_{dim}", int(column.isna().sum()))
        invalid = (~column.isna()) & (~column.isin(range(RATING_MIN, RATING_MAX + 1)))
        add(f"invalid_{dim}", int(invalid.sum()), f"outside integer {RATING_MIN}-{RATING_MAX}")
    add("missing_humt", int(consensus["humt"].isna().sum()))
    add("humt_match_rate", round(float(consensus["humt"].notna().mean()), 4))
    add("prompt_id_source", items["prompt_id_source"].iloc[0])
    add("prompt_groups", int(items["prompt_id"].nunique()))
    group_sizes = items.groupby("prompt_id").size()
    add("responses_per_prompt_min", int(group_sizes.min()))
    add("responses_per_prompt_max", int(group_sizes.max()))
    add("prompt_groups_not_size_3", int((group_sizes != 3).sum()))
    add("distinct_models", int(items["model"].nunique(dropna=True)))
    add("model_unknown", int(items["model"].isna().sum()))
    for model, n in items["model"].value_counts(dropna=True).items():
        add(f"responses_model_{model}", int(n))
    for cond, n in items["condition"].value_counts(dropna=True).items():
        add(f"responses_condition_{cond}", int(n))
    add("distinct_conditions", int(items["condition"].nunique(dropna=True)))
    add("scenario_types", int(items["scenario_type"].nunique(dropna=True)))
    add("duplicate_response_text", int(items["response"].map(norm_text).duplicated().sum()))

    # rater-independence provenance check: does the rationale text vary
    # independently of the score, or is it a deterministic function of it?
    for dim in DIMENSIONS:
        reason_col = f"{dim}_reason"
        if reason_col in ratings.columns:
            grouped = ratings.groupby("annotation_item_id")
            same_score = grouped[f"{dim}_score"].nunique().eq(1).mean()
            same_reason = grouped[reason_col].nunique().eq(1).mean()
            add(f"unanimous_score_rate_{dim}", round(float(same_score), 4))
            add(f"identical_rationale_rate_{dim}", round(float(same_reason), 4),
                "equal to the unanimity rate implies rationale is determined by score")

    keep_ratings = ["domain", "annotation_item_id", "annotator_id", "scenario_type"] + [
        f"{d}_score" for d in DIMENSIONS
    ]
    long = ratings[[c for c in keep_ratings if c in ratings.columns]].copy()
    long = long.merge(
        items[["annotation_item_id", "prompt_id", "model", "condition"]],
        on="annotation_item_id",
        how="left",
    )
    return consensus, long


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main() -> None:
    audit: list[dict] = []
    join_rows: list[dict] = []
    consensus_frames, long_frames = [], []

    for domain in DOMAINS:
        consensus, long = build_domain(domain, audit, join_rows)
        consensus_frames.append(consensus)
        long_frames.append(long)

    consensus = pd.concat(consensus_frames, ignore_index=True)
    long = pd.concat(long_frames, ignore_index=True)

    keep = [
        "domain", "annotation_item_id", "prompt_id", "prompt_id_source", "model",
        "model_raw", "model_source", "condition", "scenario_type", "n_raters",
        "H", "humt", "humt_std", "humt_join_tier", "humt_source_file",
        "OA", "OA_median", "OA_std", "E", "E_median", "E_std",
        "D", "D_median", "D_std", "F", "F_median", "F_std",
        "prompt", "response",
    ]
    consensus = consensus[[c for c in keep if c in consensus.columns]]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    consensus.to_csv(CONSENSUS, index=False)
    long.to_csv(RATINGS_LONG, index=False)

    audit.append({"domain": "ALL", "check": "responses", "value": len(consensus), "detail": ""})
    audit.append({"domain": "ALL", "check": "rating_rows", "value": len(long), "detail": ""})
    audit.append({"domain": "ALL", "check": "complete_cases_HEDF_OA",
                  "value": int(consensus[["H"] + DIMENSIONS].notna().all(axis=1).sum()), "detail": ""})
    audit.append({"domain": "ALL", "check": "domain_label_values",
                  "value": consensus["domain"].nunique(), "detail": ", ".join(sorted(consensus["domain"].unique()))})
    audit.append({"domain": "ALL", "check": "model_label_values",
                  "value": consensus["model"].nunique(dropna=True),
                  "detail": ", ".join(sorted(consensus["model"].dropna().unique()))})

    audit_frame = pd.DataFrame(audit)
    join_frame = pd.DataFrame(join_rows)
    save_table(audit_frame, "data_audit")
    save_table(join_frame, "humt_join_report")
    save_markdown(render_audit(audit_frame, join_frame, consensus), "data_audit")
    save_json({"environment": env_versions(),
               "audit": audit_frame.to_dict(orient="records"),
               "humt_join": join_frame.to_dict(orient="records")}, "phase1_results")

    print(f"Phase 1 complete: {len(consensus)} responses, {len(long)} rating rows -> {CONSENSUS}")


def render_audit(audit: pd.DataFrame, join: pd.DataFrame, consensus: pd.DataFrame) -> str:
    lines = ["# PERSONA data audit (Phase 1)", "",
             "Generated by `python -m analysis.build_dataset`. Nothing is dropped; "
             "unmatched and ambiguous records are carried with explicit missing values.", ""]

    lines += ["## Coverage", "", "| Domain | Responses | Rating rows | Raters | Prompt groups | HuMT matched | Model known |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for domain in DOMAINS:
        block = audit[audit["domain"] == domain].set_index("check")["value"]
        matched = int(join.loc[join["domain"] == domain, "matched_total"].iloc[0])
        lines.append(
            f"| {domain} | {block['responses']} | {block['rating_rows']} | {block['annotators']} | "
            f"{block['prompt_groups']} | {matched} | {int(block['responses']) - int(block['model_unknown'])} |"
        )

    lines += ["", "## HuMT join provenance", "",
              "The committed HuMT exports for education and health carry no response id, so the join is "
              "by text. A cascading, ambiguity-aware match is used and every tier is reported.", "",
              "| Domain | Available | full | pre300 | pre200 | pre120 | pre80 | fuzzy | embedded | Total | Unmatched | Ambiguous |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for _, row in join.iterrows():
        lines.append(
            f"| {row['domain']} | {row['humt_rows_available']} | {row['matched_full']} | {row['matched_prefix_300']} | "
            f"{row['matched_prefix_200']} | {row['matched_prefix_120']} | {row['matched_prefix_80']} | "
            f"{row['matched_fuzzy']} | {row['matched_embedded']} | {row['matched_total']} | "
            f"{row['unmatched']} | {row['ambiguous_keys_rejected']} |"
        )

    lines += ["", "## Structural repairs", "",
              "| Domain | prompt_id source | Models recovered by elimination | Model still unknown |",
              "|---|---|---:|---:|"]
    for domain in DOMAINS:
        block = audit[audit["domain"] == domain].set_index("check")
        jrow = join[join["domain"] == domain].iloc[0]
        lines.append(
            f"| {domain} | {block.loc['prompt_id_source', 'value']} | "
            f"{jrow['model_recovered_by_elimination']} | {jrow['model_unknown']} |"
        )

    lines += ["", "## Validity checks", "",
              "| Domain | Duplicate ids | Duplicate annotations | Invalid ratings | Missing ratings | Prompt groups != 3 |",
              "|---|---:|---:|---:|---:|---:|"]
    for domain in DOMAINS:
        block = audit[audit["domain"] == domain].set_index("check")["value"]
        invalid = sum(int(block[f"invalid_{d}"]) for d in DIMENSIONS)
        missing = sum(int(block[f"missing_{d}"]) for d in DIMENSIONS)
        lines.append(
            f"| {domain} | {block['duplicate_response_ids']} | {block['duplicate_annotations']} | "
            f"{invalid} | {missing} | {block['prompt_groups_not_size_3']} |"
        )

    lines += ["", "## Rating provenance flag", "",
              "For each dimension the table compares how often all raters gave the same score with how often "
              "all raters wrote the same rationale. When the two rates coincide, the rationale field is a "
              "deterministic function of the score and therefore cannot be treated as independent evidence "
              "that the ratings were produced independently.", "",
              "| Domain | Dimension | Unanimous score rate | Identical rationale rate |",
              "|---|---|---:|---:|"]
    for domain in DOMAINS:
        block = audit[audit["domain"] == domain].set_index("check")["value"]
        for dim in DIMENSIONS:
            key_s, key_r = f"unanimous_score_rate_{dim}", f"identical_rationale_rate_{dim}"
            if key_s in block.index and key_r in block.index:
                lines.append(f"| {domain} | {dim} | {block[key_s]} | {block[key_r]} |")

    lines += ["", "## Response counts by model and condition", "",
              "| Domain | Model | Condition | N |", "|---|---|---|---:|"]
    grouped = consensus.groupby(["domain", "model", "condition"], dropna=False).size()
    for (domain, model, condition), n in grouped.items():
        lines.append(f"| {domain} | {model if pd.notna(model) else 'UNKNOWN'} | "
                     f"{condition if pd.notna(condition) else 'UNKNOWN'} | {n} |")

    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
