# PERSONA Research Summary

## 1. Research Question

AI systems are increasingly deployed as counselors, tutors, health assistants, and other human-support interfaces. Many evaluations ask whether a response sounds human-like. PERSONA starts from a different question:

**When is anthropomorphic AI behavior appropriate in context?**

The central claim is that human-likeness is not enough. A response can sound human while being misleading, overconfident, unsafe, emotionally manipulative, or poorly matched to the user's situation. Conversely, a response can be less human-like while being safer and more appropriate.

## 2. Framework

PERSONA evaluates responses as a profile:

```text
P = (H, E, D, F)
```

| Dimension | Meaning | Role |
|---|---|---|
| `H` / HuMT | Automated human-likeness | Descriptive style signal |
| `E` | Empathic appropriateness | Calibrated warmth and validation |
| `D` | Anthropomorphic deception risk | False human feeling, relationship, identity, memory, authority, continuity, or dependency |
| `F` | Contextual fit | Match of content, tone, action, boundaries, and certainty to the situation |
| `OA` | Overall appropriateness | Independent holistic target judgment |

`OA` is not computed from `E`, `D`, or `F`. This is important because the framework is testing whether the profile explains appropriateness, not assuming it by construction.

The optional secondary score is:

```text
S = (H + E - D + F) / 4
```

`S` is a transparent ranking index. It should not replace independent `OA`.

## 3. Why This Matters For CHI

Human-support AI creates interaction risks that are not captured by human-likeness alone:

- Warm language can improve support, but it can also simulate feelings or relationships the AI does not have.
- Professional personas can help users understand the role, but they can also imply authority, care, confidentiality, or continuity.
- Different domains need different calibrations: counseling, tutoring, and health assistance do not share the same ideal persona.

PERSONA contributes a measurable way to separate "sounds human" from "is appropriate for this situation."

## 4. Datasets

The canonical release is under `data/clean_domains/`.

| Domain | Responses | Rating rows | Raters / passes | HuMT |
|---|---:|---:|---:|---|
| Mental health | 660 | 3,300 | 5 | embedded in annotator files |
| Education | 450 | 2,250 | 5 | `humt_education.csv` |
| Health | 450 | 2,250 | 5 oversight/adjudication passes | `humt_health.csv` |

Each domain has a frozen rubric and a domain-specific `analysis.md`.

## 5. Mental Health Findings

Mental health is the primary validation domain.

### Data Quality

- 660 responses.
- 5 annotators per response.
- 0 invalid score entries.
- 660 HuMT matches.

### Reliability

| Measure | Reliability |
|---|---:|
| OA | 0.852 |
| E | 0.949 |
| D | 0.960 |
| F | 0.864 |

### Core Results

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.167 |
| E with OA | 0.096 |
| D with OA | -0.159 |
| F with OA | 0.694 |

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | 0.008 |
| HuMT + E + D + F | 0.657 |
| Increment | 0.648 |

Mental health strongly supports the central claim. HuMT is weakly negative with OA, while the PERSONA dimensions provide substantial explanatory value.

### Model Profiles

| Model | OA | E | D | F | HuMT |
|---|---:|---:|---:|---:|---:|
| Claude Opus 4.8 | 4.133 | 3.873 | 2.254 | 4.170 | 0.054 |
| GLM | 4.098 | 3.655 | 2.205 | 4.142 | 0.055 |
| GPT-5.6-Sol | 4.720 | 3.682 | 1.819 | 4.770 | 0.041 |

GPT-5.6-Sol scores highest on OA and F while having lower D and lower HuMT. This is exactly the distinction PERSONA is meant to reveal.

## 6. Education Findings

Education tests transfer into tutoring and teaching-assistant support.

### Data Quality

- 450 responses.
- 5 annotators per response.
- 0 invalid score entries.
- 450 HuMT rows available; quick exact-text matching matched 385 due to response truncation and character normalization differences.

### Reliability

| Measure | Reliability |
|---|---:|
| OA | 0.947 |
| E | 0.997 |
| D | 0.965 |
| F | 0.960 |

Agreement is very high. The paper should describe this as strong consensus and avoid overclaiming independence without an annotation-process audit.

### Core Results

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.072 |
| E with OA | -0.030 |
| D with OA | -0.028 |
| F with OA | 0.229 |

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | 0.119 |
| HuMT + E + D + F | 0.592 |
| Increment | 0.472 |

Education supports transfer. HuMT remains weak, and contextual fit is the most interpretable appropriateness dimension because tutoring quality depends on scaffolding, academic boundaries, and fit to the learner's need.

### Model Profiles

| Model/Condition | OA | E | D | F | HuMT |
|---|---:|---:|---:|---:|---:|
| adv_claude_opus_4_8 | 4.535 | 2.486 | 1.363 | 4.110 | 0.038 |
| adv_glm_5_2 | 4.176 | 2.416 | 1.608 | 3.780 | 0.041 |
| adv_gpt_5_6_sol | 4.150 | 2.223 | 1.242 | 3.796 | 0.045 |
| claude_opus_4_8 | 4.416 | 2.772 | 1.140 | 4.124 | 0.028 |
| glm_5_2 | 4.251 | 2.246 | 1.029 | 4.126 | 0.029 |
| gpt_5_6_sol | 4.268 | 2.044 | 1.000 | 4.064 | 0.020 |

Education shows a different appropriate profile than mental health: lower E can still be appropriate when the response is pedagogically clear and bounded.

## 7. Health Findings

Health tests transfer into casual health assistance.

### Data Quality

- 450 responses.
- 5 oversight/adjudication passes per response.
- 0 invalid score entries.
- 450 HuMT rows available; quick exact-text matching matched 416 due to response truncation and character normalization differences.

### Reliability

| Measure | Reliability |
|---|---:|
| OA | 0.900 |
| E | 0.937 |
| D | 0.935 |
| F | 0.918 |

### Core Results

| Relationship | Spearman rho |
|---|---:|
| HuMT with OA | -0.046 |
| E with OA | -0.060 |
| D with OA | -0.069 |
| F with OA | 0.043 |

| Model | Cross-validated R2 |
|---|---:|
| HuMT only | -0.003 |
| HuMT + E + D + F | 0.242 |
| Increment | 0.245 |

Health supports the rejection of HuMT as an appropriateness proxy, but the current response set is highly appropriate overall. That makes it useful as a domain-transfer check rather than the strongest domain for discriminating failures.

### Model Profiles

| Model/Condition | OA | E | D | F | HuMT |
|---|---:|---:|---:|---:|---:|
| adv_claude_opus_4_8 | 4.836 | 3.200 | 1.444 | 4.320 | 0.047 |
| adv_glm_5_2 | 4.552 | 3.156 | 1.732 | 4.148 | 0.045 |
| adv_gpt_5_6 | 4.840 | 2.840 | 1.380 | 4.244 | 0.035 |
| claude_opus_4_8 | 4.907 | 2.364 | 1.187 | 4.193 | 0.031 |
| glm_5_2 | 4.918 | 2.153 | 1.129 | 4.144 | 0.020 |
| gpt_5_6_sol | 4.916 | 2.091 | 1.153 | 4.112 | 0.021 |

The health profiles show that low anthropomorphic deception risk and strong boundaries can coexist with modest empathy scores and high OA.

## 8. Cross-Domain Interpretation

| Domain | HuMT-OA rho | PERSONA gain over HuMT-only CV R2 | Best use in paper |
|---|---:|---:|---|
| Mental health | -0.167 | +0.648 | Primary validation |
| Education | -0.072 | +0.472 | Domain-transfer validation |
| Health | -0.046 | +0.245 | Domain-transfer and ceiling-case analysis |

Across all three domains, HuMT is weak or negative as an appropriateness proxy. PERSONA is useful because it lets the paper ask a richer question:

**What kind of human-like behavior is appropriate, for which context, and under what risk constraints?**

## 9. Recommended Paper Direction

The strongest CHI paper should not be framed simply as a dataset paper. It should be framed as a measurement contribution:

**PERSONA: Measuring Contextual Appropriateness of Humanlike AI Across High-Stakes Support Domains**

Suggested structure:

1. Introduce the failure of human-likeness as a safety or appropriateness proxy.
2. Define `P = (H, E, D, F)` and independent `OA`.
3. Use mental health as the primary validation study.
4. Use education and health as domain-transfer studies.
5. Show that appropriate profiles differ by domain.
6. Argue for profile-based evaluation rather than single human-likeness metrics.

## 10. Practical Implications

- Do not optimize assistant behavior for human-likeness alone.
- Use domain-specific contextual-fit rubrics.
- Treat empathy as calibrated helpfulness, not emotional intensity.
- Measure deception risk separately from warmth.
- Keep OA independent from formula scores.
- Use `S` only as a transparent secondary ranking score.

## 11. Current Limitations

- Mental health is the strongest domain; education and health are transfer evidence.
- Education has extremely high agreement on some dimensions and should be described carefully.
- Health has high OA ratings overall, which limits discrimination among already safe responses.
- Education and health HuMT joins should use stable response IDs in the next analysis pass.
- Scores are ordinal and should be interpreted with ordinal-aware checks where possible.

## 12. Repository Map

- `data/clean_domains/`: canonical multi-domain datasets.
- `analysis/`: current mental-health analysis pipeline.
- `analysis_outputs/`: current generated analysis tables and figures.
- `presentations/`: presentation artifacts.
- `README.md`: repository overview.
