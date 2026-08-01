"""CLI entry: python -m analysis [--corpus v1|v2|both] [--compare]."""

from __future__ import annotations

import argparse

from .compare_conditions import run_comparison
from .run import main


def cli() -> None:
    parser = argparse.ArgumentParser(description="PERSONA-MH focused analysis")
    parser.add_argument(
        "--corpus",
        choices=["v1", "v2", "both"],
        default="v1",
        help="Which annotation corpus to analyze (default: v1)",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Also write v1 vs v2 condition comparison outputs",
    )
    args = parser.parse_args()
    if args.corpus in {"v1", "both"}:
        main("v1")
    if args.corpus in {"v2", "both"}:
        main("v2")
    if args.compare or args.corpus == "both":
        run_comparison()


if __name__ == "__main__":
    cli()
