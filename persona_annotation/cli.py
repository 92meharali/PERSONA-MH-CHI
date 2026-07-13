"""Command-line entry point for the PERSONA annotation pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import load_config
from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="persona_annotation",
        description=(
            "PERSONA annotation tools: scaffold blank JSON and/or apply the "
            "rubric scorer. Never modifies upstream response/HuMT CSVs."
        ),
    )
    sub = parser.add_subparsers(dest="command")

    scaffold = sub.add_parser(
        "scaffold",
        help="Build blank annotation JSON from responses + HuMT scores.",
    )
    scaffold.add_argument("--config", type=Path, default=None)
    scaffold.add_argument("--batch-size", type=int, default=None)
    scaffold.add_argument("--output-dir", type=Path, default=None)
    scaffold.add_argument("--no-resume", action="store_true")
    scaffold.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing existing scaffold JSON (not recommended).",
    )

    score = sub.add_parser(
        "score",
        help="Fill E/D/F/OA rubric scores into a new output directory.",
    )
    score.add_argument("--config", type=Path, default=None)
    score.add_argument("--input-dir", type=Path, default=None)
    score.add_argument("--output-dir", type=Path, default=None)
    score.add_argument("--batch-size", type=int, default=50)
    score.add_argument("--limit", type=int, default=None)
    score.add_argument("--no-resume", action="store_true")

    # Default command = scaffold for backward compatibility when no subcommand.
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def _run_scaffold(args: argparse.Namespace) -> int:
    from dataclasses import replace

    from .pipeline import run_pipeline

    cfg = load_config(args.config)
    processing = cfg.processing
    if args.batch_size is not None:
        processing = replace(processing, batch_size=args.batch_size)
    if args.no_resume:
        processing = replace(processing, resume=False)
    if getattr(args, "overwrite", False):
        processing = replace(processing, overwrite=True)

    output_dir = cfg.output_dir
    manifest_path = cfg.manifest_path
    log_path = cfg.log_path
    if args.output_dir is not None:
        output_dir = args.output_dir.resolve()
        manifest_path = output_dir / cfg.manifest_path.name
        log_path = output_dir / cfg.log_path.name

    cfg = replace(
        cfg,
        processing=processing,
        output_dir=output_dir,
        manifest_path=manifest_path,
        log_path=log_path,
    )
    result = run_pipeline(cfg)
    print(
        f"PERSONA scaffolds ready: {result.written} written, "
        f"{result.skipped} skipped, {result.total_records} total → {result.output_dir}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "score":
        from .score_pipeline import main as score_main

        score_argv: list[str] = []
        if args.config:
            score_argv.extend(["--config", str(args.config)])
        if args.input_dir:
            score_argv.extend(["--input-dir", str(args.input_dir)])
        if args.output_dir:
            score_argv.extend(["--output-dir", str(args.output_dir)])
        if args.batch_size:
            score_argv.extend(["--batch-size", str(args.batch_size)])
        if args.limit is not None:
            score_argv.extend(["--limit", str(args.limit)])
        if args.no_resume:
            score_argv.append("--no-resume")
        return score_main(score_argv)

    # scaffold (explicit or default)
    return _run_scaffold(args)


if __name__ == "__main__":
    sys.exit(main())
