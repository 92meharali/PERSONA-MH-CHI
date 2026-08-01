# PERSONA-MH v2 research summary (relaxed system prompt)

## Condition

v2 uses a relaxed professional-therapist system prompt (no anti-anthropomorphism ban). Same 220 CounselBench prompts; models are Claude Opus 4.8, GLM, and GPT-5.6-Sol. Five annotators; protocol v3.1.

## Confirmatory hypotheses (v2)

| ID | Claim | Result |
|---|---|---|
| H1 | HuMT is not a reliable OA proxy | Supported (ρ≈−0.17; tiny HuMT-only fit) |
| H2 | E/D/F add beyond HuMT | Supported (ΔCV R²≈0.338) |
| H3 | E↑ F↑ with OA; D↓ with OA | Supported |
| H4 | Models differ in OA/E/F | Supported (larger than v1; W≈0.41) |

## Key v2 numbers

- Reliability (ICC avg of 5): OA 0.85, E 0.95, D 0.96, F 0.86
- S tracks OA (ρ≈0.43)
- Consensus median D: D1=163, D2=297, D3=190, D4=10
- Model ranking by S / OA: GPT ≳ Claude ≳ GLM

## v1 vs v2 (shared models: Claude + GLM)

| Metric | v1 | v2 | Δ (v2−v1) |
|---|---|---|---|
| D | 1.49 | 2.23 | **+0.74** |
| OA | 4.45 | 4.12 | **−0.33** |
| E | 3.53 | 3.76 | +0.23 |
| F | 4.26 | 4.16 | −0.10 |

Relaxed prompting substantially raises deception risk and lowers overall appropriateness on the shared-model paired contrast. Outputs: `analysis_outputs_v2/`, `analysis_outputs_compare/`.
