"""Basic unit tests for analysis helpers."""

from __future__ import annotations

import numpy as np

from analysis.utils import cliffs_delta, cohens_d, hedges_g, mean_ci


def test_effect_sizes_direction() -> None:
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([10.0, 11.0, 12.0, 13.0])
    assert cohens_d(a, b) < 0
    assert hedges_g(a, b) < 0
    assert cliffs_delta(a, b) < 0


def test_mean_ci_keys() -> None:
    out = mean_ci([1, 2, 3, 4, 5])
    assert out["n"] == 5
    assert out["ci_low"] <= out["mean"] <= out["ci_high"]
