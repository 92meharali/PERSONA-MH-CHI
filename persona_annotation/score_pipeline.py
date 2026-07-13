"""Apply PERSONA rubric scores to scaffolded annotation JSON files.

Reads blank scaffolds from ``annotations/`` (or a configured input dir),
scores each response with the response-grounded protocol, and writes
filled JSON to a **separate** output directory so existing scaffolds are
never modified.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional

from tqdm import tqdm

from .config import load_config
from .logging_utils import setup_logging
from .schema import AnnotationRecord, build_annotation
from .scorer import ScoreContext, annotate_response, protocol_id
from .writer import AnnotationWriter

logger = logging.getLogger("persona_annotation.score_pipeline")


def _load_manifest_index(manifest_path: Path) -> dict[str, dict[str, Any]]:
    if not manifest_path.exists():
        return {}
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return {entry["filename"]: entry for entry in payload.get("entries", [])}


def _load_scaffold(path: Path) -> AnnotationRecord:
    """Load a scaffold JSON; PERSONA block is ignored (re-scored)."""

    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return build_annotation(
        prompt_id=str(raw.get("prompt_id", "")),
        model=str(raw.get("model", "")),
        response=str(raw.get("response", "")),
        humt_score=(
            None
            if raw.get("humt_score") is None
            else float(raw["humt_score"])
        ),
    )


def run_scoring(
    *,
    input_dir: Path,
    output_dir: Path,
    manifest_path: Path,
    batch_size: int = 50,
    resume: bool = True,
    overwrite: bool = False,
    limit: Optional[int] = None,
) -> dict[str, Any]:
    """Score scaffold JSON files into ``output_dir`` without touching inputs."""

    if overwrite:
        raise ValueError(
            "Refusing overwrite=True for scored outputs; "
            "write to a new directory or delete targets manually."
        )

    scaffolds = sorted(input_dir.glob("prompt*.json"))
    if limit is not None:
        scaffolds = scaffolds[:limit]
    if not scaffolds:
        raise FileNotFoundError(f"No prompt*.json scaffolds found in {input_dir}")

    meta = _load_manifest_index(manifest_path)
    writer = AnnotationWriter(
        output_dir,
        filename_prefix="prompt",
        filename_pad=3,
        resume=resume,
        overwrite=False,
        manifest_path=output_dir / "manifest.json",
    )

    logger.info("Protocol: %s", protocol_id())
    logger.info("Input scaffolds: %s (%d files)", input_dir, len(scaffolds))
    logger.info("Scored output dir: %s", output_dir)

    batches = [
        scaffolds[i : i + batch_size] for i in range(0, len(scaffolds), batch_size)
    ]
    progress = tqdm(total=len(scaffolds), desc="PERSONA scoring", unit="resp")

    try:
        for batch_num, batch in enumerate(batches, start=1):
            logger.info("Batch %d / %d", batch_num, len(batches))
            for path in batch:
                scaffold = _load_scaffold(path)
                # Derive 1-based index from filename promptNNN.json
                digits = "".join(ch for ch in path.stem if ch.isdigit())
                index = int(digits) if digits else progress.n + 1

                entry_meta = meta.get(path.name, {})
                ctx = ScoreContext(
                    topic=str(entry_meta.get("topic") or ""),
                    failure_mode=entry_meta.get("failure_mode"),
                    source_set=str(entry_meta.get("source_set") or ""),
                    prompt="",  # evidence remains response-only
                )
                persona = annotate_response(scaffold["response"], ctx)
                scored = build_annotation(
                    prompt_id=scaffold["prompt_id"],
                    model=scaffold["model"],
                    response=scaffold["response"],
                    humt_score=scaffold["humt_score"],
                    persona=persona,
                )

                # Defense: verify all evidence quotes are substrings.
                for dim_name, dim in persona.items():
                    for quote in dim["evidence"]:
                        if quote not in scored["response"]:
                            raise AssertionError(
                                f"Evidence not in response ({path.name} / {dim_name}): {quote!r}"
                            )

                writer.write_one(
                    index,
                    scored,
                    source_id=str(entry_meta.get("source_id") or ""),
                    source_set=str(entry_meta.get("source_set") or ""),
                    topic=str(entry_meta.get("topic") or ""),
                    failure_mode=entry_meta.get("failure_mode"),
                    response_file=str(entry_meta.get("response_file") or path),
                    humt_file=str(entry_meta.get("humt_file") or ""),
                    row_index=int(entry_meta.get("row_index") or 0),
                )
                progress.update(1)

            writer.flush_manifest(
                extra={
                    "protocol": protocol_id(),
                    "batch": batch_num,
                    "input_dir": str(input_dir),
                }
            )
    finally:
        progress.close()

    writer.flush_manifest(
        extra={
            "protocol": protocol_id(),
            "status": "completed",
            "input_dir": str(input_dir),
            "written": writer.written,
            "skipped": writer.skipped,
            "total": len(scaffolds),
        }
    )
    summary = {
        "protocol": protocol_id(),
        "total": len(scaffolds),
        "written": writer.written,
        "skipped": writer.skipped,
        "output_dir": str(output_dir),
    }
    logger.info("Scoring done: %s", summary)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="persona_annotation.score",
        description=(
            "Fill PERSONA rubric scores (E/D/F/OA) for scaffolded annotation "
            "JSON without modifying existing scaffolds."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Base config YAML (used for logging / repo paths).",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help="Directory of blank scaffolds (default: annotations/).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for scored JSON (default: annotations_scored/).",
    )
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional cap for dry runs.",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Do not treat resume specially (existing outputs still skipped).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)
    setup_logging(cfg.logging, None)

    input_dir = (args.input_dir or (cfg.repo_root / "annotations")).resolve()
    output_dir = (args.output_dir or (cfg.repo_root / "annotations_scored")).resolve()
    manifest_path = input_dir / "manifest.json"

    summary = run_scoring(
        input_dir=input_dir,
        output_dir=output_dir,
        manifest_path=manifest_path,
        batch_size=args.batch_size,
        resume=not args.no_resume,
        overwrite=False,
        limit=args.limit,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
