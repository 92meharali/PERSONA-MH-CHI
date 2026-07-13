"""Pipeline orchestration: load → scaffold → batch write."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from tqdm import tqdm

from .config import PipelineConfig, load_config
from .loaders import ResponseRow, load_all_sources
from .logging_utils import setup_logging
from .schema import build_annotation
from .writer import AnnotationWriter

logger = logging.getLogger("persona_annotation.pipeline")


@dataclass(frozen=True)
class PipelineResult:
    """Summary of a pipeline run."""

    total_records: int
    written: int
    skipped: int
    output_dir: str
    manifest_path: str


def _batched(items: list[ResponseRow], batch_size: int) -> list[list[ResponseRow]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def run_pipeline(config: Optional[PipelineConfig] = None) -> PipelineResult:
    """Build blank PERSONA annotation JSON for every response.

    Flow
    ----
    Prompt → Model Response → HuMT Score → PERSONA scaffold → JSON

    PERSONA scores are left as ``null``; HuMT scores are reused from
    ``humt_results/``. Existing files under ``persona_mh_outputs/``,
    ``humt_results/``, and ``counselbench_outputs/`` are never modified.
    """

    cfg = config or load_config()
    setup_logging(cfg.logging, cfg.log_path if cfg.logging.log_to_file else None)

    logger.info("Repository root: %s", cfg.repo_root)
    logger.info("Output directory: %s", cfg.output_dir)
    logger.info("Sources: %d", len(cfg.sources))
    logger.info(
        "Processing: batch_size=%d resume=%s overwrite=%s",
        cfg.processing.batch_size,
        cfg.processing.resume,
        cfg.processing.overwrite,
    )

    if cfg.processing.overwrite:
        logger.warning("Overwrite enabled — existing annotation JSON will be replaced.")
    elif not cfg.processing.resume:
        logger.info(
            "Resume disabled and overwrite=false: existing files will still be "
            "skipped to protect prior outputs."
        )

    rows = load_all_sources(cfg.sources)
    writer = AnnotationWriter(
        cfg.output_dir,
        filename_prefix=cfg.processing.filename_prefix,
        filename_pad=cfg.processing.filename_pad,
        resume=cfg.processing.resume,
        overwrite=cfg.processing.overwrite,
        manifest_path=cfg.manifest_path,
    )

    batches = _batched(rows, cfg.processing.batch_size)
    global_index = 0

    progress = tqdm(total=len(rows), desc="PERSONA scaffolds", unit="resp")
    try:
        for batch_num, batch in enumerate(batches, start=1):
            logger.info(
                "Batch %d / %d (%d records)",
                batch_num,
                len(batches),
                len(batch),
            )
            for row in batch:
                global_index += 1
                record = build_annotation(
                    prompt_id=row.prompt_id,
                    model=row.model,
                    response=row.response,
                    humt_score=row.humt_score,
                )
                writer.write_one(
                    global_index,
                    record,
                    source_id=row.source_id,
                    source_set=row.source_set,
                    topic=row.topic,
                    failure_mode=row.failure_mode,
                    response_file=row.response_file,
                    humt_file=row.humt_file,
                    row_index=row.row_index,
                )
                progress.update(1)

            writer.flush_manifest(
                extra={
                    "batch": batch_num,
                    "batches_total": len(batches),
                    "records_seen": global_index,
                }
            )
    finally:
        progress.close()

    # Final manifest flush with complete summary.
    writer.flush_manifest(
        extra={
            "status": "completed",
            "total_records": len(rows),
            "written": writer.written,
            "skipped": writer.skipped,
        }
    )

    result = PipelineResult(
        total_records=len(rows),
        written=writer.written,
        skipped=writer.skipped,
        output_dir=str(cfg.output_dir),
        manifest_path=str(cfg.manifest_path),
    )
    logger.info(
        "Done. total=%d written=%d skipped=%d → %s",
        result.total_records,
        result.written,
        result.skipped,
        result.output_dir,
    )
    return result
