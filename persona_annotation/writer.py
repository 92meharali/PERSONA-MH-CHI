"""JSON writers with no-overwrite and resume support."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .schema import AnnotationRecord, annotation_to_dict

logger = logging.getLogger("persona_annotation.writer")


@dataclass
class ManifestEntry:
    """Provenance record linking an output file to its source row."""

    index: int
    filename: str
    prompt_id: str
    model: str
    source_id: str
    source_set: str
    topic: str
    failure_mode: Optional[str]
    humt_score: Optional[float]
    response_file: str
    humt_file: str
    row_index: int
    written_at: str
    skipped: bool = False


class AnnotationWriter:
    """Write annotation JSON files without modifying upstream datasets."""

    def __init__(
        self,
        output_dir: Path,
        *,
        filename_prefix: str = "prompt",
        filename_pad: int = 3,
        resume: bool = True,
        overwrite: bool = False,
        manifest_path: Optional[Path] = None,
    ) -> None:
        self.output_dir = output_dir
        self.filename_prefix = filename_prefix
        self.filename_pad = filename_pad
        self.resume = resume
        self.overwrite = overwrite
        self.manifest_path = manifest_path or (output_dir / "manifest.json")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_entries: list[ManifestEntry] = []
        self.written = 0
        self.skipped = 0

    def filename_for_index(self, index: int) -> str:
        """Return ``prompt001.json``-style name for a 1-based index."""

        return f"{self.filename_prefix}{index:0{self.filename_pad}d}.json"

    def path_for_index(self, index: int) -> Path:
        return self.output_dir / self.filename_for_index(index)

    def should_skip(self, path: Path) -> bool:
        """True when the target exists and resume/no-overwrite applies."""

        if not path.exists():
            return False
        if self.overwrite:
            return False
        return True

    def write_one(
        self,
        index: int,
        record: AnnotationRecord,
        *,
        source_id: str,
        source_set: str,
        topic: str,
        failure_mode: Optional[str],
        response_file: str,
        humt_file: str,
        row_index: int,
    ) -> ManifestEntry:
        """Write a single annotation JSON, respecting resume/overwrite policy.

        Returns a manifest entry describing what happened.
        """

        path = self.path_for_index(index)
        now = datetime.now(timezone.utc).isoformat()

        if self.should_skip(path):
            self.skipped += 1
            logger.debug("Skipping existing file: %s", path.name)
            entry = ManifestEntry(
                index=index,
                filename=path.name,
                prompt_id=record["prompt_id"],
                model=record["model"],
                source_id=source_id,
                source_set=source_set,
                topic=topic,
                failure_mode=failure_mode,
                humt_score=record["humt_score"],
                response_file=response_file,
                humt_file=humt_file,
                row_index=row_index,
                written_at=now,
                skipped=True,
            )
            self.manifest_entries.append(entry)
            return entry

        payload = annotation_to_dict(record)
        # Atomic-ish write: write temp then replace only when overwrite allowed
        # or file does not exist. Double-check existence to avoid races.
        if path.exists() and not self.overwrite:
            self.skipped += 1
            entry = ManifestEntry(
                index=index,
                filename=path.name,
                prompt_id=record["prompt_id"],
                model=record["model"],
                source_id=source_id,
                source_set=source_set,
                topic=topic,
                failure_mode=failure_mode,
                humt_score=record["humt_score"],
                response_file=response_file,
                humt_file=humt_file,
                row_index=row_index,
                written_at=now,
                skipped=True,
            )
            self.manifest_entries.append(entry)
            return entry

        tmp_path = path.with_suffix(".json.tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        tmp_path.replace(path)

        self.written += 1
        entry = ManifestEntry(
            index=index,
            filename=path.name,
            prompt_id=record["prompt_id"],
            model=record["model"],
            source_id=source_id,
            source_set=source_set,
            topic=topic,
            failure_mode=failure_mode,
            humt_score=record["humt_score"],
            response_file=response_file,
            humt_file=humt_file,
            row_index=row_index,
            written_at=now,
            skipped=False,
        )
        self.manifest_entries.append(entry)
        return entry

    def flush_manifest(self, extra: Optional[dict[str, Any]] = None) -> None:
        """Persist the in-memory manifest to disk (safe to call after each batch)."""

        existing: dict[str, Any] = {}
        if self.manifest_path.exists():
            try:
                with self.manifest_path.open("r", encoding="utf-8") as handle:
                    existing = json.load(handle)
            except json.JSONDecodeError:
                logger.warning(
                    "Existing manifest was unreadable; rewriting from this run."
                )

        # Merge by filename so resumed runs keep prior entries for skipped files.
        by_name: dict[str, dict[str, Any]] = {}
        for prior in existing.get("entries", []):
            by_name[prior["filename"]] = prior
        for entry in self.manifest_entries:
            by_name[entry.filename] = asdict(entry)

        payload = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "output_dir": str(self.output_dir),
            "counts": {
                "entries": len(by_name),
                "written_this_run": self.written,
                "skipped_this_run": self.skipped,
            },
            "entries": [
                by_name[name]
                for name in sorted(
                    by_name.keys(),
                    key=lambda n: int(
                        "".join(ch for ch in n if ch.isdigit()) or "0"
                    ),
                )
            ],
        }
        if extra:
            payload["run"] = extra

        tmp = self.manifest_path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        tmp.replace(self.manifest_path)
        logger.debug("Manifest updated: %s", self.manifest_path)
