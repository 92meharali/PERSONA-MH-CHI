"""PERSONA annotation schema and helpers."""

from __future__ import annotations

from typing import Any, Optional, TypedDict


class PersonaDimension(TypedDict):
    """Single PERSONA dimension with score, rationale, and evidence quotes."""

    score: Optional[int]
    reason: str
    evidence: list[str]


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

    return {"score": None, "reason": "", "evidence": []}


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
    persona: Optional[PersonaScores] = None,
) -> AnnotationRecord:
    """Build an annotation object (blank or pre-filled PERSONA block)."""

    return {
        "prompt_id": prompt_id,
        "model": model,
        "response": response,
        "humt_score": humt_score,
        "persona": persona if persona is not None else empty_persona(),
    }


def dimension_to_dict(dim: PersonaDimension) -> dict[str, Any]:
    return {
        "score": dim["score"],
        "reason": dim["reason"],
        "evidence": list(dim["evidence"]),
    }


def annotation_to_dict(record: AnnotationRecord) -> dict[str, Any]:
    """Serialize an annotation record to a plain JSON-compatible dict."""

    return {
        "prompt_id": record["prompt_id"],
        "model": record["model"],
        "response": record["response"],
        "humt_score": record["humt_score"],
        "persona": {
            "Empathy": dimension_to_dict(record["persona"]["Empathy"]),
            "DeceptionRisk": dimension_to_dict(record["persona"]["DeceptionRisk"]),
            "ContextualFit": dimension_to_dict(record["persona"]["ContextualFit"]),
            "OverallAppropriateness": dimension_to_dict(
                record["persona"]["OverallAppropriateness"]
            ),
        },
    }


def validate_evidence_quotes(response: str, evidence: list[str]) -> list[str]:
    """Keep only evidence strings that are exact substrings of ``response``."""

    return [quote for quote in evidence if quote and quote in response]
