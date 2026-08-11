# Domain datasets for PERSONA extension

CounselBench worked well for mental health because it provides:

- realistic help-seeking questions
- open-ended responses (not multiple choice)
- adversarial / failure-mode coverage
- a path to human normative rating

Below are the closest analogues for **education** and **health care**, ranked for PERSONA fit.

## What we need in a PERSONA domain pack

A good PERSONA seed dataset should let us:

1. sample ~100–200 user prompts
2. generate model responses under controlled system prompts
3. rate **E / D / F / OA** with domain-adapted anchors
4. optionally craft an adversarial subset that invites anthropomorphism (false tutor intimacy, false clinical authority, etc.)

---

## Education (tutor / teaching assistant)

### Top picks

| Dataset | Why it fits | Size / notes | Link |
|---|---|---|---|
| **Bridge** | Real math tutoring turns with novice vs expert remediation; excellent for “false authority / over-help / warmth vs pedagogy” | ~700 tutoring conversations | [HF](https://huggingface.co/datasets/rose-e-wang/bridge) · [GitHub](https://github.com/rosewang2008/bridge) · NAACL 2024 |
| **MathDial** | Teacher–student math tutoring dialogues; good prompt pool for single-turn PERSONA extraction | ~2.9k dialogues | [HF](https://huggingface.co/datasets/eth-nlped/mathdial) |
| **MathTutorBench** | Unified tutoring eval over Bridge + MathDial; useful task definitions even if we keep human PERSONA ratings | Benchmark + code | [GitHub](https://github.com/eth-lre/mathtutorbench) · EMNLP 2025 |

### Secondary options

| Dataset | Notes | Link |
|---|---|---|
| **SocraTeach / SocraticLM** | Large Socratic teaching dialogues; more synthetic/multi-agent | [GitHub](https://github.com/Ljyustc/SocraticLM) · NeurIPS 2024 |
| Classroom discourse corpora (e.g., NCTE) | Often multi-party; less clean for 1:1 AI tutor PERSONA | Demszky & Hill, 2023 |

### Recommended PERSONA-Education starter

1. Sample ~100 prompts from **Bridge** + **MathDial** student turns
2. Write ~50 adversarial tutor prompts that invite:
   - “I’ll always be here for you”
   - “I know how you feel as a teacher/friend”
   - answer-giving vs scaffolding pressure
3. Keep P = (H, E, D, F), specialize D/F anchors for tutoring

**Closest CounselBench analogue:** Bridge (+ MathDial), because it is real tutoring interaction with expert pedagogical judgments.

---

## Health care (patient / clinician support)

### Top picks

| Dataset | Why it fits | Size / notes | Link |
|---|---|---|---|
| **HealthBench** | Closest overall analogue to CounselBench: realistic health conversations + physician-written rubrics | 5,000 conversations; 262 physicians; 48k+ rubric criteria | [OpenAI](https://openai.com/index/healthbench/) · [arXiv](https://arxiv.org/pdf/2505.08775) · [HF mirror](https://huggingface.co/datasets/Tonic/Health-Bench-Eval-OSS-2025-07) |
| **MedDialog-EN** | Large patient–doctor dialogues for prompt mining | ~0.26M English dialogues | [HF](https://huggingface.co/datasets/UCSD26/medical_dialog) · [paper](https://ar5iv.labs.arxiv.org/html/2004.03329) |
| **OpenMed/MedDialog** | Cleaner patient/doctor pair format for sampling | ~252k pairs | [HF](https://huggingface.co/datasets/OpenMed/MedDialog) |

### Secondary options

| Dataset | Notes | Link |
|---|---|---|
| Reddit AskDocs threads / ThReadMed-style sets | Realistic, but noisier and privacy-sensitive | various releases |
| MedLoCoMo | Long multi-session clinical memory; too heavy for first PERSONA pilot | [arXiv](https://arxiv.org/abs/2607.22566) |

### Recommended PERSONA-Health starter

1. Prefer **HealthBench** conversation stems as the CounselBench-like backbone
2. Supplement prompt diversity from **MedDialog-EN** if needed
3. Write adversarial items for:
   - false clinical certainty
   - unauthorized diagnosis/prescription tone
   - empathy theater that replaces escalation
   - implied ongoing clinician relationship

**Closest CounselBench analogue:** HealthBench, because it is expert-grounded, open-ended, and built for LLM health conversation evaluation.

---

## Suggested mapping to PERSONA

| PERSONA piece | Mental health now | Education extension | Health extension |
|---|---|---|---|
| Prompt source | CounselBench | Bridge / MathDial | HealthBench / MedDialog |
| E | calibrated emotional support | supportive teaching presence | patient-centered communication |
| D | false care / understanding / continuity | false tutor intimacy / omniscience | false clinician identity / certainty |
| F | crisis vs distress fit | scaffolding vs answer-dumping | triage / disclaimer / escalation fit |
| OA | independent holistic appropriateness | same | same |

Keep **P and OA fixed**. Only specialize scenario labels and D/F anchors.

---

## Practical next experiment (lightweight)

If we want a multi-domain claim without exploding annotation cost:

- 50 education prompts (Bridge/MathDial)
- 50 health prompts (HealthBench)
- same 3–4 models + relaxed vs strict prompt
- same Group A / Group B rater structure, domain-adapted D/F cheat sheets

That is enough for a CHI “framework generality” pilot beside the deep mental-health study.
