"""PERSONA annotation scaffolding pipeline.

Builds blank annotation JSON objects from existing model responses and
HuMT human-likeness scores. Does **not** assign PERSONA scores and does
**not** modify existing repository data.
"""

from __future__ import annotations

from .pipeline import PipelineResult, run_pipeline
from .schema import AnnotationRecord, build_annotation

__all__ = [
    "AnnotationRecord",
    "PipelineResult",
    "build_annotation",
    "run_pipeline",
]

__version__ = "0.1.0"
