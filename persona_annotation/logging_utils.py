"""Logging setup for the PERSONA annotation pipeline."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import LoggingConfig


def setup_logging(
    logging_cfg: LoggingConfig,
    log_path: Optional[Path] = None,
) -> logging.Logger:
    """Configure root/package logging for console (and optional file).

    Returns the ``persona_annotation`` package logger.
    """

    logger = logging.getLogger("persona_annotation")
    logger.handlers.clear()
    logger.setLevel(getattr(logging, logging_cfg.level, logging.INFO))
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if logging_cfg.log_to_file and log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
