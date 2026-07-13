"""Export scored PERSONA annotation JSON to structured per-model CSVs.

Reads ``annotations_scored/prompt*.json`` (+ optional manifest metadata) and
writes one CSV per model under a dedicated output directory. Does not modify
JSON scaffolds, scored JSON, or upstream response/HuMT CSVs.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from tqdm import tqdm

from .config import load_config
from .logging_utils import setup_logging
from .rubric import PERSONA_DIMENSIONS

logger = logging.getLogger("persona_annotation.export_csv")

EVIDENCE_SEP = " | "


def _load_manifest(manifest_path: Path) -> dict[str, dict[str, Any]]:
    if not manifest_path.exists():
        logger.warning("Manifest not found at %s; metadata columns may be empty.", manifest_path)
        return {}
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return {entry["filename"]: entry for entry in payload.get("entries", [])}


def _join_evidence(evidence: Any) -> str:
    if not evidence:
        return ""
    if isinstance(evidence, list):
        return EVIDENCE_SEP.join(str(item) for item in evidence if item)
    return str(evidence)


def annotation_to_row(
    payload: dict[str, Any],
    *,
    filename: str,
    meta: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Flatten one annotation JSON object into a CSV row dict."""

    meta = meta or {}
    persona = payload.get("persona") or {}
    row: dict[str, Any] = {
        "filename": filename,
        "index": meta.get("index"),
        "prompt_id": payload.get("prompt_id", meta.get("prompt_id", "")),
        "model": payload.get("model", meta.get("model", "")),
        "source_id": meta.get("source_id", ""),
        "source_set": meta.get("source_set", ""),
        "topic": meta.get("topic", ""),
        "failure_mode": meta.get("failure_mode"),
        "response": payload.get("response", ""),
        "humt_score": payload.get("humt_score"),
    }

    for dim in PERSONA_DIMENSIONS:
        block = persona.get(dim) or {}
        row[f"{dim}_score"] = block.get("score")
        row[f"{dim}_reason"] = block.get("reason", "")
        row[f"{dim}_evidence"] = _join_evidence(block.get("evidence"))

    return row


def collect_rows(
    input_dir: Path,
    manifest_path: Path,
) -> list[dict[str, Any]]:
    """Load all scored annotation JSON files into flat row dicts."""

    files = sorted(input_dir.glob("prompt*.json"))
    if not files:
        raise FileNotFoundError(f"No prompt*.json files found in {input_dir}")

    meta_index = _load_manifest(manifest_path)
    rows: list[dict[str, Any]] = []
    for path in tqdm(files, desc="Flatten annotations", unit="file"):
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        rows.append(
            annotation_to_row(
                payload,
                filename=path.name,
                meta=meta_index.get(path.name),
            )
        )
    logger.info("Loaded %d annotation rows from %s", len(rows), input_dir)
    return rows


def export_per_model_csv(
    rows: list[dict[str, Any]],
    output_dir: Path,
    *,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Write one structured CSV per model. Refuses to overwrite by default."""

    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    if "model" not in df.columns:
        raise ValueError("Flattened rows are missing required column 'model'.")

    # Stable column order.
    base_cols = [
        "filename",
        "index",
        "prompt_id",
        "model",
        "source_id",
        "source_set",
        "topic",
        "failure_mode",
        "response",
        "humt_score",
    ]
    persona_cols: list[str] = []
    for dim in PERSONA_DIMENSIONS:
        persona_cols.extend([f"{dim}_score", f"{dim}_reason", f"{dim}_evidence"])
    ordered = [c for c in base_cols + persona_cols if c in df.columns]
    df = df[ordered]

    written: dict[str, Path] = {}
    for model_name, group in df.groupby("model", sort=True):
        safe_name = str(model_name).strip().replace("/", "_").replace(" ", "_")
        out_path = output_dir / f"{safe_name}_persona_annotations.csv"
        if out_path.exists() and not overwrite:
            logger.info("Skipping existing CSV (no overwrite): %s", out_path)
            written[str(model_name)] = out_path
            continue
        group = group.sort_values(["source_set", "index", "prompt_id"], kind="stable")
        group.to_csv(out_path, index=False, encoding="utf-8-sig")
        logger.info("Wrote %d rows → %s", len(group), out_path)
        written[str(model_name)] = out_path

    # Optional combined export for convenience (also no-overwrite).
    combined_path = output_dir / "all_models_persona_annotations.csv"
    if combined_path.exists() and not overwrite:
        logger.info("Skipping existing combined CSV (no overwrite): %s", combined_path)
    else:
        df.sort_values(["model", "source_set", "index", "prompt_id"], kind="stable").to_csv(
            combined_path, index=False, encoding="utf-8-sig"
        )
        logger.info("Wrote %d rows → %s", len(df), combined_path)
    written["__all__"] = combined_path
    return written


def run_export(
    *,
    input_dir: Path,
    output_dir: Path,
    manifest_path: Optional[Path] = None,
    overwrite: bool = False,
) -> dict[str, Any]:
    """End-to-end JSON → per-model CSV export."""

    manifest = manifest_path or (input_dir / "manifest.json")
    rows = collect_rows(input_dir, manifest)
    paths = export_per_model_csv(rows, output_dir, overwrite=overwrite)
    summary = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "rows": len(rows),
        "models": sorted({r["model"] for r in rows}),
        "files": {k: str(v) for k, v in paths.items()},
    }
    logger.info("CSV export complete: %s", summary)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="persona_annotation.export_csv",
        description="Convert scored PERSONA JSON annotations into per-model CSVs.",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help="Scored JSON directory (default: annotations_scored/).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="CSV output directory (default: annotations_csv/).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing CSV files in the output directory.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)
    setup_logging(cfg.logging, None)

    input_dir = (args.input_dir or (cfg.repo_root / "annotations_scored")).resolve()
    output_dir = (args.output_dir or (cfg.repo_root / "annotations_csv")).resolve()

    summary = run_export(
        input_dir=input_dir,
        output_dir=output_dir,
        overwrite=bool(args.overwrite),
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
