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
            "Build blank PERSONA annotation JSON scaffolds from existing "
            "model responses and HuMT scores. Does not modify source data."
        ),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config YAML (default: persona_annotation/config.yaml).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Override processing.batch_size from config.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override paths.output_dir from config.",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Disable resume flag in config (existing files still skipped unless --overwrite).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacing existing annotation JSON (not recommended).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)

    # Apply CLI overrides via object reconstruction (frozen dataclasses).
    from dataclasses import replace

    processing = cfg.processing
    if args.batch_size is not None:
        processing = replace(processing, batch_size=args.batch_size)
    if args.no_resume:
        processing = replace(processing, resume=False)
    if args.overwrite:
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


if __name__ == "__main__":
    sys.exit(main())
