> **⚠ The written lessons are authoritative, not this script.** This was written
> 2026-10-18, after the documentation verification pass of the same date, so it does not
> lag the lessons today. It will. There is no automated check for script-versus-lesson
> drift — a diff cannot tell a legitimate rewording from a stale claim — so **re-read the
> lesson for each task statement below and reconcile before recording.**
>
> **This is a production asset, not the lesson.** It is the narration script for the video
> version: spoken wording, screen directions, and a recording checklist.
>
> **If you are here to learn, read the written lessons instead.**
> [The course front page](../../../README.md) lists all twenty-nine. This script covers
> task statements 5.1 through 5.5:
> [5.1](../lesson-5-1-conversation-context.md) ·
> [5.2](../lesson-5-2-escalation.md) ·
> [5.3](../lesson-5-3-error-propagation.md) ·
> [5.4](../lesson-5-4-codebase-exploration.md) ·
> [5.5](../lesson-5-5-human-review-and-calibration.md)

# Episode 5 — What a 97% hides

**Domain 5: Context Management & Reliability — 15% of CCAR-F**
Target runtime 7–8 minutes · ~1,200 spoken words
Ships: Course Doctor's confidence routing and its coverage statement — including what it
could not check

**This is the shortest episode and the smallest domain**, 15%. Runtime is proportional to
blueprint weight across the series, which is why this one is half the length of episode 3
and still covers all five of its task statements.

**It is also the series close.** The ending is different from the other four — see the note
before the final screen direction.

---

## Before you record

- Clean recording profile, per the recording checklist kept outside this repo.
- **Start from episode 4's commit.** This is the last one, so the repo shown here is the
  finished lab.
- **The "typically" degradation cannot be demonstrated in eight minutes.** It takes an
  extended session to appear. Describe the symptom; do not stage a fake instance of it.
- **Do not quote a calibration result for this lab.** No labelled validation set exists for
  Course Doctor, so there is nothing to calibrate against. Say that — it is the honest
  version and it is also the episode's own lesson applied to itself.
- The series close names what the course does not do. That is deliberate and it is the
  strongest ending available. Do not soften it into a call to action.

---

## Fundamentals

Not spoken on camera. For the written lesson and the episode description.

**Aggregate versus segmented metrics.** One number over a whole population against the same
number computed within each subgroup. *Why it matters here:* it is the whole of task
statement 5.5. The formal version is Simpson's paradox. *Depth:* any introductory
statistics text.

**Stratified random sampling.** Sampling *within* each stratum so a rare segment is actually
represented. *Why it matters here:* the guide names it as the remedy, and simple random
sampling does not substitute. *Depth:* standard sampling material.

**Calibration.** Whether a stated confidence matches observed accuracy, measured against
labelled data. *Why it matters here:* an uncalibrated confidence score is a word, and
routing on one is a named anti-pattern. *Depth:* calibration curves; the idea is old and
well documented.

**Denominator.** The population a rate is computed over. *Why it matters here:* a rate
without its n is not a claim. *Depth:* lesson 5.5.

**Lost in the middle.** The observed tendency of models to use the beginning and end of a
long input more reliably than the middle. *Why it matters here:* it makes position a design
decision rather than a formatting one. *Depth:* the guide's own wording in TS 5.1.

**Partial failure.** Some components succeed and some do not. *Why it matters here:* 5.3 is
about reporting which, honestly. *Depth:* any distributed systems text.

---

## Script

```
Ninety-seven percent is a number that stops questions.

[screen: the blueprint table, Domain 5 highlighted]

Domain 5 is the smallest domain, fifteen percent, and it contains the task
statement that decides whether anything else in this exam was real.

We'll get there. Five task statements, and this is the short episode.

[screen: the five task statements]

[screen: a summary that lost its numbers]

Five point one. Context.

The guide names two failures that are invisible while they happen.

First: progressive summarisation that condenses numerical values, percentages,
dates and customer-stated expectations into vague summaries.

Think about what that looks like. "The customer discussed a refund." That has
lost the amount, the date and the order number — and it reads perfectly well.
That's the whole problem. A summary that reads well has still lost your numbers.

The fix is a facts block. A short list of the values that must survive, carried
forward verbatim, separate from the prose. It's cheap and almost nobody writes
one.

[screen: beginning, middle, end of a long input]

Second failure, and the guide's wording is specific: models reliably process
information at the beginning and end of long inputs, but may omit findings from
middle sections.

So a long input is not uniformly attended. Which makes position a design
decision. Put what must be read first or last — and specifically, put your "not
covered" section at the end, where it will actually be read, rather than buried in
the middle where it reads as covered.

And trim tool output at the boundary, not when context gets tight. The guide's own
example is forty-plus fields per lookup when five are relevant.

[screen: an escalation trigger list]

Five point two. Escalation.

The guide lists the real triggers and then rules out the popular ones.

Legitimate: an explicit request for a human. A policy exception or gap — and it
says explicitly, not just complex cases. And an inability to make meaningful
progress.

Unreliable, in its own words: sentiment-based escalation and self-reported
confidence scores are unreliable proxies for actual case complexity.

Both of those are the obvious implementations. Sentiment measures how the person
sounds, not how hard the case is — so it misroutes in both directions. A calm
person with an impossible problem doesn't escalate, and a frustrated person with
an easy one does. And a confidence score measures a word, until you've calibrated
it, which is task statement five five.

[screen: an explicit request for a human]

And the sharpest rule in the domain, because it inverts a natural instinct:
honour an explicit request for a human immediately, without first attempting
investigation.

"Let me just try one thing first" is the helpful move. It's the named wrong
answer.

[screen: empty results beside a timeout]

Five point three. Error propagation.

Two anti-patterns, named in the same breath, pulling in opposite directions.
Silently suppressing errors — returning empty results as success. And terminating
an entire workflow on a single failure.

Both. Which tells you the answer is neither extreme.

Recover locally what you can. Propagate what you can't resolve, with enough
context for the coordinator to decide. And never let a failure render as a clean
result.

Of those two, suppression is the one you'll actually ship, because it's what
happens when nobody decides. An empty list is the default return value.

[screen: a failure reply with attempted and alternatives]

And the distinction from episode two returns, because it matters more at system
scale: an access failure versus a valid empty result. A timeout and a query that
legitimately matched nothing are both "no data" to a coordinator that can't tell
them apart.

Two fields that pay for themselves. What was attempted — so the coordinator
doesn't re-derive it. And what alternatives weren't tried. That second one is the
field nobody includes and the coordinator most wants.

[screen: a session saying "typically"]

Five point four. Long explorations.

The guide describes the symptom precisely, and it's the most useful sentence in
the task statement: in extended sessions, models start giving inconsistent answers
and referencing "typical patterns" rather than the specific classes discovered
earlier.

That's a diagnostic you can use today. When an agent stops naming the class it
read an hour ago and starts describing what such a class usually looks like — the
specific knowledge is gone. Nothing announces it. The answers stay fluent and
become generic.

"Typically" is the tell.

The remedies are all forms of getting findings out of the conversation.
Scratchpad files. Delegating the verbose exploration to a subagent that returns a
summary. Summarising between phases — before you spawn the next one, not after
you finish. And a structured state export, so a crash doesn't restart the whole
thing.

[screen: 97% in large type]

Five point five. And here's the ninety-seven percent.

The guide's framing is a warning: aggregate accuracy metrics — its example is
ninety-seven percent overall — may mask poor performance on specific document
types or fields.

So it can be ninety-seven percent overall and sixty percent on one document type
that happens to be a fifth of your volume. And nothing about the headline says
so.

[screen: the same figure, segmented]

The remedies are a measurement programme, not a prompt change. Three of them.

Stratified random sampling — and sample the high-confidence population, not the
low one, because the high-confidence batch is the one you were going to stop
checking. Accuracy analysed by document type and by field, not in aggregate. And
field-level confidence calibrated against a labelled validation set before you
reduce human review.

That last word is the one that matters. Before.

[screen: a confidence score with no validation set]

Which gives you the named anti-pattern: routing on field-level confidence that has
not been calibrated. A confidence score is a word until it's been measured against
labelled data. Until then it's the model's guess about its own guess.

And the exam shape is clean: when one option quotes an overall accuracy figure as
grounds for automating, and another segments or samples first, the second is the
answer. The guide treats the aggregate as actively misleading, not merely
incomplete.

One habit to leave with: report the denominator with every rate. "Ninety-seven
percent" is a claim about a population you haven't described.

[screen: the anti-pattern slide]

The anti-patterns for this domain.

Summarisation that condenses numbers, dates and stated expectations into vague
prose. Tool results accumulating out of proportion to their relevance. Treating a
long input as uniformly attended. Sentiment-based escalation. Self-reported
confidence as a complexity proxy. Investigating before honouring a request for a
human. Heuristic selection among multiple matches instead of asking for another
identifier. Suppressing errors as empty success. Terminating a workflow on one
failure. A generic error status that hides context. Letting a session degrade to
typical patterns. Exploring in the main context when a subagent could isolate it.
Relying on an aggregate accuracy metric. Reducing human review before validating
by segment. And routing on uncalibrated confidence.

[screen: the five anti-pattern slides, together]

That's fifteen in this domain, and more than forty across the five episodes.
Nearly all of them are named in the exam guide itself — a few, in episode one, I
drew from its knowledge and skills bullets rather than from a named anti-pattern
list, and I said so at the time.

I've said this every episode and it's the single most useful idea in this course:
well-written multiple-choice distractors are not random noise. They're the
plausible mistakes a competent person actually makes. That's what makes them work
as distractors. So a published list of anti-patterns is a published list of the
wrong answers' shapes.

And notice what nearly all of them have in common, across all five domains.

A cap that reads as a design. A tool list that reads as what the worker has. A
populated server list that reads as a working server. A restored transcript that
reads as current. A schema-valid document that reads as correct. An empty result
that reads as success. A broken hook that reads as a control. A ninety-seven
percent that reads as good enough.

Every one of them is something that looks right and quietly isn't. That's not five
domains. That's one idea, examined from five directions.

[screen: the finished repo]

That's the lab, finished, and it runs.

[NOTE: series close. Different ending from episodes 1 through 4 — no "next
episode". Keep the limitations paragraph; it is the point.]

Everything in this course came from the published exam guide or the public
documentation. Every claim is traced in SOURCES.md. Nothing came from sitting the
exam.

And one last thing, in the spirit of the task statement we just did.

This course has no practice questions, because the exam guide publishes sample
items with full rationales and there's no reason to write worse ones. It has no
pass-rate claim, because I don't have that data. The lessons were written by an
agent and checked by the same agent, which is the configuration episode four
called the weakest — so VERIFICATION.md records which pages were re-verified word
for word, which were not, and what that process still can't tell you. Five of
thirteen, at the time of recording.

A course about content freshness that didn't say that would be the anti-pattern.

Good luck with the exam. Repo link is below.
```

---

## Tips

Not spoken on camera — for the written lesson and the episode notes.

**A summary that reads well has still lost your numbers.** Fluency is not a check on
information loss, and it is actively misleading as one.

**Trim tool output at the boundary, not when context gets tight.** By the time context is
tight you are making the decision under pressure and will trim the wrong thing.

**Put what must be read first or last**, and specifically put "not covered" at the end. A
gaps section in the middle reads as covered.

**A facts block is cheap and almost nobody writes one.** A short verbatim list of values
that must survive, carried separately from the prose.

**"Let me just try one thing first" after someone asks for a human is the named wrong
answer.** It feels like service and it is the anti-pattern.

**Sentiment escalation misroutes in both directions.** A calm person with an impossible
problem never escalates; a frustrated person with a trivial one always does.

**A policy gap is not a hard case.** The guide says explicitly *not just complex cases* —
the trigger is that no policy covers it, regardless of difficulty.

**Asking for a clarifying identifier is cheaper than being wrong once**, and heuristic
selection among multiple matches is named.

**"Returning empty results as success" is the failure you will actually ship**, because an
empty list is what you get when nobody decides.

**`alternatives_not_tried` is the field nobody includes and the coordinator most wants.**

**A report with no "gaps" section is claiming complete coverage whether you meant to or
not.**

**"Typically" is the tell.** When the session starts describing what such a class usually
looks like, the specific knowledge is gone and nothing announced it.

**Write the scratchpad as you discover, not at the end.** At the end you are writing from
the same degraded context you are trying to escape.

**Summarise before spawning the next phase, not after finishing.**

**Sample the high-confidence batch, not the low one.** The high-confidence population is the
one you were about to stop checking, which is exactly why it needs checking.

**A confidence score is a word until it is calibrated** against labelled data. Until then it
is the model's guess about its own guess.

**Report the denominator with every rate.** An aggregate accuracy figure is a claim about a
population you have not described.

**A segment can override a confidence score, and usually should.** If one document type is
measurably worse, route on the type regardless of what the score says.

**Re-measure after changing the prompt.** A calibration is a property of one prompt on one
population, and editing the prompt invalidates it silently.

---

## Post-production checklist

- [ ] Watch the full take at full screen. No internal paths, nothing in the window title or
      tab bar.
- [ ] The "typically" degradation is described, not staged. A faked instance would be the
      one dishonest thing in the series.
- [ ] **No calibration figure is quoted for this lab.** There is no labelled validation set,
      so there is nothing to calibrate against, and the episode says so.
- [ ] The series-close limitations paragraph is intact — no practice questions, no pass-rate
      claim, the self-review admission, and the 5-of-13 verification figure.
- [ ] **The 5-of-13 figure matches `VERIFICATION.md` at the time of recording.** If more
      pages have been re-verified by then, update the spoken number. This is the one figure
      in the series that goes stale.
- [ ] **The anti-pattern total is "more than forty", and that wording is deliberate.**
      Counted 2026-10-18 from the slide bodies: 4 + 7 + 10 + 11 + 15 = 47, but three items
      are named by the guide in two domains each and so appear on two decks — about 44
      distinct. "More than forty" is true under either count. An earlier draft of this
      script said "well over fifty", which was simply wrong and was caught only by
      counting. If you re-cut any anti-pattern slide, re-count before you speak a number.
- [ ] No "next episode" line. This is the close.
- [ ] Clean clone at this episode's commit reproduces the finished lab and the tests.
- [ ] Description carries the repo link with the `julie-elkins` handle.
