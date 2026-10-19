# Lesson 5.5 — What a 97% hides

**Domain 5: Context Management & Reliability — 15% of CCAR-F**
**Task Statement 5.5:** Design human review workflows and confidence calibration.

Lab artifact: Course Doctor's accuracy reported per lesson type and per field, not as one
number.

## What you will be able to do afterwards

Say what an aggregate accuracy figure does not tell you, sample high-confidence output so
the measurement means something, and calibrate a confidence score against labelled data
rather than trusting it.

## Why the exam cares

This is the last task statement of the exam and it is the one that decides whether anything
else was real. The guide's framing is a warning: **aggregate accuracy metrics, its example
being 97% overall, may mask poor performance on specific document types or fields.**

Ninety-seven percent is a number that stops questions. It can be 97% overall and 60% on one
document type that happens to be a fifth of your volume, and nothing about the headline
says so.

Its remedies are a measurement programme rather than a prompt change: **stratified random
sampling** of the high-confidence population, **accuracy analysed by document type and by
field**, and **field-level confidence calibrated using labelled validation sets** before
human review is reduced.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Aggregate versus segmented metric.** One number against a number per population. *Why it
matters here:* the whole warning. *Depth:* any treatment of Simpson's paradox, which is the
formal version of this.

**Stratified random sampling.** Sampling within defined strata rather than across the whole
population. *Why it matters here:* a simple random sample of everything barely touches a
rare-but-important segment. *Depth:* standard sampling theory.

**Calibration.** Whether a stated confidence matches observed accuracy — if things marked
90% confident are right 90% of the time, the score is calibrated. *Why it matters here:*
without it a confidence score is a word. *Depth:* calibration curves and reliability
diagrams.

**Labelled validation set.** Cases where the right answer is known independently. *Why it
matters here:* it is the only thing you can calibrate against. *Depth:* the build.

**Automation threshold.** The confidence level above which no human looks. *Why it matters
here:* it is the decision this whole task statement exists to inform. *Depth:* the build.

## The idea, before any measurement

**Never let one number stand for a system.** Report by segment — document type, field,
source — because that is where the variance lives. The guide's instruction is to validate
accuracy **by document type and field segment before automating high-confidence
extractions**, and the order matters: segment first, then automate.

**Sample inside the population you are about to trust.** The temptation is to sample the
low-confidence cases, because that is where the errors are expected. But those are already
going to a human. The question that matters is *what is wrong in the batch nobody will
look at* — so stratified random sampling **of high-confidence extractions**, which is the
guide's own wording, and it is counterintuitive on purpose.

**Calibrate rather than assume.** A field-level confidence score is only a routing signal
once you have compared it against labelled outcomes. Before that it is a number the model
produced, and lesson 5.2 already told you self-reported confidence is an unreliable proxy.
**This lesson is how it stops being one.**

## The build

### Step 1 — segment the metric

```
OVERALL            94%  (the number that stops questions)

BY LESSON TYPE
  cited to docs    98%
  cited to guide   96%
  OBSERVED claims  71%   <- a fifth of the corpus
BY FIELD
  verdict          97%
  quoted_support   99%
  read date        68%   <- nobody checked these
```

Same data, two segments, and the 94% was hiding both. The two low cells are where the work
is, and neither is visible in the headline.

### Step 2 — sample the population you are about to stop checking

```
population      claims marked high confidence   (812)
sample          stratified: 20 per lesson type, randomly within each
label           a human decides each, independently
measure         error rate per stratum, and any NEW error pattern
```

Two outputs. The error rate tells you whether automation is safe; the novel patterns tell
you what your criteria do not yet cover — and that second one is why the sample has to be
*random within strata* rather than chosen.

### Step 3 — calibrate the score

```
confidence   n     actually correct
high         812   96%     -> roughly calibrated
medium       240   81%     -> roughly calibrated
low           94   79%     -> NOT calibrated: barely different from medium
```

Low confidence predicting 79% means the score is not separating the cases you most wanted
it to separate. That is a finding about your *instrument*, and until it is fixed, routing
on low confidence routes near-randomly.

### Step 4 — set the threshold from the measurement

```
automate        high confidence AND lesson type in (cited-to-docs, cited-to-guide)
human review    everything OBSERVED, regardless of confidence
human review    any missing read date, regardless of confidence
```

Two of those three rules come from the segmentation, not the confidence score. That is the
point: the segment can override the score, because the segment is where the variance was.

## Tips

Things that cost somebody an hour, or considerably more.

**An aggregate accuracy figure is a claim about a population you have not described.** Ask
"97% of what, split how?" before anything else. Nobody asks, because 97% sounds settled.

**Sample the high-confidence batch, not the low one.** The low-confidence cases are going
to a human anyway. The unexamined population is the only one where an error survives.

**A confidence score is a word until it is calibrated.** And when you do calibrate it, the
useful finding is often that two adjacent levels barely differ — which means the score is
not separating what you needed separated.

**Report the denominator with every rate.** "96% accurate" on 25 sampled claims is a
different statement from the same figure on 812, and the number alone cannot tell you
which.

**A segment can override a confidence score, and usually should.** If one document type is
weak, route all of it to review regardless of how confident the model is about any
individual case — because the weakness is in the type, not in the instance.

**Re-measure after changing the prompt.** A calibration is a property of one configuration.
Change the criteria and the mapping from score to accuracy moves, silently.

## The anti-pattern

From the guide's objectives:

> **Relying on an aggregate accuracy metric** that may mask poor performance on specific
> document types or fields.

> **Reducing human review before validating accuracy by document type and field segment.**

> **Routing on field-level confidence that has not been calibrated against a labelled
> validation set.**

Exam shape: when one option quotes an overall accuracy figure as grounds for automating and
another segments or samples first, the second is the answer. The guide treats the aggregate
as actively misleading rather than merely incomplete.

## What this lesson does not cover

- **Escalation triggers** — lesson 5.2, which rules out *uncalibrated* confidence as a
  trigger. This lesson is how it earns its place as a routing signal.
- **Confidence self-reporting in a review architecture** — lesson 4.6.
- **Defining the criteria being measured** — lesson 4.1. Calibrating a vague criterion
  measures how consistently it is misapplied.
- **Statistical sample-size calculation.** The guide names stratified random sampling and
  does not give sizes; neither does this lesson, and a number invented here would be worse
  than none.
- **Inter-rater agreement**, which is the right tool when the human labels are themselves
  uncertain, and is outside the guide's objectives.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 5.5.

| Claim | Source |
|---|---|
| The risk that aggregate accuracy metrics, e.g. 97% overall, may mask poor performance on specific document types or fields | EG §6, TS 5.5 |
| Stratified random sampling for measuring error rates in high-confidence extractions and detecting novel error patterns | EG §6, TS 5.5 |
| Field-level confidence scores calibrated using labelled validation sets for routing review attention | EG §6, TS 5.5 |
| The importance of validating accuracy by document type and field segment before automating high-confidence extractions | EG §6, TS 5.5 |
| Implementing stratified random sampling of high-confidence extractions for ongoing error-rate measurement and novel pattern detection | EG §6, TS 5.5 |
| Analysing accuracy by document type and field to verify consistent performance across all segments before reducing human review | EG §6, TS 5.5 |
| Having models output field-level confidence scores, then calibrating review thresholds using labelled validation sets | EG §6, TS 5.5 |
| Routing extractions with low model confidence or ambiguous/contradictory source documents to human review, prioritising limited reviewer capacity | EG §6, TS 5.5 |
| Self-reported confidence scores are unreliable proxies for complexity — which is what calibration against labelled data addresses | EG §6, TS 5.2 |
