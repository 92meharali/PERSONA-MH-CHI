"""CLI entry: python -m analysis."""

from __future__ import annotations

from .run import main


def cli() -> None:
    main("v2")


if __name__ == "__main__":
    cli()
