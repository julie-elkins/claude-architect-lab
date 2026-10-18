> **Production asset, not the lesson.** Slide bodies for the video version.
> The written lessons are listed on [the course front page](../../../README.md).

# Episode 4 slides — Wording strength is not a mechanism

One `## Slide N` per slide, plain text body lines, speaker notes as a blockquote underneath.

**Slide body text is deliberately plain — no asterisks, no hashes, no pipes.** Those arrive as
literal punctuation when pasted into Keynote or Google Slides and then have to be stripped by
hand. Copy a slide's body lines straight across.

17 slides for a 10–11 minute episode. Slides 4 through 15 are the build; the screen recording
carries those, so the slide is a title card the viewer can pause on, not a wall of text.

**Chapter markers go at slides 4, 6, 8, 11, 12 and 14** — one per task statement.

---

## Slide 1

Build to Pass
Claude Certified Architect – Foundations

Episode 4 of 5
Prompt Engineering and Structured Output

**Speaker notes:**

> Cold open is the script's first line — "be more careful is not an engineering change" —
> not this slide. Hold about two seconds.
> Do not say "welcome back". A viewer landing from search has seen none of this.

---

## Slide 2

Domain 4 — Prompt Engineering and Structured Output

20% of the exam

Domain 1  Agentic Architecture and Orchestration     27%
Domain 3  Claude Code Configuration and Workflows     20%
Domain 4  Prompt Engineering and Structured Output    20%
Domain 2  Tool Design and MCP Integration             18%
Domain 5  Context Management and Reliability          15%

**Speaker notes:**

> Weights are from exam guide section 4. Highlight Domain 4's row only.
> Fourth appearance, identical except the lit row. Do not re-order.

---

## Slide 3

One thesis runs through all six task statements

Wording strength is not a mechanism

Every task statement gives you a pair
A tempting option that makes the instruction firmer
A correct option that changes the structure

**Speaker notes:**

> This is the framing slide for the whole episode and the most useful thing in it. Say that
> once you see the pattern you can answer most of this domain from it.
> Six task statements, all six today. Screen recording starts after this slide.

---

## Slide 4

TS 4.1 — The guide names the failing instruction

Be conservative

Only report high-confidence findings

Both fail to improve precision
compared to specific categorical criteria

High confidence is not a property
the model can calibrate on request
It is a word

**Speaker notes:**

> CHAPTER MARKER.
> Exam guide section 6, task statement 4.1. The guide QUOTES these failing instructions,
> which is unusual and worth pointing out — it is handing you distractor wording.
> ATTRIBUTE the claim. It is the guide's, not measured here.

---

## Slide 5

The guide's own contrast

Weak
Check that comments are accurate

Strong
Flag comments only when claimed behaviour
contradicts actual code behaviour

The first is a hope
The second is a test

If your fix to a precision problem
is an adverb, it is not a fix

**Speaker notes:**

> Both phrasings are the guide's. Use theirs so a viewer who reads the guide recognises them.
> "You can apply it and get the same answer twice" is the definition of a criterion — say it.
> Add: write the skip list, not just the report list. It is half as likely to get written.

---

## Slide 6

TS 4.2 — The claim is unqualified

Few-shot examples are the most effective technique
for consistently formatted, actionable output
when detailed instructions alone
produce inconsistent results

The domain's thesis, in two halves
Criterion vague          define it
Output still inconsistent  show examples

Neither is fixed by stronger wording

**Speaker notes:**

> CHAPTER MARKER.
> Exam guide section 6, task statement 4.2. ATTRIBUTE — "most effective technique" is their
> claim and a strong one.
> The two-halves framing ties 4.1 and 4.2 together and is worth the extra beat.

---

## Slide 7

Which examples, specifically

Ones that demonstrate ambiguous-case handling

Ones that generalise to novel patterns
rather than matching only the cases you listed

Two examples teach matching
The third teaches generalising

The guide's number is 2 to 4
Not twenty

**Speaker notes:**

> The 2–4 figure is the guide's and it is quotable. People reach for twenty examples and get
> rigid copying.
> Put the reasoning INSIDE the example: one showing the verdict teaches format, one showing
> why teaches judgment.

---

## Slide 8

TS 4.3 — Guaranteed, and then the limit

Tool use with JSON schemas is the most reliable
approach for schema-compliant output
It eliminates JSON syntax errors

Strict schemas do NOT prevent semantic errors

Line items that do not sum to the total
Values in the wrong fields

A perfectly valid document that is wrong

**Speaker notes:**

> CHAPTER MARKER.
> The limit is the MORE examinable half — say so explicitly. Treating schema compliance as
> correctness is the named anti-pattern.
> "Structure reads as rigour" is the sentence that makes it stick: a schema-valid document
> looks more trustworthy than prose and has no more claim to being right.
> The cheapest guard is the guide's own — calculated total beside stated total.

---

## Slide 9

Where the guarantee stops

Refusal        stop_reason refusal
Truncation     stop_reason max_tokens
Enum casing    may differ on the first letter after a space

Check stop_reason before you parse
Compare enums case-insensitively

**Speaker notes:**

> All three are documented as expected behaviour, not bugs — structured outputs docs,
> re-verified 2026-10-18.
> Two lines of code. Without them the guarantee has three holes.

---

## Slide 10

The guide and the API documentation disagree

Guide        make fields optional when the source
             may not contain the information
API docs     reduce optional parameters

Both are right about different things
One prevents fabrication
One manages grammar complexity

The reconciliation
A required field with an explicit
not-present member — an enum with unclear

**Speaker notes:**

> Do NOT resolve this in favour of one. For an exam item, answer the guide. For a real
> schema, prefer required fields with explicit absent-values.
> The reconciliation is the guide's OWN other objective, which is what makes it safe to
> teach as the answer rather than as an opinion.
> The model must answer, and "unclear" is an answer you can count.

---

## Slide 11

TS 4.4 — The judgment is whether, not how

Retries are ineffective when the required information
is simply absent from the source

Format errors        respond to a retry
Structural errors    respond to a retry
A missing fact       does not

Three attempts at a figure that is not there
produce three failures and a bill

**Speaker notes:**

> CHAPTER MARKER.
> Exam guide section 6, task statement 4.4, stated directly. This is the thing people get
> wrong.
> Then the mechanism that makes a retry worth anything: retry WITH error feedback — append
> the specific validation errors so the second attempt is informed rather than repeated.
> And say "change nothing else", or the retry rewrites what already worked.

---

## Slide 12

TS 4.5 — Three numbers and one prohibition

50% cost saving
Up to a 24-hour window
No guaranteed latency

Blocking workflows cannot use it
A gate that might answer tomorrow is not a gate

Non-blocking, latency-tolerant work should
Overnight reports, weekly audits

**Speaker notes:**

> CHAPTER MARKER.
> The pre-merge check is the guide's own example and the failure is definitional — say it
> that way.
> This segment cannot be demonstrated live. Show a submission and a previously completed
> result and SAY they are two runs.

---

## Slide 13

The arithmetic you can be asked to do

Guarantee a 30-hour SLA
Batch processing takes up to 24 hours

Submit every 4 hours

24 + 4 = 28, inside 30 with margin

A cadence picked by feel meets the SLA
until the first slow day

**Speaker notes:**

> The 4-hour / 30-hour figures are the guide's worked example. Show the arithmetic on screen
> rather than asserting the answer — this is the one place in the series with a calculation
> in it.
> Two practical notes: self-describing custom_id, and resubmit the failed IDs rather than the
> whole batch.

---

## Slide 14

TS 4.6 — The author is the worst reviewer

A model retains reasoning context from generation
making it less likely to question its own decisions
in the same session

So the review inherits the assumptions
rather than testing them

Ranked by the guide
Independent instance, no prior context   strongest
Self-review instruction                  weaker
Extended thinking                        weaker

**Speaker notes:**

> CHAPTER MARKER.
> This is a MECHANISM, not an opinion — "models are overconfident" is the weaker version and
> is not what the guide says. Being able to state the mechanism is the examinable part.
> Both weaker options are the tempting ones, and the guide names both.

---

## Slide 15

Where this course does it to itself

The claims in these lessons were written by an agent

They were checked by the same agent

That is the configuration this task statement
calls the weakest

The partial defence
Demand the documentation's verbatim wording back
rather than a judgment

Written down in VERIFICATION.md
with what it still cannot tell you

**Speaker notes:**

> KEEP THIS SLIDE. It is the most credible thirty seconds in the series and the obvious thing
> to cut for time, which is why this note exists.
> Weaker than independent review, stronger than self-assessment. Say both halves — claiming
> it is as good as independent review would be exactly the failure the slide is about.
> Close: "review your own output carefully" is an instruction to the one party that cannot.

---

## Slide 16

The anti-patterns, from the exam guide

Be conservative as a precision fix
Confidence filtering instead of a report-versus-skip list
Detailed instructions where examples are needed
Examples covering only the cases you listed
Treating schema compliance as correctness
Required fields where the source may not have the information
Retrying when the fact is absent
A retry without the validation errors appended
Batch processing a blocking workflow
Resubmitting a whole batch to recover failures
Self-review in the generating session

Count how many are the firmer-wording option

**Speaker notes:**

> This slide is the course's differentiator and it recurs in all five episodes. Do not rush
> eleven items.
> The closing observation is the episode's thesis returning: when one choice rewrites the
> instruction and another changes the structure, the structure wins.

---

## Slide 17

Last episode: Domain 5

15% of the exam
Context management and reliability
And the task statement that decides
whether anything else was real

Sourced from the published exam guide
and public documentation only

Every claim traced in SOURCES.md
Verification state in VERIFICATION.md
Nothing from sitting the exam

github.com/julie-elkins/claude-architect-lab

**Speaker notes:**

> The sourcing statement goes on screen in every episode.
> "Whether anything else was real" is about TS 5.5 — aggregate accuracy hiding a bad segment.
> It is a genuine hook and it is also true.
> Check the handle in the URL before export. The bare old handle 404s.
