"""Read-only loaders for response CSVs and HuMT result CSVs."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd

from .config import SourceConfig

logger = logging.getLogger("persona_annotation.loaders")

# Encoding fallbacks for mixed UTF-8 / Windows-saved CSVs in this repo.
_ENCODINGS = ("utf-8-sig", "utf-8", "latin-1", "cp1252")


@dataclass(frozen=True)
class ResponseRow:
    """Normalized row bridging a model response and optional HuMT score."""

    source_id: str
    source_set: str
    model: str
    prompt_id: str
    question_id: str
    topic: str
    failure_mode: Optional[str]
    prompt: str
    response: str
    humt_score: Optional[float]
    response_file: str
    humt_file: str
    row_index: int


def read_csv(path: Path) -> pd.DataFrame:
    """Load a CSV trying common encodings used in this repository."""

    if not path.exists():
        raise FileNotFoundError(f"Required CSV not found: {path}")

    last_error: Optional[Exception] = None
    for encoding in _ENCODINGS:
        try:
            df = pd.read_csv(path, encoding=encoding)
            logger.debug("Loaded %s with encoding=%s (%d rows)", path, encoding, len(df))
            return df
        except Exception as exc:  # noqa: BLE001 — try next encoding
            last_error = exc
    raise RuntimeError(f"Failed to read {path}: {last_error}")


def _resolve_prompt_id(row: pd.Series) -> str:
    """Prefer ``questionID``; fall back to a synthetic id from the index."""

    if "questionID" in row.index and pd.notna(row["questionID"]):
        return str(row["questionID"]).strip()
    if "question_id" in row.index and pd.notna(row["question_id"]):
        return str(row["question_id"]).strip()
    return ""


def _join_humt(
    responses: pd.DataFrame,
    humt: pd.DataFrame,
    source: SourceConfig,
) -> list[Optional[float]]:
    """Attach HuMT scores to responses via exact ``response_text`` ↔ ``text`` join.

    Falls back to positional alignment when row counts match and some exact
    matches fail (defensive; current repo joins 100% by exact text).
    """

    if "response_text" not in responses.columns:
        raise KeyError(
            f"{source.response_file} is missing required column 'response_text'"
        )
    if "text" not in humt.columns or "humt_text" not in humt.columns:
        raise KeyError(
            f"{source.humt_file} must contain columns 'text' and 'humt_text'"
        )

    responses = responses.reset_index(drop=True)
    humt = humt.reset_index(drop=True)

    humt_lookup = (
        humt[["text", "humt_text"]]
        .dropna(subset=["text"])
        .drop_duplicates(subset=["text"], keep="first")
        .set_index("text")["humt_text"]
    )

    scores = responses["response_text"].map(humt_lookup)
    matched = int(scores.notna().sum())
    logger.info(
        "[%s] HuMT exact-text match: %d / %d",
        source.id,
        matched,
        len(responses),
    )

    unmatched_idx = scores[scores.isna()].index.tolist()
    if unmatched_idx and len(humt) == len(responses):
        for i in unmatched_idx:
            scores.iloc[i] = humt.loc[i, "humt_text"]
        logger.warning(
            "[%s] Applied positional HuMT fallback for %d rows",
            source.id,
            len(unmatched_idx),
        )

    result: list[Optional[float]] = []
    for value in scores.tolist():
        if value is None or (isinstance(value, float) and pd.isna(value)):
            result.append(None)
        else:
            result.append(float(value))

    still_missing = sum(1 for v in result if v is None)
    if still_missing:
        logger.warning(
            "[%s] %d responses still missing HuMT scores",
            source.id,
            still_missing,
        )
    return result


def load_source(source: SourceConfig) -> list[ResponseRow]:
    """Load one configured source and return normalized response rows."""

    responses = read_csv(source.response_file).reset_index(drop=True)
    humt = read_csv(source.humt_file).reset_index(drop=True)
    scores = _join_humt(responses, humt, source)

    rows: list[ResponseRow] = []
    for i, row in responses.iterrows():
        response_text = row.get("response_text", "")
        if pd.isna(response_text):
            response_text = ""
        response_text = str(response_text)

        prompt = row.get("prompt", "")
        if pd.isna(prompt):
            prompt = ""

        topic = row.get("topic", "")
        if pd.isna(topic):
            topic = ""

        failure_mode = None
        if "failure_mode" in row.index and pd.notna(row["failure_mode"]):
            failure_mode = str(row["failure_mode"])

        source_set = str(row.get("source_set", source.set))
        if source_set in ("nan", ""):
            source_set = source.set

        prompt_id = _resolve_prompt_id(row)
        humt_score = scores[int(i)]

        rows.append(
            ResponseRow(
                source_id=source.id,
                source_set=source_set,
                model=source.model,
                prompt_id=prompt_id,
                question_id=prompt_id,
                topic=str(topic),
                failure_mode=failure_mode,
                prompt=str(prompt),
                response=response_text,
                humt_score=humt_score,
                response_file=str(source.response_file),
                humt_file=str(source.humt_file),
                row_index=int(i),
            )
        )

    logger.info(
        "[%s] Loaded %d response rows (model=%s)",
        source.id,
        len(rows),
        source.model,
    )
    return rows


def load_all_sources(sources: tuple[SourceConfig, ...]) -> list[ResponseRow]:
    """Load every configured source in config order."""

    all_rows: list[ResponseRow] = []
    for source in sources:
        all_rows.extend(load_source(source))
    logger.info("Total normalized rows: %d", len(all_rows))
    return all_rows
