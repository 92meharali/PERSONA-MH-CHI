"""CLI for PERSONA analysis pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import load_config
from .pipeline import run_all


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="analysis",
        description="Run the reproducible PERSONA statistical analysis pipeline.",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--part",
        action="append",
        default=None,
        help="Optional subset of parts to enable (repeatable). Default: all configured parts.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)
    if args.part:
        # Disable all then enable requested
        parts = {k: False for k in cfg.parts}
        for p in args.part:
            if p not in parts:
                raise SystemExit(f"Unknown part '{p}'. Choices: {sorted(parts)}")
            parts[p] = True
        # keep figures/tables/report if explicitly requested only
        from dataclasses import replace

        cfg = replace(cfg, parts=parts)

    summary = run_all(cfg)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
