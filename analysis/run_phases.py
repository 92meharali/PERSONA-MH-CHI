"""Run PERSONA analysis phases 1-4 end to end.

    python -m analysis.run_phases

Every phase is deterministic given the seed in ``persona_common.SEED`` and
depends only on files under ``data/clean_domains/``.
"""

from __future__ import annotations

import time

from . import build_dataset, descriptives, domain_interactions, humt_provenance_audit, predictive, reliability
from .persona_common import OUT_DIR, PROCESSED_DIR, env_versions, save_json

PHASES = [
    ("1 - dataset build and audit", build_dataset.main),
    ("1b - HuMT provenance audit", humt_provenance_audit.main),
    ("2 - annotation reliability", reliability.main),
    ("3 - descriptives and separability", descriptives.main),
    ("4 - cross-validation, ablation, incremental validity", predictive.main),
    ("5 - domain interactions", domain_interactions.main),
]


def main() -> None:
    started = time.time()
    timings = {}
    for name, run in PHASES:
        phase_start = time.time()
        print(f"\n=== Phase {name} ===")
        run()
        timings[name] = round(time.time() - phase_start, 2)

    save_json({"environment": env_versions(), "phase_seconds": timings,
               "processed_dir": str(PROCESSED_DIR), "outputs_dir": str(OUT_DIR)}, "run_manifest")
    print(f"\nAll phases complete in {time.time() - started:.1f}s. Outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
