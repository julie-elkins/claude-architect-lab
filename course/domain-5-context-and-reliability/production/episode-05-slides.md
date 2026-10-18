> **Production asset, not the lesson.** Slide bodies for the video version.
> The written lessons are listed on [the course front page](../../../README.md).

# Episode 5 slides — What a 97% hides

One `## Slide N` per slide, plain text body lines, speaker notes as a blockquote underneath.

**Slide body text is deliberately plain — no asterisks, no hashes, no pipes.** Those arrive as
literal punctuation when pasted into Keynote or Google Slides and then have to be stripped by
hand. Copy a slide's body lines straight across.

14 slides for a 7–8 minute episode — the shortest in the series, because Domain 5 is 15%.
Slides 4 through 11 are the build; the screen recording carries those, so the slide is a title
card the viewer can pause on, not a wall of text.

**Chapter markers go at slides 4, 6, 8, 9 and 10** — one per task statement.

**This deck ends the series.** Slides 13 and 14 have no counterpart in episodes 1 to 4 and
there is no "next episode" slide. Do not add one.

---

## Slide 1

Build to Pass
Claude Certified Architect – Foundations

Episode 5 of 5
Context Management and Reliability

**Speaker notes:**

> Cold open is the script's first line — "ninety-seven percent is a number that stops
> questions" — not this slide. Hold about two seconds.
> Do not say "welcome back", and do not say "finally". A viewer landing from search on the
> last episode has seen none of the others.

---

## Slide 2

Domain 5 — Context Management and Reliability

15% of the exam

Domain 1  Agentic Architecture and Orchestration     27%
Domain 3  Claude Code Configuration and Workflows     20%
Domain 4  Prompt Engineering and Structured Output    20%
Domain 2  Tool Design and MCP Integration             18%
Domain 5  Context Management and Reliability          15%

**Speaker notes:**

> Weights are from exam guide section 4. Highlight Domain 5's row only.
> FIFTH and final appearance, identical except the lit row. By now the viewer knows the
> blueprint. That was the point of keeping it identical, and it is worth one sentence here —
> the only episode where you get to say so.

---

## Slide 3

Five task statements in this domain

Conversation context preservation
Escalation and ambiguity resolution
Error propagation across agents
Large codebase exploration
Human review and confidence calibration

The smallest domain
And the one that decides whether
anything else was real

**Speaker notes:**

> Exam guide section 6, task statements 5.1 through 5.5.
> The last three lines point at TS 5.5. It is a genuine hook and it is also true.
> Screen recording starts after this slide.

---

## Slide 4

TS 5.1 — Two failures invisible while they happen

Summarisation that condenses
numerical values, percentages, dates
and stated expectations into vague summaries

The customer discussed a refund

That lost the amount, the date, the order number
And it reads perfectly well

**Speaker notes:**

> CHAPTER MARKER.
> Exam guide section 6, task statement 5.1. The example sentence is the whole point: fluency
> is not a check on information loss.
> The fix is a facts block — a short verbatim list of values that must survive, carried
> separately from the prose. Cheap, and almost nobody writes one.

---

## Slide 5

The positional failure

Models reliably process information
at the beginning and end of long inputs
but may omit findings from middle sections

So position is a design decision

Put what must be read first or last

Put "not covered" at the END
A gaps section in the middle reads as covered

**Speaker notes:**

> Close to the guide's own wording — quote it as theirs.
> The "not covered" placement advice is the author's application of it, and it is the single
> most useful thing on this slide. Say which is which.
> Also: trim tool output at the boundary, not when context gets tight. The guide's example is
> 40+ fields per lookup when 5 are relevant.

---

## Slide 6

TS 5.2 — Real triggers, and the popular wrong ones

Legitimate
An explicit request for a human
A policy exception or gap, not just complex cases
Inability to make meaningful progress

Unreliable, in the guide's words
Sentiment-based escalation
Self-reported confidence scores

Both are the obvious implementations

**Speaker notes:**

> CHAPTER MARKER.
> "Not just complex cases" is the guide's own qualifier and it is doing real work — a policy
> gap is not the same as a hard case.
> Sentiment misroutes in BOTH directions: a calm person with an impossible problem never
> escalates; a frustrated person with a trivial one always does.

---

## Slide 7

The rule that inverts an instinct

Honour an explicit request for a human
IMMEDIATELY

Without first attempting investigation

Let me just try one thing first
is the named wrong answer

**Speaker notes:**

> This is the sharpest single rule in the domain. Hold it.
> Say why it is hard: the helpful instinct and the correct behaviour point in opposite
> directions, which is exactly what makes it a good exam item.
> Also from 5.2: heuristic selection among multiple matches is named — ask for another
> identifier instead.

---

## Slide 8

TS 5.3 — Two anti-patterns, opposite directions

Silently suppressing errors
Returning empty results as success

Terminating an entire workflow
on a single failure

Both are named
So the answer is neither extreme

Recover locally
Propagate what you cannot resolve, with context
Never let a failure render as a clean result

**Speaker notes:**

> CHAPTER MARKER.
> The guide names both IN THE SAME BREATH — that is what tells you the answer is the middle.
> Suppression is the one you will actually ship, because an empty list is what you get when
> nobody decides. Say that.
> Two fields that pay for themselves: what was attempted, and what alternatives were not
> tried. The second is the one nobody includes.

---

## Slide 9

TS 5.4 — The diagnostic you can use today

In extended sessions, models start
giving inconsistent answers and referencing
typical patterns rather than the specific
classes discovered earlier

Typically is the tell

Nothing announces it
The answers stay fluent and become generic

**Speaker notes:**

> CHAPTER MARKER.
> Close to the guide's own wording for this task statement — the most useful sentence in it.
> DO NOT STAGE A FAKE INSTANCE of this. It takes an extended session to appear and a faked
> one would be the only dishonest thing in the series. Describe it.
> Remedies are all "get findings out of the conversation": scratchpad files, subagent
> delegation, summarise between phases, structured state export for crash recovery.

---

## Slide 10

TS 5.5 — What the headline hides

97% overall

May mask poor performance
on specific document types or fields

97% overall
and 60% on one document type
that is a fifth of your volume

Nothing about the headline says so

**Speaker notes:**

> CHAPTER MARKER.
> The 97% is the guide's own example figure — attribute it.
> The 60%-on-a-fifth illustration is the author's, constructed to show the arithmetic. Say
> which is which; inventing a plausible figure and letting it sound sourced is the failure
> this episode is about.
> "A number that stops questions" is the framing from the cold open. Call back to it.

---

## Slide 11

Three remedies, and they are a measurement programme

Stratified random sampling
Sample the HIGH-confidence population

Accuracy by document type and by field
Not in aggregate

Field-level confidence calibrated
against a labelled validation set
BEFORE reducing human review

**Speaker notes:**

> All three are the guide's. "Before" is the word that matters and it is worth stressing out
> loud.
> Sampling the high-confidence batch is counterintuitive and correct: it is the population
> you were about to stop checking.
> DO NOT quote a calibration figure for this lab. There is no labelled validation set for
> Course Doctor, so there is nothing to calibrate against — and saying so is this episode's
> own lesson applied to itself.

---

## Slide 12

The anti-patterns for this domain

Summarisation condensing numbers, dates, expectations
Tool results accumulating out of proportion
Treating a long input as uniformly attended
Sentiment-based escalation
Self-reported confidence as a complexity proxy
Investigating before honouring a request for a human
Heuristic selection among multiple matches
Suppressing errors as empty success
Terminating a workflow on one failure
A generic error status that hides context
Letting a session degrade to typical patterns
Exploring in the main context when a subagent could isolate it
Relying on an aggregate accuracy metric
Reducing human review before validating by segment
Routing on uncalibrated confidence

**Speaker notes:**

> Fifteen items — the longest single list in the series. Do not rush it.
> Fifth and final appearance of the anti-pattern slide. This is the course's differentiator.
> Note for the edit: two of these — suppressing errors and terminating on one failure — also
> appeared on episode 2's deck, because the guide names them under both 2.2 and 5.3. That is
> correct, not a duplication error.

---

## Slide 13

One idea, examined from five directions

A cap that reads as a design
A tool list that reads as what the worker has
A populated server list that reads as working
A restored transcript that reads as current
A schema-valid document that reads as correct
An empty result that reads as success
A broken hook that reads as a control
A 97% that reads as good enough

Every one looks right and quietly isn't

**Speaker notes:**

> THIS IS THE SLIDE THE WHOLE SERIES WAS BUILT TOWARD. Give it the time.
> Each line is one domain's instance of the same failure. Do not explain them again — the
> viewer has seen all eight. Just read them and let the pattern land.
> More than forty anti-patterns across five episodes, nearly all named in the guide. COUNTED:
> 47 on the slides, about 44 distinct. Do not say "over fifty" — an earlier draft did and it
> was wrong.

---

## Slide 14

What this course does not do

No practice questions
The exam guide publishes sample items
with full rationales

No pass-rate claim
I do not have that data

The lessons were written by an agent
and checked by the same agent
VERIFICATION.md records which pages were
re-verified word for word, and which were not

Sourced from the published exam guide
and public documentation only
Nothing from sitting the exam

github.com/julie-elkins/claude-architect-lab

**Speaker notes:**

> SERIES CLOSE. No "next episode" slide. Do not add one, and do not soften this into a call
> to action — the limitations ARE the ending, and they are the most credible thing in the
> series.
> Update the spoken verification figure to match VERIFICATION.md at the time of recording.
> It was 5 of 13 on 2026-10-18 and it is the one number in the series that goes stale.
> A course about content freshness that did not say this would be the anti-pattern. That is
> the last line before "good luck".
> Check the handle in the URL before export. The bare old handle 404s.
