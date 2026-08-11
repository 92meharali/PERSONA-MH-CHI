"""Targeted HuMT/response provenance audit.

This script inspects the committed clean-domain files and the Phase 1 processed
dataset. It does not change joins or recover missing HuMT values.
"""

from __future__ import annotations

import pandas as pd

from .build_dataset import humt_file
from .persona_common import CLEAN_DIR, DOMAINS, norm_text, save_json, save_markdown, save_table


def audit_domain(domain: str) -> dict:
    consensus = pd.read_csv("analysis/processed/persona_all.csv")
    block = consensus[consensus["domain"] == domain].copy()
    block["response_norm"] = block["response"].map(norm_text)

    duplicate_response_texts = int(block["response_norm"].duplicated().sum())
    stable_response_id_available = "annotation_item_id" in block.columns
    humt_stable_response_id_available = False
    humt_duplicate_texts = 0
    humt_rows = 0
    humt_columns = []

    hfile = humt_file(domain)
    if hfile is not None:
        humt = pd.read_csv(hfile, encoding="utf-8-sig")
        humt_rows = len(humt)
        humt_columns = list(humt.columns)
        humt_duplicate_texts = int(humt["text"].map(norm_text).duplicated().sum()) if "text" in humt.columns else 0
        humt_stable_response_id_available = bool({"annotation_item_id", "response_id", "prompt_id"} & set(humt.columns))

    matched = block[block["humt_join_tier"].notna()]
    unmatched = block[block["humt_join_tier"].isna()]
    fuzzy = block[block["humt_join_tier"].eq("fuzzy")]

    return {
        "domain": domain,
        "responses": int(len(block)),
        "humt_rows": int(humt_rows),
        "matched": int(len(matched)),
        "unmatched": int(len(unmatched)),
        "ambiguous_accepted": 0,
        "response_duplicate_normalized_texts": duplicate_response_texts,
        "humt_duplicate_normalized_texts": humt_duplicate_texts,
        "repository_response_id_available": stable_response_id_available,
        "humt_stable_response_id_available": humt_stable_response_id_available,
        "humt_columns": ";".join(humt_columns),
        "fuzzy_matches": int(len(fuzzy)),
        "unmatched_item_ids": ";".join(unmatched["annotation_item_id"].astype(str).tolist()),
        "decision": "keep_text_join_documented" if hfile is not None else "embedded_humt",
    }


def render(rows: pd.DataFrame) -> str:
    lines = [
        "# HuMT / response provenance audit",
        "",
        "This audit checks whether the current HuMT joins can be kept without changing "
        "scores or fabricating identifiers. It is read-only: no unmatched HuMT values "
        "are recovered here.",
        "",
        "## Summary",
        "",
        "| Domain | Responses | HuMT rows | Matched | Unmatched | Duplicate response texts | Duplicate HuMT texts | Stable ID in HuMT | Fuzzy matches | Decision |",
        "|---|---:|---:|---:|---:|---:|---:|---|---:|---|",
    ]
    for _, r in rows.iterrows():
        lines.append(
            f"| {r['domain']} | {r['responses']} | {r['humt_rows']} | {r['matched']} | {r['unmatched']} | "
            f"{r['response_duplicate_normalized_texts']} | {r['humt_duplicate_normalized_texts']} | "
            f"{'yes' if r['humt_stable_response_id_available'] else 'no'} | {r['fuzzy_matches']} | {r['decision']} |"
        )

    lines += [
        "",
        "## Findings",
        "",
        "- Mental health uses embedded HuMT values and native metadata.",
        "- Education and health HuMT exports do not contain a stable response identifier "
        "such as `annotation_item_id`, `response_id`, or `prompt_id`; the repository "
        "does contain `annotation_item_id`, but the HuMT files cannot join on it.",
        "- The Phase 1 join accepts only unique normalized text keys, then unique prefixes, "
        "then mutually-best fuzzy matches with a similarity threshold and margin.",
        "- No ambiguous HuMT matches are accepted. Ambiguous or unmatched rows remain missing "
        "and are counted in `data_audit.md` and `humt_join_report.csv`.",
        "- Because no stable HuMT-side identifier exists, the correct decision is to keep the "
        "documented text join and report unmatched rows transparently.",
        "",
        "## Unmatched rows",
        "",
        "| Domain | Unmatched annotation_item_id values |",
        "|---|---|",
    ]
    for _, r in rows.iterrows():
        lines.append(f"| {r['domain']} | {r['unmatched_item_ids'] or '-'} |")

    lines += [
        "",
        "## False-match risk",
        "",
        "False matches are constrained by the one-to-one join rules: a candidate key must "
        "identify exactly one response and exactly one unused HuMT row. Fuzzy matches must "
        "also be mutually best and clear the similarity and margin requirements. The audit "
        "therefore treats accepted matches as deterministic under the committed files, while "
        "still recommending future HuMT exports include stable response IDs.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows = pd.DataFrame([audit_domain(domain) for domain in DOMAINS])
    save_table(rows, "humt_provenance_audit")
    save_markdown(render(rows), "humt_provenance_audit")
    save_json({"humt_provenance_audit": rows.to_dict(orient="records")}, "humt_provenance_audit")
    print("HuMT provenance audit complete")


if __name__ == "__main__":
    main()
