# PERSONA-MH human annotation packet

This directory contains blinded, two-phase annotation materials for protocol `persona_mh_human_v2`.

## Give annotators

### Phase 1

- `persona_mh_phase1_oa_annotation.csv`
- `PERSONA_MH_Phase1_OA_Instructions.docx`

Collect and lock Phase 1 before distributing Phase 2.

### Phase 2

- `persona_mh_phase2_edf_annotation.csv`
- `PERSONA_MH_Human_Annotation_Protocol_v2.docx`

Make one copy of each CSV per annotator. Require an `annotator_id` in every completed row. Do not let annotators collaborate before independent submission.

## Do not give annotators

`persona_mh_item_key_DO_NOT_SHARE_WITH_ANNOTATORS.csv` maps blinded item IDs to model and source metadata. Keep it with the research team. It is needed to merge completed ratings and run model/dataset analyses.

## Why OA uses a separate phase

OA must be independently elicited, not calculated from E, D, and F. A separate file and locked first pass prevent annotators from copying, averaging, or consciously reconstructing the component scores. Phase 2 uses a different fixed row order to reduce carryover.

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

## Collection safeguards

- Preserve every annotator's original submitted files unchanged.
- Do not average ratings before reliability analysis.
- Retain item-level and annotator-level scores.
- Calculate inter-rater reliability separately for OA, E, D, and F.
- Adjudicate only after independent ratings are archived.
- Follow the approved ethics/IRB, data-storage, and annotator-wellbeing procedures.
