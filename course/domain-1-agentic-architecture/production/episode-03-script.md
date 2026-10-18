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
> task statements 1.1 through 1.7:
> [1.1](../lesson-1-1-agentic-loops.md) ·
> [1.2](../lesson-1-2-coordinator-patterns.md) ·
> [1.3](../lesson-1-3-subagent-invocation.md) ·
> [1.4](../lesson-1-4-enforcement-and-handoff.md) ·
> [1.5](../lesson-1-5-hooks.md) ·
> [1.6](../lesson-1-6-task-decomposition.md) ·
> [1.7](../lesson-1-7-session-state.md)

# Episode 3 — The loop, the coordinator, and what a subagent does not know

**Domain 1: Agentic Architecture & Orchestration — 27% of CCAR-F**
Target runtime 13–14 minutes · ~2,000 spoken words
Ships: Course Doctor's coordinator, one worker per lesson, bounded by something other than
a guess

**This is the longest episode in the series and that is deliberate.** Runtime is
proportional to blueprint weight — 27% here against Domain 5's 15% — which is what lets
this episode cover all seven task statements instead of leaving three on the floor.

---

## Before you record

- Clean recording profile, per the recording checklist kept outside this repo.
- **Start from episode 2's commit.** The tool surface has to exist before the loop that
  calls it.
- **Budget a second take for the fan-out.** Parallel spawning has to be one response rather
  than several turns, and the difference is invisible in the transcript afterwards — so if
  the first take serialises, you cannot fix it in the edit.
- **Two things in this episode are claims, not demonstrations.** The non-zero failure rate
  of prompt instructions, and the attention dilution of a single large review pass. Both are
  the guide's. Say so out loud; neither is measurable in thirteen minutes.
- At 13–14 minutes this runs past the length where completion rates fall. **Put a chapter
  marker at each task statement** so the viewer can navigate rather than abandon.

---

## Fundamentals

Not spoken on camera. For the written lesson and the episode description.

**The agentic loop.** Send a request, get back either tool calls or a final answer, run the
tools, feed the results back, repeat. *Why it matters here:* it is the subject of the
domain. *Depth:* `/docs/en/how-claude-code-works`.

**`stop_reason`.** A field on the model's response saying why it stopped generating. *Why
it matters here:* it is the structural signal to branch on instead of reading the prose.
*Depth:* the Messages API documentation.

**Hub-and-spoke.** A topology where every message goes through a central node. *Why it
matters here:* the guide specifies it for multi-agent work, and the reason is
observability. *Depth:* any network topology primer.

**Process isolation.** Separate execution with separate state. *Why it matters here:* a
subagent is an isolated context — the whole point and the whole hazard. *Depth:* any
treatment of process boundaries.

**Partial failure.** Some components succeed and some do not. *Why it matters here:* it is
the normal state of a fan-out, and the join has to say which. *Depth:* any distributed
systems text; this is the oldest problem here wearing a new name.

**Idempotence.** Whether repeating an operation is safe. *Why it matters here:* it decides
whether a loop may retry, and whether a resumed tool already took effect. *Depth:* REST
method semantics.

**Determinism versus probability.** Whether an outcome is guaranteed or merely likely.
*Why it matters here:* it is the single distinction that decides the largest family of
items in this exam. *Depth:* lessons 1.4 and 1.5.

---

## Script

```
This is the biggest domain on the exam. Twenty-seven percent.

[screen: the blueprint table, Domain 1 highlighted]

And it does something unusual. In the first task statement, the exam guide names
three wrong answers. In writing. Explicitly.

So let's start there, because a published list of wrong answers is a published
list of distractors.

[screen: the seven task statements]

Seven task statements. We are doing all seven, which is why this episode is
longer than the others. There are chapter markers if you want to come back to one.

[screen: the loop, four turns]

Task statement one point one. The agentic loop.

Here is one iteration. You send a request. The model comes back with either tool
calls or a final answer. If there are tool calls, you run them, feed the results
back, and go round again.

And the documented termination is exactly this: turns continue until the model
produces output with no tool calls. That is the condition. Tool calls present,
keep going. No tool calls, you are done.

At the API level that is what stop_reason carries. tool_use means it wants a tool
run. end_turn means it has finished.

[screen: the three named anti-patterns]

Now the three wrong answers the guide names.

One: parsing natural language to decide the loop has ended. Two: using an
arbitrary iteration cap as the primary stopping mechanism. Three: checking whether
assistant text exists as a completion indicator.

All three are things a competent engineer actually does. That is what makes them
good distractors.

And they are all the same mistake — reading something soft when a hard signal is
available.

The third one is the subtlest, so let me be specific. A model can produce text
and tool calls in the same response. So if your loop stops when it sees text, it
stops in the middle of the work. And it does that intermittently, on the turn
where the model happens to narrate while calling something.

[screen: max_turns and max_budget_usd]

You still need a cap. The distinction the guide draws is primary versus backstop.

Keep the cap. Just don't let it be the thing that normally ends your run,
because if runs routinely end at the cap, you don't have a bound — you have a
timeout dressed up as a design.

And when a documented bound fires, you get a named result. error_max_turns.
error_max_budget_usd.

Two things about that worth knowing. Check the result subtype before you read the
result text, because the text is only there on success — so code that reads it
unconditionally gets an empty string on exactly the runs you most need to
diagnose. And budget caps can overshoot by design, because spend is compared
against the cap after a response arrives. That is when its cost is known. Leave
headroom.

[screen: hub and spoke diagram]

One point two. The coordinator.

The guide specifies the architecture rather than leaving it to you: hub and
spoke. A coordinator manages all communication between subagents, all error
handling, all information routing. Workers do not talk to each other.

And it gives a reason that is worth more than the rule. Routing everything
through the coordinator buys you three things: observability, consistent error
handling, and controlled information flow.

Those are the three things you lose the moment two workers start exchanging
results directly. And you lose them silently. The system still works. You just
can't see what it did any more.

[screen: a coordinator selecting two of five workers]

Here is the examinable judgment. A coordinator that always runs the full pipeline
is not really coordinating. The guide treats choosing which subagents a request
actually needs as the coordinator's defining job.

So when one exam option adds a routing decision and another adds a worker, the
routing decision is usually the answer.

And one failure you would never think to guard against, which the guide names:
overly narrow task decomposition, leading to incomplete coverage. The
coordinator can be too good at splitting. Six narrow workers all reporting
success can cover less ground than two broad ones — and every one of them
reports success.

[screen: a worker prompt]

One point three. Spawning a subagent.

This is the fact everything else follows from: subagent context must be provided
explicitly in the prompt, because subagents do not inherit parent context and do
not share memory between invocations.

Write the worker's prompt as though it has never met you. Because it hasn't.

A coordinator that says "review the lesson we just discussed" has told the worker
nothing. The worker has no "just". And it will not ask — it will confidently
invent a subject.

So pass the findings, not references to the findings. "Use the search results"
works in your head and not in a prompt.

[screen: tools: Read, WebFetch — and a worker without them]

Now the part that costs an afternoon. There are two ways a tool you granted a
subagent disappears anyway.

The documentation is blunt about the first: Claude Code removes every other
built-in tool from a background subagent, whether inherited or listed in the
tools field. So a tools entry you wrote can be stripped, and nothing about the
definition tells you that happened.

The second is nesting. There is a depth limit, three layers by default, and the
spawning tool is automatically removed at it. A worker that was supposed to
delegate further simply can't — and the symptom is that it does the work itself.

[screen: Task beside Agent]

One naming thing, and it is the kind of detail that decides a question.

The exam guide says the Task tool. The current documentation says the Agent tool,
and there is no Task row in the tools reference at all.

Hold both. The objective being tested is the requirement — a coordinator cannot
spawn workers unless the spawning tool is in its allowed list — and that is true
under either name. If an exam item says Task, answer the guide. If you are
configuring a real project today, the docs are what your settings file has to
match.

And a permission rule naming a tool that doesn't exist is not an error. It is
silently inert.

[screen: a prompt instruction beside a hook]

One point four and one point five together, because they share a sentence.

Here is the sentence, and it governs a whole family of exam items. The guide
states it as fact: when deterministic compliance is required, prompt instructions
alone have a non-zero failure rate.

Its example is identity verification before a financial operation.

Non-zero is the whole problem. A rule that holds ninety-nine percent of the time
is not a prerequisite. It's a tendency.

So the exam item writes itself. A business rule must always hold. One option
strengthens the prompt; another adds a hook or a prerequisite gate. The mechanism
wins, and the guide tells you why in the plainest language it uses anywhere.

Hooks give deterministic guarantees. Prompts give probabilistic compliance. Two
named uses: interception, blocking a tool call that violates policy — and
normalisation, transforming a tool result before the model sees it.

[screen: onFailure: block]

But here is the thing about hooks that the exam will not ask and that will cost
you more in practice.

When a hook script is missing, times out, can't start, or exits non-zero with
anything other than two — the documented default is a non-blocking error. The
action proceeds. You get a notice in the transcript and the tool call runs anyway.

So a hook with a wrong path, or one that crashes on an edge case, is not a
control. It's a comment. And a session with a broken hook looks exactly like a
session doing fine.

The fix is one key: onFailure, set to block.

And one caveat I want you to hear, because it is this problem one level deeper:
that key requires a recent Claude Code. On an older version it isn't rejected,
it's ignored — so the hook stays fail-open and your config still reads as though
the rule is enforced. Check your version before you rely on the line.

[screen: PostToolUse]

One more: you cannot undo a tool call from PostToolUse. By then it has run. You
can change what the model is told about it, and that's all. If something must not
happen, the hook belongs on PreToolUse.

[screen: a chain beside a plan]

One point six. How to split the work.

The guide frames this as a binary with a clean discriminator. Fixed sequential
pipelines — prompt chaining — versus dynamic adaptive decomposition based on
intermediate findings.

The discriminator is predictability. If you know the steps before you start,
chain them. If the next step depends on what the last one found, you cannot write
the chain.

And the exam stem will tell you which. "A comprehensive review of four known
aspects" is a chain. "Add tests to a legacy codebase" is not — you don't know
what you'll find.

Both mismatches are named. Dynamic decomposition for a predictable workflow pays
a planning step to rediscover a sequence you already knew. A fixed pipeline for
an open-ended investigation was written before anyone knew the shape.

[screen: per-item passes, then one cross-item pass]

And one structural pattern worth memorising, because it recurs everywhere: per
item local passes, plus a separate cross item integration pass.

The guide's named cost for doing both at once is attention dilution. One pass
asked to find local problems and cross-cutting problems reliably finds neither
well.

[screen: a resumed session reading a stale file]

Last one. One point seven. Session state.

The guide puts the judgment in its own words, and this is a correctness question
rather than a mechanics question: why starting a new session with a structured
summary is more reliable than resuming with stale tool results.

Think about what a resume restores. Everything. Including file contents that were
read before you changed the files.

A transcript is a record of what was true. If the code has moved, the agent is
reasoning from a snapshot — and nothing about restoring it marks which parts have
expired. It will be confident about a file you have since edited.

So the named anti-pattern is resuming with stale tool results where a summary
would be more reliable. And its partner: requiring full re-exploration after
changing files, instead of just telling the resumed session which files changed.

Forking is the other case. You've paid for an analysis once and you want two
conclusions from it — two approaches off one shared baseline.

[screen: the anti-pattern slide]

The anti-patterns for this domain, and this is the longest list in the exam guide.

Parsing natural language for termination. An arbitrary iteration cap as the
primary stopping mechanism. Assistant text as a completion indicator. Subagent
communication bypassing the coordinator. Always routing through the full pipeline.
Overly narrow decomposition. Assuming a subagent inherits parent context. Prompt
instructions where deterministic compliance is required. A single large review
pass instead of local plus cross-cutting. And resuming with stale tool results.

Ten. Published, before the exam, as the shapes of the wrong answers.

Notice how many are the same shape underneath: something that looks correct and
quietly isn't. A cap that reads as a design. A tool list that reads as what the
worker has. A restored transcript that reads as current. An instruction that
reads as a guarantee.

That pattern is most of this exam.

[screen: the coordinator running, workers reporting]

That's the coordinator, and it runs.

Next episode: Domain 4, prompt engineering and structured output. JSON schemas
that cannot be violated, and the three places that guarantee stops holding.

Everything in this course is sourced from the published exam guide or the public
documentation, and every claim is traced in SOURCES.md. Content verification
state is in VERIFICATION.md, including what has not been checked. Nothing here
comes from sitting the exam.

Repo link is below.
```

---

## Tips

Not spoken on camera — for the written lesson and the episode notes.

**A model can emit text and tool calls in the same response**, which is why "is there
assistant text?" fails as a completion check — and it fails *intermittently*, on the turn
where the model narrates while calling something.

**An iteration cap that is never hit teaches you nothing, and one that is hit routinely is
your termination condition.** If runs normally end at the cap, you have a timeout dressed
as a design.

**Check the result subtype before the result text.** The text is absent on every error
subtype, so reading it unconditionally gives you an empty string and no idea why.

**Budget caps can overshoot, by design**, because the check happens after a response
arrives — that is when its cost is known. If the cap is a hard ceiling for you, set it
below your actual limit.

**Verbose tool output is the quietest cost in a loop.** Paid once per turn, then again on
every subsequent turn, because it stays in the conversation.

**A coordinator that always runs the full pipeline is not a coordinator.** Dynamic
selection of which workers a request needs is the guide's defining responsibility for the
role.

**Six narrow workers all reporting success can cover less than two broad ones**, and the
coverage gap is invisible because every individual report is clean.

**Worker-to-worker shortcuts are tempting and cost you the transcript.** The system keeps
working; you just stop being able to see what it did.

**"Review what we just discussed" is the single most common subagent bug.** It is not a
vague instruction — it refers to nothing, and the worker will confidently invent a subject.

**A tool listed in `tools:` can still be absent at runtime.** If a worker says it cannot do
something you granted, check whether it is backgrounded or nested before debugging the
definition.

**`maxTurns` marks output partial rather than failing**, so a truncated result looks like a
result. Treat an unexpectedly thin answer as suspect.

**A gate that checks "was it called" is satisfied by a call that failed.** Gate on the
result, never on the invocation.

**A handoff without a "what I could not check" line reads as complete**, and the human
receiving it has no transcript to discover otherwise.

**Verify a hook by firing it, once, deliberately, the day you write it.** A hook that has
never fired is indistinguishable from one with a wrong path.

**A config key your Claude Code version does not know is ignored, not rejected.** It fails
open and looks correct in review.

**If you can write the steps down before starting, write them down and chain them.** The
planning step is only worth paying for when the next step genuinely depends on the last
one's findings.

**The cross-cutting pass wants summaries, not sources.** Handing it the full material
reintroduces the attention dilution the two-pass split existed to avoid.

**A resumed session is confident about files you have since edited**, and nothing in the
restoration marks which parts have expired.

**`/branch` keeps your permission grants; `--fork-session` does not.** Worth knowing before
you lose ten minutes re-approving things.

---

## Post-production checklist

- [ ] Watch the full take at full screen. No internal paths, nothing in the window title or
      tab bar, no other `/mcp` entries.
- [ ] **Chapter markers at each of the seven task statements.** At this runtime they are not
      a nicety.
- [ ] The fan-out take genuinely spawned in one response, not across turns. If it
      serialised, re-record — it cannot be fixed in the edit and must not be claimed.
- [ ] The non-zero-failure-rate claim and the attention-dilution claim are both attributed
      to the exam guide on screen, not stated as measured here.
- [ ] `Task` versus `Agent` is shown as a discrepancy with both halves named, not resolved
      in favour of one.
- [ ] The `onFailure` version caveat is stated. Without it the segment teaches a fix that
      silently does nothing on an older install.
- [ ] Clean clone at this episode's commit reproduces the coordinator and the tests.
- [ ] Description carries the repo link with the `julie-elkins` handle.
