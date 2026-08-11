# Literature map

Organised around the argument rather than by topic convenience. Citation keys
resolve in `BIBLIOGRAPHY.md`, which separates **verified** references from those
**needing verification**. Every key marked `[NV]` below is one whose
bibliographic details have not yet been confirmed and which must not be cited in
a submission until they are.

---

## A. Anthropomorphism

**What it is.** Anthropomorphism is the attribution of humanlike
characteristics, motivations, intentions, or emotions to non-human agents
[Epley2007]. It is common but not invariant: [Epley2007] models it as driven by
the accessibility of anthropocentric knowledge, effectance motivation (the need
to explain and predict an agent's behaviour), and sociality motivation (the
desire for social contact). [Waytz2010] shows these tendencies are stable
individual differences that predict how much trust and responsibility people
place in an agent.

**The distinction the project turns on.** [Epley2007] and [Waytz2010] describe
anthropomorphism as something a *person does*. HumT measures something a *system
emits*. These are different objects:

| | Anthropomorphic signalling | Anthropomorphic perception |
|---|---|---|
| Located in | The response text | The reader |
| Measured by | HumT, taxonomies of linguistic cues | Self-report, behavioural measures |
| Varies with | Model, prompt, decoding | Person, situation, prior exposure |

PERSONA measures signalling. It does not measure perception, and must not claim
to. The [Epley2007] framework explains why signalling alone is insufficient: the
same cue lands differently depending on the reader's state, which is one reason
appropriateness cannot be read off the text alone.

**How it has been measured.** [DeVrio2025] provides a taxonomy of linguistic
expressions contributing to anthropomorphism of language technologies.
[Abercrombie2023] catalogues linguistic factors driving personification and
argues that prior efforts are fragmented. [Cheng2025HumT] introduces the
probability-based metric this project uses. [Feine2019][NV] offers a taxonomy of
social cues for conversational agents.

## B. Human-AI interaction

People respond socially to computers even when they know better — the CASA and
media-equation tradition [Nass1994][NV]; [Reeves1996][NV]; [Nass2000][NV]. This
is the foundational reason anthropomorphic design cues have effects at all, and
the reason a purely technical description of a system does not predict how it
will be received.

Relational agents — systems designed to build and maintain social-emotional
relationships with users over time [Bickmore2005][NV] — are the design tradition
PERSONA's `D` dimension is in tension with. That tradition treats relational
continuity as a feature; `D` treats claimed continuity as a risk when the claim
is false. The paper should engage this tension explicitly rather than assume the
risk framing.

[Araujo2018][NV] examines how anthropomorphic design cues shape perceptions of
conversational agents.

## C. Empathy and AI

[Sharma2020] is the anchor: empathy in text-based mental health support is
decomposable into distinct communication mechanisms and requires measurement
designed for asynchronous text rather than borrowed from face-to-face
instruments. [Sharma2021][NV] extends this to empathy-improving interventions.

**The gap this literature leaves.** These are measures of *how much* empathy is
expressed. They do not ask whether the expressed empathy was *right for the
situation*. PERSONA's `E` is a calibration measure, and its novelty relative to
this literature should be stated in exactly those terms.

**Risks of excessive simulated empathy.** [Ayers2023][NV] is frequently cited for
the finding that chatbot responses were rated more empathetic than physician
responses; this is a load-bearing citation for the claim that models are already
capable of high measured empathy, and it must be verified before use.
[Cheng2025HumT] finds human-like output correlates with warmth, social closeness,
and low status attributions — connecting the empathy channel directly to the
anthropomorphism literature.

## D. Deception and anthropomorphic misrepresentation

[Leong2019] is the primary conceptual source: dishonest anthropomorphism, built
on the honest-anthropomorphism principle of [Kaminski2017], with a taxonomy of
types and associated harms. The core concern — designs that exploit predictable
human responses to human-like cues against the user's interest — is `D`'s
ancestor.

[Abercrombie2023] links personification to transparency failures and
over-reliance. [Sharkey2020][NV] argues deception in social robotics needs
explicit treatment. [Danaher2020][NV] provides an ethical taxonomy of robotic
deception. [Park2024][NV] surveys AI deception examples and risks.
[Weidinger2021][NV] situates anthropomorphic misrepresentation within a broader
risk taxonomy for language models.

**Trust and reliance.** The harm mechanism is over-reliance: appropriate reliance
requires that a user's trust track the system's actual reliability
[Lee2004][NV]. Anthropomorphic cues can inflate trust independently of
reliability, which is what makes false implication of experience or authority a
risk rather than a stylistic quibble. [Bucinca2021][NV] demonstrates
interventions against over-reliance in AI-assisted decisions.

**Regulation.** EU AI Act Article 50 requires disclosure that a user is
interacting with an AI system, enforceable from 2 August 2026 [EUAIAct2024]. This
is a *disclosure* obligation, not a *behaviour* obligation — which is exactly the
space `D` occupies. A system can disclose once at the start of a conversation,
fully satisfying Article 50, and then imply feeling, memory, and relationship
throughout. The paper can position `D` as measuring what disclosure rules do not
reach, provided it does not claim to be a compliance tool.

## E. Contextual appropriateness

Appropriateness norms are context-relative. [Nissenbaum2004][NV] argues
informational norms are specific to social contexts rather than universal — the
closest available theoretical grounding for the claim that what is appropriate in
education is not what is appropriate in crisis support.

High-stakes conversational systems bring domain-specific expectations.
[CounselBench2025] evaluates LLM behaviour in single-turn mental health
counselling against six clinically grounded dimensions rated by 100 mental health
professionals, and finds that models can score highly on perceived quality while
being flagged by experts for safety concerns such as unauthorised medical advice.
That dissociation — high perceived quality, expert-identified inappropriateness —
is empirical precedent for PERSONA's central premise, from an adjacent construct
pair.

[CounselBench2025] also finds that LLM judges systematically overrate model
responses and overlook safety issues human experts identify, which is a direct
argument for human rather than model annotation of `OA`.

## F. Human-likeness versus appropriateness

This section carries the paper's core claim and deserves the most care.

**Direct support.** [Cheng2025HumT] reports that across preference and usage
datasets, users prefer *less* human-like outputs in many contexts. This is the
strongest available evidence that human-likeness is not monotonically desirable,
and it comes from the authors of the metric this project uses — which both
strengthens the citation and obliges the paper to acknowledge that the premise
was established before PERSONA rather than by it.

**Complicating evidence.** The same paper finds human-like output correlates with
warmth and social closeness, which in support contexts are usually desirable.
Human-likeness therefore has genuinely mixed valence rather than negative valence
— consistent with PERSONA's calibration framing and inconsistent with any
"anthropomorphism is harmful" reading.

**What is still missing, and what PERSONA adds.** [Cheng2025HumT] establishes
that preference and human-likeness diverge. It does not decompose *why*, and it
does not test whether the divergence differs by domain. PERSONA's contribution is
the decomposition — separating the relational channel (`E`), the boundary channel
(`D`), and the calibration channel (`F`) — and evaluating them against an
independently elicited criterion.

**A hazard to state plainly.** If, empirically, the profile's explanatory power
concentrates in one dimension, the honest contribution is narrower than "a
multidimensional framework": it becomes evidence about *which* channel carries
appropriateness. That would still be a result worth reporting, but it is a
different paper from the one the framing currently promises, and the framing
should follow the data rather than the reverse (§18 of the analysis plan).

---

## The research gap, constructed

Not "few studies have investigated". The gap follows from the literature:

1. **Human-like behaviour can be measured automatically and at scale.**
   [Cheng2025HumT]; [DeVrio2025]; [Abercrombie2023].
2. **Human-likeness is not equivalent to appropriateness.** Users prefer less
   human-like output in many contexts [Cheng2025HumT]; anthropomorphic cues can
   inflate trust beyond warranted levels [Leong2019]; [Abercrombie2023].
3. **Existing evaluation collapses distinct interactional properties.** Empathy
   measures quantify expression without calibration [Sharma2020]; quality
   benchmarks score responses without separating relational, boundary, and
   contextual channels; model-based judges are unreliable for the properties
   experts care about [CounselBench2025].
4. **High-stakes contexts impose domain-specific expectations.** Expert raters
   flag safety and boundary failures that quality scores miss
   [CounselBench2025]; disclosure regulation now attaches specifically to
   conversational AI [EUAIAct2024].
5. **Therefore a framework is needed that separates descriptive human-likeness
   from relational, boundary, and contextual properties**, rather than treating
   human-likeness as the endpoint of evaluation.
6. **PERSONA proposes** `P = (H, E, D, F)`.
7. **PERSONA evaluates it against independently elicited `OA`**, so that the
   relationship between profile and appropriateness is an empirical finding
   rather than an algebraic consequence.

Step 4 is currently the weakest link: it rests substantially on
[CounselBench2025] plus regulatory context. Additional support for
domain-specific appropriateness expectations, particularly outside mental health,
would strengthen it. Recorded as an open task in `CITATION_MATRIX.md`.
