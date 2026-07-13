"""PERSONA annotation pipeline.

1. Scaffold blank annotation JSON from responses + HuMT scores.
2. Score Empathy / DeceptionRisk / ContextualFit / OverallAppropriateness
   with the research rubric (response-grounded evidence quotes).
3. Export structured per-model CSVs.

Upstream prompt, response, and HuMT CSVs are never modified.
"""

from __future__ import annotations

from .export_csv import run_export
from .pipeline import PipelineResult, run_pipeline
from .schema import AnnotationRecord, build_annotation
from .score_pipeline import run_scoring
from .scorer import annotate_response

__all__ = [
    "AnnotationRecord",
    "PipelineResult",
    "annotate_response",
    "build_annotation",
    "run_export",
    "run_pipeline",
    "run_scoring",
]

__version__ = "0.3.0"
