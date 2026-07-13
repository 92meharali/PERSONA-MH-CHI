"""PERSONA annotation pipeline.

1. Scaffold blank annotation JSON from responses + HuMT scores.
2. Score Empathy / DeceptionRisk / ContextualFit / OverallAppropriateness
   with the research rubric (response-grounded evidence quotes).

Upstream prompt, response, and HuMT CSVs are never modified.
"""

from __future__ import annotations

from .pipeline import PipelineResult, run_pipeline
from .schema import AnnotationRecord, build_annotation
from .scorer import annotate_response
from .score_pipeline import run_scoring

__all__ = [
    "AnnotationRecord",
    "PipelineResult",
    "annotate_response",
    "build_annotation",
    "run_pipeline",
    "run_scoring",
]

__version__ = "0.2.0"
