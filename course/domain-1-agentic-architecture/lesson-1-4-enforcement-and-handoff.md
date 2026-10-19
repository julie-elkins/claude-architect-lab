# Lesson 1.4 — Gating a step, and handing off to someone who cannot see the conversation

**Domain 1: Agentic Architecture & Orchestration — 27% of CCAR-F**
**Task Statement 1.4:** Implement multi-step workflows with enforcement and handoff
patterns.

Lab artifact: Course Doctor refusing to write a finding until the source fetch has
returned, and producing a handoff a human can act on without reading the transcript.

## What you will be able to do afterwards

Block a step until its prerequisite has genuinely completed, and write a handoff that is
useful to someone who was not there.

## Why the exam cares

This task statement contains the sentence that governs half of this exam, and the guide
states it as a fact rather than advice: **when deterministic compliance is required — its
example is identity verification before a financial operation — prompt instructions alone
have a non-zero failure rate.**

Non-zero is the whole problem. A rule that holds 99% of the time is not a prerequisite; it
is a tendency. So the distinction it draws between **programmatic enforcement** (hooks,
prerequisite gates) and **prompt-based guidance** is the answer to a whole family of
items.

The second half is handoff, and the guide's framing is precise about why it is hard: you
are escalating to **human agents who lack access to the conversation transcript.** They
cannot read what happened. Whatever they need must be *in* the handoff.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Precondition.** Something that must be true before an operation may run. *Why it matters
here:* a prerequisite gate is a precondition with teeth. *Depth:* design-by-contract.

**Enforcement versus guidance.** Prevented against requested. *Why it matters here:* it is
the task statement's central distinction and the course's recurring theme. *Depth:*
lessons 1.5, 3.1 and 3.4, which are the same line drawn in three other places.

**State machine.** A system where only certain transitions are legal from a given state.
*Why it matters here:* "refund only after verified customer" is a transition rule, and
thinking of it that way makes the gate obvious. *Depth:* any treatment of finite state
machines.

**Handoff.** Transferring work to another party with the context they need. *Why it
matters here:* the receiving human has no transcript. *Depth:* clinical handover protocols
such as SBAR are the mature version of this idea.

**Shared context in parallel work.** Several investigations drawing on one body of facts.
*Why it matters here:* the guide names decomposing a multi-concern request and
investigating each part in parallel *using shared context*. *Depth:* lesson 1.2.

## The idea, before any code

**Ask whether the requirement is "should" or "must".** Should → prompt. Must → a gate. The
guide's test is whether compliance has to be *deterministic*, and if it does, no amount of
instruction wording gets you there.

**Then make the gate test the real thing, not a proxy.** "Blocking `process_refund` until
`get_customer` has returned a verified customer ID" is the guide's own example, and notice
what it checks: not that the step *was called*, but that it **returned a verified ID.** A
gate that checks whether a prior tool ran is satisfied by a prior tool that ran and
failed.

**For the handoff, write for a stranger.** The guide lists exactly what to compile:
customer ID, root cause, amount, recommended action. Every item is something the human
would otherwise have to reconstruct, and one of them — the recommended action — is the
agent's actual contribution.

## The build

### Step 1 — the gate, and what it checks

Course Doctor must not write a finding about a source it has not successfully fetched.
The wrong gate:

```
if fetch_source_was_called: allow write_findings
```

That passes after a fetch that 404'd. The right gate tests the *result*:

```
if fetch_source returned a body AND a status of 200: allow write_findings
else: deny, with the reason
```

The mechanism is a `PreToolUse` hook — lesson 1.5 covers it, and the one line that matters
here is `onFailure: "block"`, because a gate that evaporates when its own script breaks is
not a gate.

### Step 2 — decompose a multi-concern request, then share the context

A lesson with three problems — a dead link, a stale quota and a renamed console path — is
three investigations. The guide's pattern: split into distinct items, investigate each
**in parallel using shared context**, then synthesise one resolution.

Shared context is the part that saves you. All three investigations need the lesson text
and its citation table. Fetched once, passed to each, rather than three workers each
reading the same file.

### Step 3 — the handoff

When the agent cannot resolve something, what reaches the human is not the transcript. So:

```
HANDOFF
  item           lesson 3.1, claim "files above the working directory load at launch"
  root cause     cited page returns 200 but no longer contains the quoted wording
  what was tried fetched the URL twice, searched the page for three phrasings
  recommendation re-read the memory docs and re-quote, or downgrade to OBSERVED
  not covered    the other five citations in this lesson were not checked
```

Five fields. Four of them a human would otherwise reconstruct, and the fifth —
`not covered` — is the one that stops the handoff reading as complete.

### Step 4 — make the gate fire, once

Write the gate, then deliberately violate the prerequisite and watch it refuse. A gate
that has never refused anything is indistinguishable from a gate with a logic error, and
both look like a well-behaved system.

## Tips

Things that cost somebody an hour.

**A gate that checks "was it called" is satisfied by a call that failed.** This is the most
common prerequisite bug and the hardest to see in review, because the code reads exactly
like the correct version. Test the returned value, not the invocation.

**A handoff without a "what I could not check" line reads as complete.** The human assumes
the agent covered the rest. That assumption is doing real damage in a support context and
in a certification context alike.

**"Recommended action" is the agent's contribution.** A handoff with facts and no
recommendation has moved the problem without reducing it.

**Shared context is cheaper than parallel re-reading.** Three workers each reading the
same file is three times the tokens for one file. Fetch once, pass it.

**Prompt-based ordering works right up until it does not, and nothing tells you which run
failed.** That is what non-zero failure rate means in practice: no error, no alert, one
refund processed without verification.

## The anti-pattern

From the guide's objectives:

> **Prompt instructions where deterministic compliance is required.** Its own example is
> identity verification before a financial operation, and its own words are that prompt
> instructions alone have a non-zero failure rate.

And the handoff form:

> **Escalating to a human who lacks the transcript, without compiling what they need.**

On exam day, when one option strengthens an instruction and another adds a hook or a gate,
the mechanism wins — and this task statement is where the guide says why in the clearest
language it uses anywhere.

## What this lesson does not cover

- **Hook mechanics** — TS 1.5, including the fail-open default that undoes a gate.
- **When to escalate at all** — Domain 5 TS 5.2, which is about triggers rather than
  format.
- **Error propagation between agents** — Domain 5 TS 5.3.
- **Decomposition strategy** — TS 1.6.
- **Coordinator architecture** — TS 1.2.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 1.4.

| Claim | Source |
|---|---|
| The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering | EG §6, TS 1.4 |
| When deterministic compliance is required, e.g. identity verification before financial operations, prompt instructions alone have a non-zero failure rate | EG §6, TS 1.4 |
| Structured handoff protocols for mid-process escalation including customer details, root cause analysis and recommended actions | EG §6, TS 1.4 |
| Implementing programmatic prerequisites that block downstream tool calls until prerequisite steps have completed, e.g. blocking `process_refund` until `get_customer` has returned a verified customer ID | EG §6, TS 1.4 |
| Decomposing multi-concern requests into distinct items, investigating each in parallel using shared context, then synthesising a unified resolution | EG §6, TS 1.4 |
| Compiling structured handoff summaries — customer ID, root cause, refund amount, recommended action — when escalating to human agents who lack access to the conversation transcript | EG §6, TS 1.4 |
| Hooks give deterministic guarantees where prompt instructions give probabilistic compliance | EG §6, TS 1.5 |
| A `PreToolUse` hook blocks a tool call; a missing, timed-out or erroring hook script is a non-blocking error and the action proceeds unless `onFailure: "block"` is set | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
