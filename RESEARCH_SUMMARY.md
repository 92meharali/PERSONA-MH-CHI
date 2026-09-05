# PERSONA Research Summary

This file is now a pointer, not a source of hand-entered results.

The canonical research entry point is [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md).
That index routes readers to the theory documents, cleaned datasets, annotation
rubrics, analysis scripts, generated reports, and limitations.

## Current Status

PERSONA is a proposed framework for studying when anthropomorphic AI behavior is
appropriate in context. It is not presented as fully validated.

The framework is:

```text
P = (H, E, D, F)
```

where `H` is automated human-likeness, `E` is empathic appropriateness, `D` is
anthropomorphic deception risk, and `F` is domain fit. `OA` is the
independently elicited holistic appropriateness judgment examined by the
analysis. The optional scalar `S` is secondary and should not replace the
profile.

The framework is informed by the distinction between generalizable knowledge
and situation-sensitive practical judgment. This Episteme--Phronesis framing is
a conceptual lens only: HumT does not measure factual knowledge, and PERSONA
does not claim to measure or confer practical wisdom. Context refers to the
broader interactional environment; mental health, education, and general health
are the bounded domains evaluated in the current study.

## Canonical Locations

| Content | Where to read |
|---|---|
| Research archive index | [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md) |
| Theory foundation | [`docs/theory/README.md`](docs/theory/README.md) |
| Construct definitions | [`docs/theory/CONSTRUCT_DEFINITIONS.md`](docs/theory/CONSTRUCT_DEFINITIONS.md) |
| Research questions | [`docs/theory/RESEARCH_QUESTIONS.md`](docs/theory/RESEARCH_QUESTIONS.md) |
| Hypotheses | [`docs/theory/HYPOTHESES.md`](docs/theory/HYPOTHESES.md) |
| Claim boundaries | [`docs/theory/CLAIMS_AND_BOUNDARIES.md`](docs/theory/CLAIMS_AND_BOUNDARIES.md) |
| Reproducible analysis | [`analysis/README.md`](analysis/README.md) |
| Generated reports | [`analysis/outputs/reports/`](analysis/outputs/reports/) |
| Cleaned datasets | [`data/clean_domains/`](data/clean_domains/) |

## Why This File Changed

Earlier versions of this summary contained manually transcribed analysis numbers.
The Phase 1-5 pipeline now makes generated outputs canonical, so results should
be read directly from `analysis/outputs/` rather than duplicated here.

This avoids stale figures and keeps the repository easier to audit for CHI-style
review.
