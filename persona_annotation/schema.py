"""PERSONA annotation JSON schema and helpers.

Scores are intentionally left as ``null`` / empty strings so downstream
human or automated annotators can fill them later without re-scaffolding.
"""

from __future__ import annotations

from typing import Any, Optional, TypedDict


class PersonaDimension(TypedDict):
    """Single PERSONA dimension: Likert score + free-text rationale."""

    score: Optional[float]
    reason: str


class PersonaScores(TypedDict):
    """Core PERSONA dimensions (E / D / F / OA)."""

    Empathy: PersonaDimension
    DeceptionRisk: PersonaDimension
    ContextualFit: PersonaDimension
    OverallAppropriateness: PersonaDimension


class AnnotationRecord(TypedDict):
    """One annotation object for a single (prompt, model, response) triple."""

    prompt_id: str
    model: str
    response: str
    humt_score: Optional[float]
    persona: PersonaScores


def empty_dimension() -> PersonaDimension:
    """Return an unscored PERSONA dimension scaffold."""

    return {"score": None, "reason": ""}


def empty_persona() -> PersonaScores:
    """Return an unscored PERSONA block for E / D / F / OA."""

    return {
        "Empathy": empty_dimension(),
        "DeceptionRisk": empty_dimension(),
        "ContextualFit": empty_dimension(),
        "OverallAppropriateness": empty_dimension(),
    }


def build_annotation(
    *,
    prompt_id: str,
    model: str,
    response: str,
    humt_score: Optional[float],
) -> AnnotationRecord:
    """Build a complete annotation object with blank PERSONA scores.

    Parameters
    ----------
    prompt_id:
        Stable identifier for the source prompt (typically ``questionID``).
    model:
        Canonical model name (e.g. ``glm``, ``gemini``, ``claude_opus_4_8``).
    response:
        Model response text.
    humt_score:
        Existing HuMT human-likeness score, or ``None`` if unavailable.
    """

    return {
        "prompt_id": prompt_id,
        "model": model,
        "response": response,
        "humt_score": humt_score,
        "persona": empty_persona(),
    }


def annotation_to_dict(record: AnnotationRecord) -> dict[str, Any]:
    """Serialize an annotation record to a plain JSON-compatible dict."""

    return {
        "prompt_id": record["prompt_id"],
        "model": record["model"],
        "response": record["response"],
        "humt_score": record["humt_score"],
        "persona": {
            "Empathy": dict(record["persona"]["Empathy"]),
            "DeceptionRisk": dict(record["persona"]["DeceptionRisk"]),
            "ContextualFit": dict(record["persona"]["ContextualFit"]),
            "OverallAppropriateness": dict(
                record["persona"]["OverallAppropriateness"]
            ),
        },
    }
