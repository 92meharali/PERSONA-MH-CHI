"""Domain-level PERSONA analysis for cleaned education and health folders."""

from __future__ import annotations

import csv
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parent.parent / "data" / "clean_domains"
SCORES = ["OA_score", "E_score", "D_score", "F_score"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def num(value: str) -> float:
    try:
        return float(value) if value != "" else math.nan
    except Exception:
        return math.nan


def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u2019", "'").replace("\u2018", "'")).strip().lower()


def cronbach_alpha(matrix: list[list[float]]) -> float:
    arr = np.array(matrix, dtype=float)
    arr = arr[~np.isnan(arr).any(axis=1)]
    if arr.shape[0] < 2 or arr.shape[1] < 2:
        return math.nan
    k = arr.shape[1]
    item_vars = arr.var(axis=0, ddof=1)
    total_var = arr.sum(axis=1).var(ddof=1)
    return math.nan if math.isclose(total_var, 0.0) else (k / (k - 1)) * (1 - item_vars.sum() / total_var)


def group_cv_r2(x: np.ndarray, y: np.ndarray, groups: np.ndarray, folds: int = 5) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    groups = np.asarray(groups)
    mask = ~np.isnan(y) & ~np.isnan(x).any(axis=1)
    x, y, groups = x[mask], y[mask], groups[mask]
    unique = np.array(sorted(set(groups)))
    folds = max(2, min(folds, len(unique)))
    preds = np.full_like(y, np.nan, dtype=float)
    for split in np.array_split(unique, folds):
        test = np.isin(groups, split)
        train = ~test
        beta = np.linalg.lstsq(np.column_stack([np.ones(train.sum()), x[train]]), y[train], rcond=None)[0]
        preds[test] = np.column_stack([np.ones(test.sum()), x[test]]) @ beta
    ss_res = np.sum((y - preds) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return float(1 - ss_res / ss_tot)


def analyze_domain(domain: str) -> str:
    folder = ROOT / domain
    annotator_files = sorted(
        f for f in folder.glob("*.csv") if not f.name.startswith("humt_")
    )
    humt_file = next((f for f in folder.glob("humt_*.csv")), None)
    humt_rows = read_rows(humt_file) if humt_file else []
    humt_map = {norm_text(r.get("text", "")): num(r.get("humt_text", "")) for r in humt_rows}

    item_rows = defaultdict(dict)
    for path in annotator_files:
        rows = read_rows(path)
        annotator = path.stem
        for row in rows:
            key = row.get("annotation_item_id", "") or f"{row.get('prompt','')}|{row.get('response','')}"
            item_rows[key].setdefault("ratings", {})[annotator] = {s: num(row.get(s, "")) for s in SCORES}
            item_rows[key]["prompt"] = row.get("prompt", "")
            item_rows[key]["response"] = row.get("response", "")
            item_rows[key]["annotator_id"] = row.get("annotator_id", row.get("annotator", annotator))
            item_rows[key]["prompt_id"] = row.get("prompt_id", row.get("annotation_item_id", ""))
            item_rows[key]["model"] = row.get("model", "")
            item_rows[key]["scenario_type"] = row.get("scenario_type", "")
            item_rows[key]["humt"] = humt_map.get(norm_text(row.get("response", "")), math.nan)

    consensus = []
    for key, item in item_rows.items():
        row = {
            "item": key,
            "prompt_id": item.get("prompt_id", ""),
            "model": item.get("model", ""),
            "humt": item.get("humt", math.nan),
        }
        for score in SCORES:
            vals = [r[score] for r in item["ratings"].values() if not math.isnan(r[score])]
            row[score] = float(np.mean(vals)) if vals else math.nan
        consensus.append(row)

    def spear(a: str, b: str) -> float:
        vals = [(r[a], r[b]) for r in consensus if not math.isnan(r[a]) and not math.isnan(r[b])]
        return float(stats.spearmanr([x for x, _ in vals], [y for _, y in vals]).statistic) if len(vals) > 2 else math.nan

    alpha = {}
    for score in SCORES:
        matrix = []
        for item in item_rows.values():
            ratings = item.get("ratings", {})
            if len(ratings) == len(annotator_files):
                matrix.append([ratings[a][score] for a in sorted(ratings)])
        alpha[score] = cronbach_alpha(matrix)

    lines = []
    lines.append(f"# {domain.title()} Analysis")
    lines.append("")
    if domain == "health":
        lines.append("This domain is treated as oversight/adjudication evidence rather than independently verified human annotation.")
        lines.append("")
    lines.append("## Data Quality")
    lines.append("")
    lines.append(f"- Responses: {len(item_rows)}")
    lines.append(f"- Rating rows: {sum(len(read_rows(f)) for f in annotator_files)}")
    lines.append(f"- HuMT matches: {sum(not math.isnan(r['humt']) for r in consensus)}")
    if domain != "mental_health":
        lines.append("- HuMT joins are by normalized response text in this quick runner; a stable response ID join would be preferable in a final pass.")
    lines.append("")
    lines.append("## Reliability")
    lines.append("")
    for s in SCORES:
        lines.append(f"- {s}: {alpha[s]:.3f}")
    lines.append("")
    lines.append("## Correlations")
    lines.append("")
    lines.append(f"- HuMT/OA: {spear('humt', 'OA_score'):.3f}")
    lines.append(f"- E/OA: {spear('E_score', 'OA_score'):.3f}")
    lines.append(f"- D/OA: {spear('D_score', 'OA_score'):.3f}")
    lines.append(f"- F/OA: {spear('F_score', 'OA_score'):.3f}")
    lines.append("")

    usable = [r for r in consensus if not any(math.isnan(r[s]) for s in ["OA_score", "E_score", "D_score", "F_score", "humt"])]
    if usable:
        x_h = np.array([[r["humt"]] for r in usable])
        x_edf = np.array([[r["humt"], r["E_score"], r["D_score"], r["F_score"]] for r in usable])
        y = np.array([r["OA_score"] for r in usable])
        groups = np.array([r["prompt_id"] for r in usable])
        lines.append("## Predictive Check")
        lines.append("")
        lines.append(f"- HuMT only CV R2: {group_cv_r2(x_h, y, groups):.3f}")
        lines.append(f"- HuMT+E/D/F CV R2: {group_cv_r2(x_edf, y, groups):.3f}")
        lines.append("")

    out = folder / "analysis.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return str(out)


def main() -> None:
    for domain in ["education", "health"]:
        print(analyze_domain(domain))


if __name__ == "__main__":
    main()
