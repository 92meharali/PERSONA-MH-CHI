"""Configuration loading for the PERSONA annotation pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

logger = logging.getLogger(__name__)

# Default location: package-local config.yaml
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


@dataclass(frozen=True)
class SourceConfig:
    """One response CSV paired with its HuMT results CSV."""

    id: str
    set: str
    model: str
    response_file: Path
    humt_file: Path


@dataclass(frozen=True)
class ProcessingConfig:
    """Runtime processing behaviour."""

    batch_size: int = 50
    filename_pad: int = 3
    filename_prefix: str = "prompt"
    resume: bool = True
    overwrite: bool = False


@dataclass(frozen=True)
class LoggingConfig:
    """Logging options."""

    level: str = "INFO"
    log_to_file: bool = True


@dataclass(frozen=True)
class PipelineConfig:
    """Fully resolved pipeline configuration."""

    repo_root: Path
    output_dir: Path
    manifest_path: Path
    log_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig
    sources: tuple[SourceConfig, ...] = field(default_factory=tuple)


def _as_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = (repo_root / path).resolve()
    return path


def load_config(config_path: Optional[Path | str] = None) -> PipelineConfig:
    """Load and resolve ``config.yaml``.

    Parameters
    ----------
    config_path:
        Optional path to a YAML config. Defaults to the package ``config.yaml``.
    """

    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        raw: dict[str, Any] = yaml.safe_load(handle) or {}

    paths = raw.get("paths", {})
    processing_raw = raw.get("processing", {})
    logging_raw = raw.get("logging", {})
    sources_raw = raw.get("sources", [])

    repo_root = Path(paths.get("repo_root", ".")).resolve()
    # Allow config authors to use "." relative to the git repo, not CWD.
    # If repo_root is ".", resolve against the parent of the config's package
    # (repository root = parent of persona_annotation/).
    if paths.get("repo_root", ".") in (".", "./"):
        repo_root = path.parent.parent.resolve()

    output_dir = _as_path(repo_root, paths.get("output_dir", "annotations"))
    manifest_filename = paths.get("manifest_filename", "manifest.json")
    log_filename = paths.get("log_filename", "persona_annotation.log")

    processing = ProcessingConfig(
        batch_size=int(processing_raw.get("batch_size", 50)),
        filename_pad=int(processing_raw.get("filename_pad", 3)),
        filename_prefix=str(processing_raw.get("filename_prefix", "prompt")),
        resume=bool(processing_raw.get("resume", True)),
        overwrite=bool(processing_raw.get("overwrite", False)),
    )
    logging_cfg = LoggingConfig(
        level=str(logging_raw.get("level", "INFO")).upper(),
        log_to_file=bool(logging_raw.get("log_to_file", True)),
    )

    sources: list[SourceConfig] = []
    for item in sources_raw:
        sources.append(
            SourceConfig(
                id=str(item["id"]),
                set=str(item["set"]),
                model=str(item["model"]),
                response_file=_as_path(repo_root, item["response_file"]),
                humt_file=_as_path(repo_root, item["humt_file"]),
            )
        )

    if not sources:
        raise ValueError("Config must define at least one entry under 'sources'.")

    if processing.batch_size < 1:
        raise ValueError("processing.batch_size must be >= 1")

    if processing.overwrite:
        logger.warning(
            "overwrite=true is set; existing annotation JSON may be replaced. "
            "Prefer overwrite=false for research reproducibility."
        )

    return PipelineConfig(
        repo_root=repo_root,
        output_dir=output_dir,
        manifest_path=output_dir / manifest_filename,
        log_path=output_dir / log_filename,
        processing=processing,
        logging=logging_cfg,
        sources=tuple(sources),
    )
