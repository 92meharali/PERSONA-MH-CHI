"""CLI entry: python -m analysis [--corpus v2|v1|both] [--compare]."""

from __future__ import annotations

import argparse

from .compare_conditions import run_comparison
from .run import main


def cli() -> None:
    parser = argparse.ArgumentParser(description="PERSONA focused analysis")
    parser.add_argument(
        "--corpus",
        choices=["v2", "v1", "both"],
        default="v2",
        help="Which annotation corpus to analyze (default: v2 primary)",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Also write archived v1 vs v2 condition comparison outputs",
    )
    args = parser.parse_args()
    if args.corpus in {"v2", "both"}:
        main("v2")
    if args.corpus in {"v1", "both"}:
        main("v1")
    if args.compare or args.corpus == "both":
        run_comparison()


if __name__ == "__main__":
    cli()
