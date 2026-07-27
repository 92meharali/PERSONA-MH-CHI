# PERSONA-MH human annotation packet

This directory contains blinded, two-phase annotation materials for protocol `persona_mh_human_v2`.

## Give annotators

### Phase 1

- `persona_mh_phase1_oa_annotation.csv`
- `PERSONA_MH_Phase1_OA_Instructions.docx`

For the strongest independent OA design, assign Phase 1 and Phase 2 to separate rater pools. OA raters must never receive the E/D/F rubric. If resources require the same raters, collect and lock Phase 1, use a pre-specified washout interval, and report same-rater carryover as a limitation.

### Phase 2

- `persona_mh_phase2_edf_annotation.csv`
- `PERSONA_MH_Human_Annotation_Protocol_v2.docx`

Make one copy of each CSV per annotator. Require an `annotator_id` in every completed row. Do not let annotators collaborate before independent submission.

## Do not give annotators

`persona_mh_item_key_DO_NOT_SHARE_WITH_ANNOTATORS.csv` maps blinded item IDs to model and source metadata. Keep it with the research team. It is needed to merge completed ratings and run model/dataset analyses.

`persona_mh_build_manifest.json` records protocol version, seeds, and checksums for the source files and configuration.

## Why OA uses a separate phase

OA must be independently elicited, not calculated from E, D, and F. Separate rater pools remove direct same-rater carryover. When separate pools are infeasible, separate files and a locked first pass prevent copying or averaging the component scores; Phase 2 also uses a different fixed row order.

## Rating fields

All rating, reason, evidence, scenario, review, and note cells are intentionally blank. Prompt and response text are populated because those are the annotation stimuli. Model labels, HuMT values, and prior automated PERSONA scores are excluded from annotator-facing files.

Allowed `scenario_type` values:

- `crisis_risk`
- `general_distress`
- `psychoeducation`
- `boundary_authority`
- `casual_checkin`
- `other`

Scores must be whole numbers from 1 through 5. Evidence must be copied exactly from the response. Separate multiple evidence quotes with ` | `.

## Rebuild

From the repository root:

```bash
pip install -r annotation_materials/requirements.txt
python annotation_materials/build_annotation_packet.py
```

The builder uses fixed random seeds, validates all 660 configured responses, and regenerates the CSV and DOCX files deterministically apart from DOCX package metadata.

Create a separately randomized, pre-assigned copy for each annotator by using a unique seed:

```bash
python annotation_materials/build_annotation_packet.py \
  --make-copy phase1 \
  --annotator-id OA_RATER_01 \
  --order-seed 41001 \
  --output private_assignments/OA_RATER_01.csv
```

Use `--make-copy phase2` for an E/D/F rater. Record every seed in the study log. Never reuse annotator IDs. Individually randomized orders reduce shared fatigue and comparison effects; `presentation_order` is retained for diagnostics.

## Collection safeguards

- Preserve every annotator's original submitted files unchanged.
- Validate `protocol_id=persona_mh_human_v2` and `rubric_version=2.0` on import.
- Do not average ratings before reliability analysis.
- Retain item-level and annotator-level scores.
- Calculate inter-rater reliability separately for OA, E, D, and F.
- Adjudicate only after independent ratings are archived.
- Follow the approved ethics/IRB, data-storage, and annotator-wellbeing procedures.
