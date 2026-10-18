> **Production asset, not the lesson.** Slide bodies for the video version.
> The written lessons are listed on [the course front page](../../../README.md).

# Episode 3 slides — The loop, the coordinator, and what a subagent does not know

One `## Slide N` per slide, plain text body lines, speaker notes as a blockquote underneath.

**Slide body text is deliberately plain — no asterisks, no hashes, no pipes.** Those arrive as
literal punctuation when pasted into Keynote or Google Slides and then have to be stripped by
hand. Copy a slide's body lines straight across.

20 slides for a 13–14 minute episode — the longest in the series, because Domain 1 is 27%.
Slides 4 through 18 are the build; the screen recording carries those, so the slide is a title
card the viewer can pause on, not a wall of text.

**Chapter markers go at slides 4, 8, 10, 13, 15 and 17** — one per task statement boundary. At
this runtime that is navigation, not polish.

---

## Slide 1

Build to Pass
Claude Certified Architect – Foundations

Episode 3 of 5
Agentic Architecture and Orchestration

**Speaker notes:**

> Cold open is the first line of the script — "this is the biggest domain on the exam" — not
> this slide. Hold this one about two seconds.
> Do not say "welcome back". A viewer landing from search has not seen episodes 1 or 2.

---

## Slide 2

Domain 1 — Agentic Architecture and Orchestration

27% of the exam

Domain 1  Agentic Architecture and Orchestration     27%
Domain 3  Claude Code Configuration and Workflows     20%
Domain 4  Prompt Engineering and Structured Output    20%
Domain 2  Tool Design and MCP Integration             18%
Domain 5  Context Management and Reliability          15%

**Speaker notes:**

> Weights are from exam guide section 4. Highlight Domain 1's row only.
> IDENTICAL to episodes 1 and 2 except which row is lit. Third time the viewer has seen it;
> by episode 5 they have the blueprint memorised without having been asked to.
> This is the episode where the highlighted row is also the top row — worth a beat.

---

## Slide 3

Seven task statements in this domain

Agentic loops and termination
Coordinator and subagent orchestration
Subagent invocation and context passing
Multi-step enforcement and handoff
Agent SDK hooks
Task decomposition strategy
Session state, resumption and forking

All seven in this episode

**Speaker notes:**

> Exam guide section 6, task statements 1.1 through 1.7, titles paraphrased to fit.
> Say that this is the longest episode and that there are chapter markers. Give the viewer
> permission to come back to one rather than abandoning the whole thing.

---

## Slide 4

TS 1.1 — One iteration of the loop

Send a request
Get back tool calls, or a final answer
Run the tools
Feed the results back
Repeat

Turns continue until the model produces
output with no tool calls

**Speaker notes:**

> CHAPTER MARKER.
> The last two lines are the documented termination condition — agent loop docs, cited in
> lesson 1.1. Quote it as documented, not as a design opinion.
> Screen recording starts after this slide.

---

## Slide 5

The guide names three wrong answers

Parsing natural language to decide the loop ended

An arbitrary iteration cap as the
primary stopping mechanism

Checking whether assistant text exists
as a completion indicator

A published list of wrong answers
is a published list of distractors

**Speaker notes:**

> Exam guide section 6, task statement 1.1. This is the most specific anti-pattern list in
> the whole guide and it is the reason this episode opens here.
> All three are things a competent engineer actually does. Say that — it is why they work as
> distractors.
> Hold this slide. It is the single highest-value thing in the episode.

---

## Slide 6

All three are the same mistake

Reading something soft
when a hard signal is available

A model can emit text AND tool calls
in the same response

So a loop that stops at text
stops in the middle of the work

And it does it intermittently

**Speaker notes:**

> The intermittent point is the one to land. Consistent failure gets debugged; intermittent
> failure gets blamed on the model.
> The hard signal is stop_reason — tool_use versus end_turn. Name it here.

---

## Slide 7

You still need a cap

Primary versus backstop

max_turns          error_max_turns
max_budget_usd     error_max_budget_usd

Check the subtype before the text
The text is only present on success

Budget caps overshoot by design
Spend is checked after a response arrives

**Speaker notes:**

> If runs routinely end at the cap, you do not have a bound — you have a timeout dressed as
> a design. That sentence is the takeaway.
> The overshoot is documented, not a bug: the cost is only known once the response exists.
> Say "leave headroom."

---

## Slide 8

TS 1.2 — Hub and spoke, specified by the guide

A coordinator manages all of it
Communication between subagents
Error handling
Information routing

Workers do not talk to each other

What routing through the coordinator buys
Observability
Consistent error handling
Controlled information flow

**Speaker notes:**

> CHAPTER MARKER.
> The guide SPECIFIES this architecture rather than leaving it open — say so.
> The three benefits are the reason the rule exists and they are worth more than the rule.
> Land the loss: you lose all three silently. The system still works; you just cannot see
> what it did.

---

## Slide 9

The examinable judgment

A coordinator that always runs
the full pipeline is not coordinating

Choosing which subagents a request needs
is the coordinator's defining job

So when one option adds a routing decision
and another adds a worker
the routing decision is usually the answer

And the guide names the opposite failure too
Overly narrow decomposition
Six narrow workers reporting success
can cover less than two broad ones

**Speaker notes:**

> The exam-shape prediction is worth saying out loud — viewers remember predictions.
> The narrow-decomposition failure is the counterintuitive one: the coordinator can be too
> good at splitting, and every individual report comes back clean.

---

## Slide 10

TS 1.3 — The fact everything follows from

Subagent context must be provided
explicitly in the prompt

Subagents do not inherit parent context
and do not share memory between invocations

Write the worker's prompt as though
it has never met you

Because it hasn't

**Speaker notes:**

> CHAPTER MARKER.
> "Review the lesson we just discussed" has told the worker nothing. The worker has no
> "just" — and it will not ask, it will confidently invent a subject.
> Pass findings, not references to findings.

---

## Slide 11

Two ways a granted tool disappears anyway

Background subagents
Claude Code removes every other built-in tool
whether inherited OR listed in the tools field

Nesting
Depth limit, three layers by default
The spawning tool is removed at it

Nothing about the definition says so

**Speaker notes:**

> The background sentence is quoted verbatim from the sub-agents docs and was re-verified
> word for word on 2026-10-18. Say it is documented, because it sounds like a bug.
> The nesting symptom is the tell: a worker that was supposed to delegate does the work
> itself instead.

---

## Slide 12

A naming discrepancy — hold both halves

The exam guide says        Task
The documentation says     Agent

There is no Task row in the tools reference

The requirement is true under either name
A coordinator cannot spawn workers unless
the spawning tool is in its allowed list

Exam item says Task, answer the guide
Configuring a real project, the docs win

**Speaker notes:**

> Do NOT resolve this in favour of one name. The guide says Task in two places — task
> statement 1.3 and the section 17 appendix — so it is deliberate, not a slip.
> Close with: a permission rule naming a tool that does not exist is not an error, it is
> silently inert. Same family as everything else in this course.

---

## Slide 13

TS 1.4 and 1.5 — one sentence governs both

When deterministic compliance is required
prompt instructions alone
have a non-zero failure rate

The guide's example
Identity verification before a financial operation

A rule that holds 99% of the time
is not a prerequisite
It is a tendency

**Speaker notes:**

> CHAPTER MARKER. These two task statements share this sentence, which is why they are one
> segment.
> This is the single most load-bearing quotation in the exam guide and it decides a whole
> family of items. ATTRIBUTE IT — it is the guide's claim, not a measurement made here.
> "Non-zero is the whole problem" is the line.

---

## Slide 14

Hooks give deterministic guarantees
Prompts give probabilistic compliance

Two named uses

Interception    block a tool call that violates policy
Normalisation   transform a result before the model sees it

The exam item writes itself
One option strengthens the prompt
One adds a hook or a gate

The mechanism wins

**Speaker notes:**

> Both named uses are from task statement 1.5's objectives.
> Also cover handoff from 1.4 here if time allows: you are escalating to humans who lack
> the conversation transcript, so whatever they need must be IN the handoff. If the episode
> runs long, this is the first thing to cut — it is in the written lesson.

---

## Slide 15

The hook default that makes one useless

Missing script, timeout, cannot start,
or exit non-zero other than 2

Documented default — non-blocking error
The action proceeds

So a broken hook is not a control
It is a comment

The fix is one key
onFailure: block

Requires a recent Claude Code
On an older build it is IGNORED, not rejected

**Speaker notes:**

> CHAPTER MARKER.
> Verbatim-verified against the hooks docs on 2026-10-18, including the version floor
> (v2.1.295 or later).
> The version caveat is this episode's own failure mode one level deeper: the fix for
> fail-open is itself fail-open on an older install, and the config still READS as enforced.
> Do not cut this. It is the most practically useful thirty seconds in the episode.
> Add: PostToolUse cannot prevent anything. By then the call has run.

---

## Slide 16

TS 1.6 — Chain it, or plan it

The discriminator is predictability

Steps knowable before you start        chain
Next step depends on the last finding  plan

A comprehensive review of four known aspects
is a chain

Add tests to a legacy codebase
is not

**Speaker notes:**

> The exam stem will tell you which. Point that out — it is a reading skill, not a
> judgement call, once you know to look for it.
> Both mismatches are named by the guide: planning a known sequence wastes a step, and a
> fixed pipeline for an open-ended investigation was written before anyone knew the shape.

---

## Slide 17

The pattern worth memorising

Per-item local passes
Then a separate cross-item integration pass

One pass asked to do both
reliably does neither well

The guide's name for the cost
Attention dilution

**Speaker notes:**

> CHAPTER MARKER.
> Attention dilution is the guide's term — attribute it. It is not demonstrable in this
> episode and must not be presented as measured here.
> The cross-cutting pass wants summaries, not sources. That is in the written lesson.

---

## Slide 18

TS 1.7 — What a resume restores

Everything
Including file contents read
before you changed the files

A transcript is a record of what WAS true

Nothing about restoring it
marks which parts have expired

A new session with a structured summary
is more reliable than resuming stale tool results

**Speaker notes:**

> The last two lines are close to the guide's own wording for this task statement. It is a
> CORRECTNESS question, not a mechanics question — say that.
> Forking is the other half: you have paid for an analysis once and want two conclusions off
> one shared baseline.

---

## Slide 19

The anti-patterns — the longest list in the guide

Natural language for termination
An arbitrary cap as the primary mechanism
Assistant text as a completion indicator
Subagent communication bypassing the coordinator
Always routing through the full pipeline
Overly narrow decomposition
Assuming a subagent inherits parent context
Prompt instructions where compliance must be guaranteed
A single large review pass
Resuming with stale tool results

Most are the same shape underneath
Something that looks correct and quietly isn't

**Speaker notes:**

> This slide is the course's differentiator and it recurs in all five episodes. Do not rush
> it — ten items needs a slow read, and it is worth the thirty seconds.
> All ten are the guide's, from Domain 1's objectives. Here you can say "the guide names
> these" without qualification, unlike episode 1 where two of four were the author's.
> Close on the pattern: a cap that reads as a design, a tool list that reads as what the
> worker has, a restored transcript that reads as current, an instruction that reads as a
> guarantee. That is most of this exam.

---

## Slide 20

Next: Domain 4, prompt engineering and structured output

20% of the exam
JSON schemas that cannot be violated
And the three places that guarantee stops

Sourced from the published exam guide
and public documentation only

Every claim traced in SOURCES.md
Verification state in VERIFICATION.md
Nothing from sitting the exam

github.com/julie-elkins/claude-architect-lab

**Speaker notes:**

> The sourcing statement goes on screen in every episode. A viewer arriving here from search
> needs it, and scrolling back is not a thing they will do.
> VERIFICATION.md says what has NOT been checked — the differentiator for a course about
> content freshness. Name it.
> Check the handle in the URL before export. The bare old handle 404s.
