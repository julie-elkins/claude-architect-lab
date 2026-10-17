# Build to Pass — Claude Certified Architect – Foundations

**This file is generated. Do not edit it.**

It is the whole written course in one document, assembled from the per-lesson files
under `course/` by `scripts/build_guide.py`. Edit the lesson, then run:

```
python3 scripts/build_guide.py
```

The test suite checks this file against the lessons, so a stale guide fails the build
rather than quietly disagreeing with the course.

Lessons are in **dependency order**, not exam-weight order. See the
[repository README](README.md) for the exam details, the full 29-task-statement outline
including what is not yet written, how the course is sourced, and how to run the lab.

---

## Contents

- **TS 1.1** — Lesson 1.1 — The loop, and what is allowed to end it
- **TS 1.3** — Lesson 1.3 — Spawning a subagent, and what it does not know
- **TS 1.5** — Lesson 1.5 — Hooks, and the default that makes one useless
- **TS 1.7** — Lesson 1.7 — Resuming, branching, and what the saved state is no longer true about
- **TS 2.1** — Lesson 2.1 — The description is the routing logic
- **TS 2.2** — Lesson 2.2 — An error the agent can act on
- **TS 2.3** — Lesson 2.3 — Fewer tools, and forcing the first one
- **TS 2.4** — Lesson 2.4 — Wiring a server in, and what a populated `/mcp` does not prove
- **TS 2.5** — Lesson 2.5 — The built-in tools, and the two that are not there
- **TS 3.1** — Lesson 3.1 — Where an instruction lives decides who gets it
- **TS 3.2** — Lesson 3.2 — Packaging a procedure, and deciding what it may touch
- **TS 3.3** — Lesson 3.3 — Rules that only load when they are relevant
- **TS 3.4** — Lesson 3.4 — Planning first, and when plan mode is not actually a block
- **TS 3.5 and 3.6** — Lesson 3b — Iterating on purpose, and reviewing without yourself

---

# Lesson 1.1 — The loop, and what is allowed to end it

**Domain 1: Agentic Architecture & Orchestration — 27% of CCAR-F**
**Task Statement 1.1:** Design and implement agentic loops for autonomous task execution.

Lab artifact: Course Doctor's checking loop, bounded by something other than a guess.

## What you will be able to do afterwards

Describe one iteration of an agentic loop precisely, say what terminates it, and name why
the two most intuitive stopping mechanisms are both published anti-patterns.

## Why the exam cares

This is the first task statement of the largest domain, and the guide gives it the most
unusually specific anti-pattern list in the whole document — it names **three wrong
answers by name:**

- parsing natural language signals to determine loop termination
- setting arbitrary iteration caps as the primary stopping mechanism
- checking for assistant text content as a completion indicator

A published list of wrong answers is a published list of distractors. All three are
plausible, all three are things a competent engineer actually does, and that is exactly
what makes them good exam options.

## Fundamentals

**The agentic loop.** Send a request, get back either tool calls or a final answer, run
the tools, feed the results back, repeat. *Why it matters here:* it is the subject.
*Depth:* `/docs/en/how-claude-code-works`.

**`stop_reason`.** A field on the model's response saying why it stopped generating.
*Why it matters here:* it is the structural signal the guide wants you to branch on
rather than reading the prose. *Depth:* the Messages API documentation.

**A turn.** One round trip: the model produces output including tool calls, the tools
run, the results go back. *Why it matters here:* turn caps count these, and the
definition decides what a cap means. *Depth:* the build.

**Termination condition.** The rule that ends the loop. *Why it matters here:* the whole
task statement. A loop whose termination is incidental does not stop because it is
finished — it stops because something external killed it. *Depth:* Domain 3 TS 3.6 for
the unattended case.

**Idempotence.** Whether repeating an operation is safe. *Why it matters here:* a loop
that may retry needs its tools to tolerate being called twice. *Depth:* REST semantics.

## The idea, before any code

**Branch on structure, never on prose.**

The model tells you what it wants structurally. The documented cycle is explicit:
*"Turns continue until Claude produces output with no tool calls, at which point the loop
ends."* That is the condition. Tool calls present means continue; a response with no tool
calls means done.

At the API level this is what `stop_reason` carries — `tool_use` meaning the model wants
a tool run, `end_turn` meaning it has finished. The guide's framing is the same thing in
different words.

**So the three anti-patterns are all the same mistake:** reading something soft when a
hard signal is available.

- Parsing natural language for "I'm done" reads prose that was never a protocol.
- Checking whether assistant text exists is worse, because a model can produce text *and*
  tool calls in the same response — so text is present mid-task and your loop stops early.
- An iteration cap is not a termination condition at all. It is a safety net, and using
  it as the *primary* mechanism means your loop's normal exit is "ran out of allowance."

**A cap is still necessary.** The distinction the guide draws is primary versus backstop.
Keep the cap; just do not let it be the thing that normally ends the run.

## The build

### Step 1 — the cycle, concretely

For "check every cited URL in this lesson":

```
Turn 1   model calls read_material_file          -> text + the cited URLs
Turn 2   model calls fetch_source, three times   -> three pages
Turn 3   model calls write_findings              -> written
Final    model responds with text, no tool calls -> the loop ends
```

Four turns, three with tool calls, one without. The loop did not end because a counter
ran out or because the text sounded conclusive. It ended because there was nothing left
to call.

### Step 2 — feed results back, do not summarise them

Each tool's result is appended to the conversation and goes back to the model for the
next decision. That is what lets the model adapt: a `fetch_source` returning a 404
changes what it does next, but only if it sees the 404.

The context consequence is immediate and belongs in your design: **everything
accumulates.** Prompts, responses, tool inputs, tool outputs, across every turn. A
verbose tool is a context cost paid for the rest of the session.

### Step 3 — bound it, with the right thing

Two documented bounds, both of which end the run with a *named* result rather than
silently:

```
max_turns        -> result subtype error_max_turns
max_budget_usd   -> result subtype error_max_budget_usd
```

`max_turns` counts tool-use turns only. And the budget cap has a documented tolerance
worth knowing before you rely on it: spend is compared against the cap **after** a
response arrives, so **spend can pass the cap** by the cost of that response plus whatever
still-running subagents spend before they stop. Leave headroom.

### Step 4 — read the termination, do not infer it

When the loop ends you get a result whose subtype says which way it went: `success`,
`error_max_turns`, `error_max_budget_usd`, `error_during_execution`. **Check the subtype
before reading the output** — the final text is only present on `success`, so code that
reads it unconditionally gets nothing on exactly the runs you most need to diagnose.

## Tips

Things that cost somebody an hour.

**A model can emit text and tool calls in the same response.** This is why "is there
assistant text?" fails as a completion check, and it fails *intermittently* — the loop
works until the turn where the model narrates while calling something.

**An iteration cap that is never hit teaches you nothing, and one that is hit routinely
is your termination condition.** If runs normally end at the cap, you do not have a bound,
you have a timeout dressed as a design.

**Check the result subtype before the result text.** The text is absent on every error
subtype. Reading it unconditionally gives you an empty string and no idea why.

**Budget caps can overshoot, by design.** The check happens after a response arrives,
because that is when its cost is known. If the cap is a hard ceiling for you, set it
below your actual limit.

**Verbose tool output is the quietest cost in a loop.** It is paid once per turn and then
again on every subsequent turn, because it stays in the conversation.

**Compaction can drop your early instructions.** When context fills, older history is
replaced by a summary — so a rule stated once in the opening prompt may not survive.
Persistent rules belong in `CLAUDE.md`, which is re-injected on every request.

## The anti-pattern

Quoted, because the guide names all three:

> **"Avoiding anti-patterns such as parsing natural language signals to determine loop
> termination, setting arbitrary iteration caps as the primary stopping mechanism, or
> checking for assistant text content as a completion indicator."**

Three options you will see on exam day. The correct answer always branches on the
structural signal — tool calls present or absent — and keeps the cap as a backstop rather
than a design.

## What this lesson does not cover

- **Multi-agent coordination** — TS 1.2 and 1.3.
- **Hooks**, which can short-circuit a loop by rejecting a tool call before it runs —
  TS 1.5.
- **Task decomposition** — TS 1.6.
- **Context management as a subject** — Domain 5, though its consequences appear here.
- **Unattended runs.** Domain 3 TS 3.6, where the absence of a human changes what a bound
  is for.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 1.1.

| Claim | Source |
|---|---|
| The agentic loop lifecycle: send requests, inspect `stop_reason` (`"tool_use"` vs `"end_turn"`), execute requested tools, return results for the next iteration | EG §6, TS 1.1 |
| Tool results are appended to conversation history so the model can reason about the next action | EG §6, TS 1.1 |
| The distinction between model-driven decision-making and pre-configured decision trees or tool sequences | EG §6, TS 1.1 |
| Implementing loop control that continues on `"tool_use"` and terminates on `"end_turn"` | EG §6, TS 1.1 |
| Three named anti-patterns: parsing natural language signals for termination, arbitrary iteration caps as the primary stopping mechanism, and assistant text content as a completion indicator | EG §6, TS 1.1 |
| "Turns continue until Claude produces output with no tool calls, at which point the loop ends and the final result is delivered" | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| A turn is one round trip: output with tool calls, tools executed, results fed back automatically | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| `max_turns` counts tool-use turns only; `max_budget_usd` caps on estimated spend | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| Hitting either limit returns a result with subtype `error_max_turns` or `error_max_budget_usd` | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| "Spend can therefore pass the cap by up to the cost of that one response, plus anything that subagents still running at that moment spend before they stop" | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| The result `subtype` is the primary way to check termination state, and the `result` field is only present on `success` | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| Context does not reset between turns: system prompt, tool definitions, history, tool inputs and outputs all accumulate | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| "Compaction replaces older messages with a summary, so specific instructions from early in the conversation may not be preserved. Persistent rules belong in CLAUDE.md... because CLAUDE.md content is re-injected on every request" | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
| A `PreToolUse` hook that rejects a tool call prevents it executing, and Claude receives the rejection message instead | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |

**Outstanding:**

- [ ] The exam guide describes inspecting `stop_reason` for `"tool_use"`, which is the raw
      Messages API level. The SDK result's `stop_reason` lists `end_turn`, `max_tokens`
      and `refusal` as common values and describes termination through the
      no-tool-calls condition instead. Both describe the same mechanism at different
      layers; which layer a given exam item means is not resolved here.

---

# Lesson 1.3 — Spawning a subagent, and what it does not know

**Domain 1: Agentic Architecture & Orchestration — 27% of CCAR-F**
**Task Statement 1.3:** Configure subagent invocation, context passing, and spawning.

Lab artifact: Course Doctor's coordinator spawning one worker per lesson, each handed
everything it needs in its prompt.

## What you will be able to do afterwards

Spawn a subagent, pass it the context it needs, and predict what it will and will not be
able to see — including the two cases where a tool you granted it is removed anyway.

## Why the exam cares

The guide states the fact everything else in this task statement follows from:
**subagent context must be explicitly provided in the prompt, because subagents do not
automatically inherit parent context or share memory between invocations.**

Every failure here descends from forgetting that. A coordinator that says "review the
lesson we just discussed" has told the worker nothing. The worker has no "just".

There is also a naming discrepancy you need to hold both halves of. See the note in the
build — it is the kind of thing that decides a question.

## Fundamentals

**Process isolation.** Separate execution with separate state. *Why it matters here:* a
subagent is an isolated context, which is the whole point and the whole hazard. *Depth:*
any treatment of process boundaries.

**Explicit versus implicit context.** Information passed deliberately against information
assumed available. *Why it matters here:* subagents get only what you pass. *Depth:*
dependency injection is the same discipline in another setting.

**Fan-out and join.** Starting several workers, then combining results. *Why it matters
here:* parallel spawning is named as a skill, and the join is where attribution gets
lost. *Depth:* map-reduce.

**Provenance.** Keeping track of where a piece of information came from. *Why it matters
here:* the guide names separating content from metadata — source URLs, document names,
page numbers — specifically to preserve attribution across agents. *Depth:* Domain 5
TS 5.1.

**Allowlist.** An explicit list of what is permitted. *Why it matters here:* a subagent's
tool list is one, and so is the parent's — and both can be overridden in ways that
surprise you. *Depth:* lesson 2.3.

## The idea, before any configuration

**Write the worker's prompt as though it has never met you**, because it has not. The
guide's skill is including *complete findings from prior agents directly in the
subagent's prompt* — passing the search results and the document analysis into the
synthesis worker, not a reference to them.

**Separate the content from where it came from.** The guide names structured formats that
keep source URLs, document names and page numbers distinct from the text, so attribution
survives being handed on. A worker that receives a wall of prose cannot tell you which
source a claim came from, and your report then cannot either.

**Say what the worker decides, and what it must not.** The guide's phrasing is
instructive: coordinator prompts should specify *research goals and quality criteria
rather than step-by-step procedural instructions*, so the worker can adapt. Goals, not
choreography — but a named boundary on what it may conclude.

## The build

### Step 1 — the tool that spawns, and the name discrepancy

**The exam guide says the `Task` tool, and names the requirement that `allowedTools`
include `"Task"` for a coordinator to invoke subagents.**

**The current Claude Code documentation says the `Agent` tool**: "the parent conversation
needs the `Agent` tool in its allowed tools to spawn subagents," and `Agent` is what the
tools reference lists — there is no `Task` row in it.

Hold both. The objective being tested is the *requirement* — a coordinator cannot spawn
workers unless the spawning tool is in its allowed list — and that is true under either
name. If an exam item names `Task`, answer the guide; if you are configuring a real
project today, the docs are what your settings file has to match. **A permission rule
naming a tool that does not exist is not an error. It is silently inert**, which is the
same failure shape as lesson 2.5's `Grep` rule on macOS.

### Step 2 — define the worker

```yaml
---
name: lesson-source-checker
description: Checks one lesson's cited URLs against the live pages and reports per-claim verdicts
tools: Read, WebFetch
model: sonnet
maxTurns: 12
---

You check exactly ONE lesson. Everything you need is in this prompt; you cannot
see the conversation that sent you.

Report per claim: the claim verbatim, the URL, and SUPPORTED, CONTRADICTED,
NOT IN DOCS, or NOT CHECKED. You never edit a lesson and you never set a
verified date.
```

`name` and `description` are required — the description is what the parent matches on to
delegate. `tools` is an allowlist, `disallowedTools` a denylist, and `maxTurns` caps the
agentic turns, after which **the output is marked partial** rather than silently truncated.

### Step 3 — the two ways a granted tool disappears anyway

This is the part that costs an afternoon.

**A background subagent keeps only a restricted set.** The documentation is blunt:
"Claude Code removes every other built-in tool from a background subagent, whether
inherited **or listed in the `tools` field**." So a `tools:` entry you wrote can be
stripped, and nothing about the definition tells you that happened.

**Nesting removes the spawning tool.** There is a depth limit, three layers by default,
and the spawning tool is automatically removed at it. A worker that was supposed to
delegate further simply cannot, and the symptom is that it does the work itself.

### Step 4 — spawn several at once

The guide's skill is **emitting multiple spawn calls in a single coordinator response
rather than across separate turns.** One response, several workers, genuinely concurrent.
Spread across turns they serialise, and you have paid for parallelism you did not get.

Two costs to know: each worker's returned result consumes your context, and each spends
its own tokens. Fan-out is a context trade, not a free speed-up.

### Step 5 — fork when the background is the point

A fork is the opposite case: it **inherits the entire conversation** — same system
prompt, tools, model and message history — and runs in the background while you continue.
Use it when a fresh worker would need so much background that writing the prompt costs
more than sharing the context. Its tool calls stay out of your conversation and only the
result comes back.

## Tips

Things the documentation does not tell you.

**"Review what we just discussed" is the single most common subagent bug.** The worker
has no conversation. It is not a vague instruction — it is an instruction referring to
nothing, and the worker will confidently invent a subject.

**A tool listed in `tools:` can still be absent at runtime.** Background restriction and
the depth limit both remove tools without complaint. If a worker reports it cannot do
something you granted, check whether it is backgrounded or nested before debugging the
definition.

**`maxTurns` marks output partial rather than failing.** So a truncated result looks like
a result. Read the marker, or treat an unexpectedly thin answer as suspect.

**Pass findings, not references to findings.** "Use the search results" works in your head
and not in a prompt. The guide says include the complete findings directly, and it means
it.

**Parallel spawning must be one response, not several turns.** The difference is invisible
in the transcript afterwards and the wall-clock cost is large.

## The anti-pattern

From the guide's objectives for this domain:

> **Assuming a subagent inherits parent context.**

And the one the documentation adds:

> **Treating a tool list as what the worker will have.**

Both are the same shape as everything else in this course: a configuration that reads
correctly and does not hold. The definition says `tools: Read, WebFetch, Bash`; the
backgrounded worker has a different set; nothing says so.

## What this lesson does not cover

- **Coordinator architecture and hub-and-spoke routing** — TS 1.2.
- **The agentic loop and its termination** — TS 1.1.
- **Hooks** — TS 1.5.
- **Task decomposition strategy** — TS 1.6.
- **Session resumption and `fork_session`** — TS 1.7. A fork of the *conversation* here is
  not the same as forking a *session*.
- **Context budget as a subject** — Domain 5.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 1.3.

| Claim | Source |
|---|---|
| The `Task` tool is the mechanism for spawning subagents, and `allowedTools` must include `"Task"` for a coordinator to invoke them | EG §6, TS 1.3 |
| Subagent context must be explicitly provided in the prompt; subagents do not inherit parent context or share memory between invocations | EG §6, TS 1.3 |
| An agent definition carries descriptions, system prompts and tool restrictions per subagent type | EG §6, TS 1.3 |
| Fork-based session management explores divergent approaches from a shared baseline | EG §6, TS 1.3 |
| Including complete findings from prior agents directly in the subagent's prompt | EG §6, TS 1.3 |
| Using structured formats to separate content from metadata — source URLs, document names, page numbers — to preserve attribution | EG §6, TS 1.3 |
| Spawning parallel subagents by emitting multiple spawn calls in a single coordinator response rather than across separate turns | EG §6, TS 1.3 |
| Coordinator prompts should specify research goals and quality criteria rather than step-by-step procedural instructions | EG §6, TS 1.3 |
| **The documentation names the `Agent` tool, not `Task`:** "the parent conversation needs the `Agent` tool in its allowed tools to spawn subagents" | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| A non-fork subagent starts fresh: no conversation history, no previous file reads, receiving only a delegation message | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| A fork inherits the entire conversation — same system prompt, tools, model and message history | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| Required fields `name` and `description`; optional `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `memory`, `background` | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| `maxTurns` caps agentic turns and the output is marked partial | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| "Claude Code removes every other built-in tool from a background subagent, whether inherited or listed in the `tools` field" | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| The spawning tool is automatically removed at the depth limit, three layers by default | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| A returned subagent result consumes the parent's context, and each subagent spends its own tokens | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |

**Outstanding:**

- [ ] Whether `Task` is a current alias for `Agent`, an Agent SDK name, or stale in the
      exam guide. The lesson teaches the requirement under both names and does not
      resolve which is authoritative for a given exam item.

---

# Lesson 1.5 — Hooks, and the default that makes one useless

**Domain 1: Agentic Architecture & Orchestration — 27% of CCAR-F**
**Task Statement 1.5:** Apply Agent SDK hooks for tool call interception and data
normalization.

Lab artifact: a hook that normalises the timestamp formats Course Doctor's sources return,
and one that refuses a write outside the project.

## What you will be able to do afterwards

Choose between a hook and a prompt instruction for a given requirement, intercept a tool
call to block or rewrite it, normalise a tool result before the model sees it — and
configure a hook so that a broken one fails closed instead of disappearing.

That last clause is the most important sentence in this lesson.

## Why the exam cares

The guide states the distinction plainly: **hooks give deterministic guarantees; prompt
instructions give probabilistic compliance.** And it makes the consequence explicit —
when deterministic compliance is required, for example identity verification before a
financial operation, *prompt instructions alone have a non-zero failure rate.*

So the exam item writes itself. A business rule must always hold; one option strengthens
the prompt and another adds a hook. The hook is the answer, and the guide says why.

Its named uses are both here: **interception** — blocking a tool call that violates
policy — and **normalisation** — transforming a tool result before the model processes it.

## Fundamentals

**Determinism.** The same input always producing the same result. *Why it matters here:*
it is the single property that separates a hook from an instruction. *Depth:* none
needed; the word is doing the work.

**Interception.** Code that runs between a caller and a callee and may alter or stop the
call. *Why it matters here:* that is `PreToolUse`. *Depth:* middleware in any web
framework is the same pattern.

**Normalisation.** Converting varied representations of the same thing into one shape.
*Why it matters here:* the guide's own example is Unix timestamps, ISO 8601 and numeric
status codes arriving from different tools. *Depth:* any ETL treatment.

**Fail-open versus fail-closed.** What a broken control does: allow by default, or deny
by default. *Why it matters here:* **this decides whether your hook is a control at all.**
*Depth:* the build below, and it is the lesson.

**Exit codes.** A number a process returns to signal outcome. *Why it matters here:* a
hook signals a block with a specific one. *Depth:* `man 3 exit`.

## The idea, before any configuration

**Ask whether the requirement is "should" or "must".** A convention that is usually
followed belongs in instructions. A rule that must hold every time — a prerequisite, a
spend ceiling, a refusal — belongs in a hook, because an instruction has a failure rate
and a hook does not.

This is the third time this course has drawn that line: a `CLAUDE.md` is context not a
control (lesson 3.1), plan mode is not enforced in every context (lesson 3.4), and here
is the mechanism that actually enforces.

**Then ask what happens when the hook itself breaks.** Almost nobody asks this, and the
default answer is not the one you want. See step 3.

## The build

### Step 1 — intercept, and block

`PreToolUse` runs before a tool call. It blocks by **exiting 2**:

```bash
#!/bin/bash
# Refuse a write outside the project root.
if [[ "$TARGET" != "$CLAUDE_PROJECT_DIR"* ]]; then
  echo "Blocked: write outside the project root" >&2
  exit 2
fi
exit 0   # no decision; the normal permission flow applies
```

Or structurally, which is clearer when you want to say why:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Write outside the project root"
  }
}
```

`permissionDecision` takes `allow`, `deny`, `ask` or `defer`.

### Step 2 — normalise, and rewrite

`PostToolUse` runs after a successful call and can **replace the output the model sees**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "updatedToolOutput": "fetched_at: 2026-10-17T14:02:00Z"
  }
}
```

That is the guide's data-normalisation objective, exactly: heterogeneous formats from
different tools, converted to one shape before the agent reasons about them. `PreToolUse`
has the mirror image, `updatedInput`, for rewriting a call's arguments on the way in.

### Step 3 — the default that makes a hook decorative

Read this carefully. When a hook script is **missing**, **times out**, **cannot start**, or
**exits non-zero with anything other than 2**, the documented default is:

> **Non-blocking error; the action proceeds.**

The user sees a `hook error` notice in the transcript. The tool call runs anyway.

So a hook whose path is wrong, whose interpreter is missing, or which crashes on an edge
case **is not a control. It is a comment.** And a session with a broken hook looks like a
session doing fine — which is the exact failure this whole course keeps circling.

**The fix is one key:**

```json
{
  "type": "command",
  "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-write.sh",
  "onFailure": "block"
}
```

With `onFailure: "block"`, every one of those four cases blocks the action instead of
waving it through. **If the hook enforces a rule that must hold, it needs this line.**
Without it you have chosen fail-open, whether you meant to or not.

### Step 4 — know which events a block even applies to

Exit code 2 blocks `PreToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`
and a few others. It **does not** block `PostToolUse`, `PostToolUseFailure`,
`PermissionRequest` or `Notification`.

Which means: you cannot undo a tool call from `PostToolUse`. By then it has run. You can
rewrite what the model is told about it, and that is all. If something must not happen,
the hook belongs on `PreToolUse`.

## Tips

Things the documentation does not tell you plainly enough.

**Verify a hook by firing it, once, deliberately, the day you write it.** A hook that has
never fired is indistinguishable from a hook with a wrong path — in both cases nothing
happens and nothing complains.

**A hook that crashes is worse than no hook, because you believe you have one.** This is
the practical reason `onFailure: "block"` exists, and the reason to prefer a tiny hook
script over a clever one.

**`PostToolUse` cannot prevent anything.** People reach for it because it is where the
result is. The call already happened.

**Normalise at the boundary, not in the prompt.** Asking the model to cope with three
timestamp formats works until the fourth arrives. A hook converting them is deterministic
and the model never sees the variety.

**A hook in subagent frontmatter is scoped to that subagent.** Handy, and easy to forget
when you are looking for why a rule does not apply in the main session.

## The anti-pattern

From the guide's objectives:

> **Relying on prompt instructions for compliance that must be guaranteed.**

The guide's own case is identity verification before a financial operation, and its
phrasing is the thing to remember: prompt instructions alone have a *non-zero failure
rate*. For a rule that must hold, non-zero is the whole problem.

And the one the documentation hands you, which no exam item will ask and which will cost
you more in practice:

> **A hook without `onFailure: "block"` that was meant to enforce something.**

It enforces while it works and evaporates the moment it does not, silently. That is
fail-open by default, and it is a choice you make by omission.

## What this lesson does not cover

- **Prerequisite gating across a workflow** — TS 1.4, which uses hooks as its mechanism.
- **Every hook event.** There are over thirty; this covers the two the task statement
  names plus the failure semantics.
- **Hook handler types beyond `command`.** `http`, `mcp_tool`, `prompt` and `agent` all
  exist.
- **Permission rules**, which are a different mechanism with a different default.
- **Observability.** A hook that blocked leaves a record; whether anything records a hook
  that *ran and allowed* is a different question, and an important one.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 1.5.

| Claim | Source |
|---|---|
| Hook patterns such as `PostToolUse` intercept tool results for transformation before the model processes them | EG §6, TS 1.5 |
| Hook patterns intercept outgoing tool calls to enforce compliance rules, e.g. blocking refunds above a threshold | EG §6, TS 1.5 |
| Hooks give deterministic guarantees; prompt instructions give probabilistic compliance | EG §6, TS 1.5 |
| When deterministic compliance is required, prompt instructions alone have a non-zero failure rate | EG §6, TS 1.4 |
| Implementing `PostToolUse` hooks to normalise heterogeneous formats — Unix timestamps, ISO 8601, numeric status codes — from different MCP tools | EG §6, TS 1.5 |
| Choosing hooks over prompt-based enforcement when business rules require guaranteed compliance | EG §6, TS 1.5 |
| `PreToolUse` runs before a tool call; `PostToolUse` after it succeeds | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| A `PreToolUse` hook blocks by exiting 2, or by returning `permissionDecision` of `allow`, `deny`, `ask` or `defer` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| `PostToolUse` can replace output via `updatedToolOutput`; `PreToolUse` can rewrite arguments via `updatedInput` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| **A missing script, a timeout, a failure to start, or a non-zero exit other than 2 is a NON-BLOCKING error and the action proceeds** | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| **`onFailure: "block"` makes each of those cases block the action instead** | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| Exit code 2 does not block `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` or `Notification` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| Hooks are configured in `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, managed policy, plugin `hooks/hooks.json`, or skill and subagent frontmatter | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| Handler types are `command`, `http`, `mcp_tool`, `prompt` and `agent` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |

---

# Lesson 1.7 — Resuming, branching, and what the saved state is no longer true about

**Domain 1: Agentic Architecture & Orchestration — 27% of CCAR-F**
**Task Statement 1.7:** Manage session state, resumption, and forking.

Lab artifact: two branches off one Course Doctor analysis, comparing two checking
strategies without re-reading the corpus.

## What you will be able to do afterwards

Resume a conversation, branch one to explore an alternative, and decide between resuming
and starting fresh — on the basis of whether the saved state is still true.

## Why the exam cares

The guide puts the judgment call in its own words, and it is the whole task statement:
**why starting a new session with a structured summary is more reliable than resuming with
stale tool results.**

That is not a mechanics question, it is a correctness question. A resumed session restores
everything, including file contents that were read before you changed the files. The
transcript is a record of what *was* true. If the code has moved, the agent is reasoning
from a snapshot and nothing about the restoration says so.

The guide also names forking for exploring divergent approaches from a shared baseline —
the case where you have paid for analysis once and want two conclusions from it.

## Fundamentals

**Session.** A saved conversation tied to a project directory. *Why it matters here:* it
is the unit being resumed. *Depth:* `/docs/en/sessions`.

**Transcript.** The file the conversation is saved to. *Why it matters here:* resumption
reads it, and knowing it is a file explains both the power and the staleness. *Depth:*
the build.

**Branching versus resuming.** Continuing one conversation against copying it. *Why it
matters here:* this is the fork decision. *Depth:* the build.

**Staleness.** State that was accurate when recorded and is not now. *Why it matters
here:* the entire judgment in this task statement. *Depth:* it is also the thesis of the
lab this course builds.

**Shared baseline.** Work done once and used by several downstream paths. *Why it matters
here:* it is what makes forking cheaper than running twice. *Depth:* copy-on-write, same
shape.

## The idea, before any commands

**Resume when the prior context is mostly still valid. Start fresh with a summary when it
is not.**

The question is never "would resuming be convenient." It is: *has the world the
transcript describes changed?* If you read twenty files and then edited six of them,
resuming restores twenty file contents of which six are wrong, and the agent has no way
to know which.

The guide's remedy is the structured summary: begin a new session and inject what you
know to be true — the findings, the decisions, the current state — rather than restoring a
record of what was read. Smaller, accurate, and deliberately authored.

**Fork when you want two answers from one piece of thinking.** A long analysis, then two
strategies off the same baseline. You pay for the analysis once.

**And if you do resume after changing files, say what changed.** The guide names it as a
skill: informing a resumed session about specific file changes for targeted re-analysis
rather than requiring full re-exploration.

## The build

### Step 1 — resume

```
claude --continue                      # most recent in this directory
claude --resume                        # interactive picker
claude --resume auth-refactor          # by name
claude --resume <session-id>           # by id, from any directory
```

Name sessions so they are findable: `claude -n corpus-audit` at launch, or `/rename` mid
session. An unnamed session still gets a generated title from a background model, and that
title works as a resume handle — but the default display name like `my-app-3f` **does
not.** Passing it to `--resume` finds nothing.

### Step 2 — know what comes back, and what does not

A resumed session restores the full conversation including tool calls and results, the
model, the agent and its tool restrictions, and usually the permission mode.

**It does not restore every launch flag.** If the session depended on `--mcp-config`,
`--settings`, `--plugin-dir`, `--fallback-model`, or directories added with `--add-dir`,
pass them again. Settings *files* are re-read; flags are not.

And one documented behaviour that is better than you would expect: **a tool still running
when the previous process died does not finish and does not re-run.** Claude sees the call
marked as cut off before its result was recorded, and is told to check whether it took
effect before trying again. That is the right default for a half-applied edit, and it is
worth knowing it exists rather than assuming either extreme.

### Step 3 — branch

From inside a session:

```
/branch compare-strict-checking
```

From the command line:

```
claude --continue --fork-session
```

Both copy the conversation and leave the original intact, with its own session id, in the
picker. One difference matters: `/branch` keeps running in the same process, so
"allow for this session" permission grants carry over. **`--fork-session` starts a
separate process and you re-approve there.**

### Step 4 — start fresh, on purpose

When the transcript is stale, write the summary instead:

```
claude -n corpus-audit-2 "Context: 121 chunks under ~/course-corpus-content.
MLA depths are set; the other three courses are unreviewed. Nothing has a
verified date. Six lessons are written. Do not re-read the corpus; work from
this and ask for what you need."
```

Short, current, and authored. Compare that with restoring a transcript containing the
full text of files that have since changed.

## Tips

Things the documentation does not tell you plainly.

**A resumed session is confident about files you have since edited.** Nothing flags the
difference. This is the single most expensive habit in this task statement, and the
symptom is an agent reasoning carefully about code that no longer exists.

**The default display name is not a resume handle.** `my-app-3f` identifies a running
session in listings and cannot be resumed by. The generated *title* can. Two labels, one
of which works.

**`-p` and SDK sessions are missing from the picker and from `--continue`.** They are
resumable by id. If an automated run seems to have vanished, it has not — you need the id.

**`/branch` keeps your permission grants; `--fork-session` does not.** Same conversation,
different process, and you re-approve everything you had allowed for the session.

**Resuming the same session in two terminals without forking interleaves both into one
transcript.** It does not error. You get one conversation with two people talking over
each other.

**Do not build tooling that parses transcript files.** They are JSONL at
`~/.claude/projects/<project>/<session-id>.jsonl`, and the documentation is explicit that
the entry format is internal and changes between versions, so a parser can break on any
release. Use `/export`, `--output-format json`, or a hook's `transcript_path` instead.

## The anti-pattern

From the guide's objectives:

> **Resuming with stale tool results** where a new session with a structured summary
> would be more reliable.

And its partner, which is the same mistake at a smaller scale:

> **Requiring full re-exploration** after changing files, instead of telling the resumed
> session which files changed.

Both are the course's recurring shape once more: restored state that reads as current.
A transcript is a record of what was true, and nothing about restoring it marks which
parts have expired.

## What this lesson does not cover

- **Compaction and `/clear`.** They manage context *within* a session; this is about
  crossing between them. Domain 5 covers context.
- **Checkpointing**, which rewinds inside one session rather than branching.
- **Worktrees**, for parallel sessions on separate branches.
- **Forking a conversation into a subagent** — lesson 1.3. Forking a *session* and forking
  a *conversation into a worker* are different mechanisms with similar names.
- **The full permission-mode-on-resume matrix**, which is genuinely intricate. One rule
  worth carrying: a session that ended in plan mode resumes in plan mode in a terminal,
  but **not** when you pass `--fork-session`.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 1.7.

| Claim | Source |
|---|---|
| Named session resumption using `--resume <session-name>` to continue a specific prior conversation | EG §6, TS 1.7 |
| `fork_session` creates independent branches from a shared analysis baseline to explore divergent approaches | EG §6, TS 1.7 |
| The importance of informing the agent about changes to previously analysed files when resuming after modifications | EG §6, TS 1.7 |
| Why starting a new session with a structured summary is more reliable than resuming with stale tool results | EG §6, TS 1.7 |
| Choosing between resumption (when prior context is mostly valid) and starting fresh with injected summaries (when prior tool results are stale) | EG §6, TS 1.7 |
| Informing a resumed session about specific file changes for targeted re-analysis rather than full re-exploration | EG §6, TS 1.7 |
| `--continue`, `--resume`, `--resume <name>`, `--resume <transcript-path>`, and `/resume` | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| A resumed session restores full conversation history including tool calls and results, the model, the agent and its tool restrictions | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model` and `--add-dir` are NOT restored and must be passed again; settings files are re-read | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| A tool still running when the previous process ended "doesn't finish or run again when you resume"; Claude sees it marked cut off and is told to check whether it took effect | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| `/branch` copies the conversation in the same process so session permission grants carry over; `--fork-session` starts a separate process without them | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| A session that ended in plan mode resumes in plan mode in a terminal, but not with `--fork-session` | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| The default display name is not a resume handle; the generated title is | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| `-p` and Agent SDK sessions are excluded from the picker and from `--continue`, and are resumable by session id | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| Resuming the same session in two terminals without forking interleaves messages into one transcript | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |
| Transcripts are JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, and "the entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release" | [sessions docs](https://code.claude.com/docs/en/sessions), read 2026-10-17 |

---

# Lesson 2.1 — The description is the routing logic

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.1:** Design effective tool interfaces with clear descriptions and
boundaries.

Lab artifact: Course Doctor's tool surface, with each tool's purpose written so the next
one cannot be confused with it.

## What you will be able to do afterwards

Diagnose a tool that never gets called, or gets called for the wrong request, and fix it
in the description rather than in the code.

## Why the exam cares

The guide's first knowledge item states it outright: **tool descriptions are the primary
mechanism a model uses for tool selection, and minimal descriptions lead to unreliable
selection among similar tools.**

So a tool nobody calls is almost never a code problem. It is a description problem, and
the guide's own worked example is two tools called `analyze_content` and
`analyze_document` with near-identical descriptions — which misroute not because either
is wrong but because nothing distinguishes them.

It also names a trap most people never consider: **system prompt wording can create
unintended tool associations.** A keyword-sensitive instruction elsewhere can override a
well-written description.

## Fundamentals

**Dispatch.** Choosing which of several implementations to run. *Why it matters here:*
with an LLM, dispatch happens in natural language against your descriptions, so the
description *is* the dispatch table. *Depth:* any treatment of dynamic dispatch; the
mechanism differs, the problem does not.

**Interface contract.** What a caller may rely on: inputs, outputs, failure modes. *Why
it matters here:* the description is the only place a model learns the contract, since it
cannot read your implementation. *Depth:* design-by-contract literature.

**Cohesion.** One unit doing one thing. *Why it matters here:* a generic tool covering
three jobs cannot be described precisely, which is why the guide's fix is to split it.
*Depth:* any treatment of single responsibility.

**Schema.** A machine-readable description of accepted input. *Why it matters here:* the
schema constrains shape; the description conveys *meaning*, and only one of those stops a
wrong-tool call. *Depth:* `json-schema.org`.

## The idea, before any code

**Write the description for a reader who cannot see the code**, because that is literally
the situation. Three things it must carry, and the guide names all three: what the tool is
for, what it expects, and **when to use it rather than the similar one next to it.**

That last clause is the one people omit, and it is the one that does the routing. "Reads a
file" describes a tool. "Reads a lesson file and lists the URLs it cites; use
`fetch_source` to retrieve those URLs" routes between two.

**Then look for overlap deliberately.** If two descriptions could plausibly answer the
same request, the model will sometimes pick either — and you will debug the
implementation of whichever one it chose.

**If you cannot describe a tool precisely, it is doing too much.** The guide's fix is
splitting a generic `analyze_document` into `extract_data_points`, `summarize_content`
and `verify_claim_against_source`. Three names you can tell apart, three contracts.

## The build

### Step 1 — name the boundary in the description

Course Doctor's first tool:

```python
"""Read a material file and list the documentation URLs it cites.

Returns the file's text, a content hash, and every URL found. Use this to find
out WHAT a lesson claims and WHERE it says the claim came from. It does NOT
fetch those URLs or check whether they still support the claim — call
fetch_source for that.
"""
```

The last sentence is the routing. It names a sibling and says when to prefer it, so a
request to "check whether this lesson is still accurate" does not stop here.

### Step 2 — describe every parameter by its failure

A parameter description that restates the type tells a caller nothing — and it passes any
check that only looks for non-empty text:

```
BAD:   path: "A string path to the file."
GOOD:  path: "Path to one material file, relative to the project root. An
        absolute path or one escaping the root is refused rather than read.
        Pass one file; this tool does not take a directory."
```

The second says what a *wrong* value does. That is the information a caller cannot get
anywhere else.

### Step 3 — hunt for overlap, then split or rename

List your tools with one-line purposes side by side. For any pair you could imagine the
same request matching, do one of two things — both named by the guide:

- **Rename and re-describe** to eliminate the overlap: `analyze_content` becomes
  `extract_web_results` with a web-specific description.
- **Split the generic one** into purpose-specific tools with defined input and output
  contracts.

### Step 4 — read the system prompt for interference

The guide names this as a skill: reviewing system prompts for keyword-sensitive
instructions that might override well-written tool descriptions. An instruction saying
"always search before answering" can pull a search tool into requests that needed
something else, and no amount of description-polishing on the other tool fixes it.

## Tips

Things the documentation does not tell you.

**A tool that is never called looks exactly like a tool that is broken.** Before
debugging the implementation, check whether the description would make *you* pick it for
the request you expected. Most of the time the answer is no.

**A parameter description that names the type passes a truthiness check and teaches
nothing.** If your test asserts descriptions are non-empty, it is asserting almost
nothing. Assert a length floor, and better, review that each one says what a wrong value
does.

**Describing what a tool does NOT do is the highest-value sentence you will write.** It
is the only thing that stops a near-neighbour being called, and it is almost always
missing.

**Two tools with 80% overlapping descriptions behave worse than one tool.** The
single tool is reliably chosen; the pair is chosen at random and you debug whichever one
you happened to open.

**Returning raw dictionaries publishes an empty output schema.** A caller then has to
*call* the tool to learn the shape of the reply, which is the one thing a schema exists to
prevent. Typed output models cost almost nothing and are the difference between a
documented surface and a guessable one.

## The anti-pattern

From the guide's objectives:

> **Ambiguous or overlapping tool descriptions causing misrouting**, with
> `analyze_content` against `analyze_document` as the named case.

And its companion:

> **Minimal descriptions**, which the guide ties directly to unreliable selection among
> similar tools.

The shape to recognise on exam day: when one option offers a clearer *description* and
another offers a change to the *implementation* or the *prompt*, the description is
usually the answer — because the guide states the description is the selection mechanism.

## What this lesson does not cover

- **Error responses** — lesson 2.2, and the guide treats it as its own task statement.
- **How many tools an agent should have** — lesson 2.3.
- **MCP configuration** — lesson 2.4.
- **The built-in tools** — lesson 2.5.
- **Writing the schema itself.** Domain 4 TS 4.3 treats JSON schemas properly.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.1.

| Claim | Source |
|---|---|
| Tool descriptions are the primary mechanism LLMs use for tool selection; minimal descriptions lead to unreliable selection among similar tools | EG §6, TS 2.1 |
| Descriptions should include input formats, example queries, edge cases and boundary explanations | EG §6, TS 2.1 |
| Ambiguous or overlapping descriptions cause misrouting, e.g. `analyze_content` vs `analyze_document` | EG §6, TS 2.1 |
| System prompt wording is keyword-sensitive and can create unintended tool associations | EG §6, TS 2.1 |
| Renaming and re-describing to eliminate functional overlap is a tested skill | EG §6, TS 2.1 |
| Splitting a generic tool into purpose-specific tools with defined input/output contracts, e.g. `extract_data_points`, `summarize_content`, `verify_claim_against_source` | EG §6, TS 2.1 |
| Reviewing system prompts for instructions that override tool descriptions is a tested skill | EG §6, TS 2.1 |
| Writing descriptions that differentiate purpose, expected inputs, outputs, and when to use one versus a similar alternative | EG §6, TS 2.1 |

---

# Lesson 2.2 — An error the agent can act on

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.2:** Implement structured error responses for MCP tools.

Lab artifact: Course Doctor's refusals carry a category, a retryable flag, and what was
attempted.

## What you will be able to do afterwards

Design a failure reply an agent can make a decision from — and distinguish, in your
return shape, a failed lookup from a successful one that found nothing.

## Why the exam cares

The guide's framing is sharp: **uniform error responses prevent the agent making
appropriate recovery decisions.** A generic "Operation failed" is not a small
infelicity; it removes the information the agent needed to choose between retrying,
asking a human, and moving on.

It names a four-way taxonomy — transient, validation, business, permission — and it names
a specific distinction as a tested skill: **access failures versus valid empty results.**
A timeout and a query that legitimately matched nothing are both "no data", and they call
for opposite responses. Collapsing them means an agent retries something that worked, or
gives up on something that would have succeeded.

## Fundamentals

**Error taxonomy.** Grouping failures by what the caller should *do*, not by where they
happened. *Why it matters here:* the four categories are a decision table, not a
filing system. *Depth:* HTTP's 4xx/5xx split is the same idea at a coarser grain.

**Idempotence and retryability.** Whether repeating an operation is safe and might help.
*Why it matters here:* `isRetryable` is the single most actionable field in a failure
reply. *Depth:* REST method semantics.

**Empty result versus failure.** A successful operation whose answer is "none" against an
operation that did not happen. *Why it matters here:* the guide calls this out explicitly,
and conflating them is the most common shape of this bug. *Depth:* the difference between
`404` and `200 []`.

**Fail loudly versus fail silently.** Whether a problem announces itself. *Why it matters
here:* returning empty results as success is named as an anti-pattern. *Depth:* the
principle of least astonishment in automation.

**Structured versus prose errors.** A reply with named fields against a sentence. *Why it
matters here:* an agent can branch on a field; it has to interpret a sentence. *Depth:*
Domain 4 TS 4.3 on schemas.

## The idea, before any code

**Ask what the caller should do differently, then make the reply say that.** Four
answers, which is why there are four categories:

- **Transient** — timeout, service unavailable. Retry. `isRetryable: true`.
- **Validation** — the input was wrong. Do not retry the same call; fix the input.
- **Business** — a policy says no. Do not retry at all, and the caller may need to
  explain why to a person, so the message has to be sayable out loud.
- **Permission** — not allowed. Retrying is pointless; escalate.

**Then decide what an empty answer means.** Did the lookup succeed and find nothing, or
did the lookup not happen? Those are different results and they need different shapes. If
your return type cannot express the difference, the agent cannot either.

**And a refusal is a result, not an exception.** An agent formats whatever it is handed. A
refusal thrown as a transport error gets summarised as "the tool failed", and whatever
remedy you wrote is lost on the way.

## The build

### Step 1 — a refusal with a category and a remedy

```python
class Refusal(BaseModel):
    """A refusal arrives as a normal result with an `error` field, not as a
    raised exception."""

    error: Literal["path_escapes_root", "not_a_file", "too_large", "unreadable"]
    message: str          # what happened, for a human
    guidance: str         # the cheapest correction, not a restatement of the rule
    category: Literal["transient", "validation", "business", "permission"]
    is_retryable: bool
    attempted: str        # what the tool tried, so a coordinator can report it
```

`guidance` is the field that earns its place. "Paths must be relative to the project
root" restates the rule. "Pass `course/domain-3-configuration/lesson-3-1-…md`" is the
correction.

### Step 2 — make the empty case unambiguous

```python
class MaterialReadingResult(BaseModel):
    urls: list[str]
    urls_found: int
```

A lesson citing no sources returns `urls: []` with `urls_found: 0` — **a finding about
the material, not an error.** The docstring says so, because the next reader will assume
otherwise.

And the complement: if the file could not be read, that is a `Refusal`, not an empty
list. Two different types, so the difference cannot be lost.

### Step 3 — recover locally, propagate what you could not

The guide's skill: a subagent implements local recovery for transient failures and
propagates only what it cannot resolve — **including what was attempted and any partial
results.**

So a worker that retried twice and failed does not return "failed". It returns the
failure type, the query it attempted, whatever partial findings it did get, and
alternatives it did not try. The coordinator can then decide between re-delegating with a
narrower query and reporting a gap, which it cannot do from "failed".

### Step 4 — annotate coverage, not just content

For a synthesis step, the guide names structuring output **with coverage annotations
indicating which findings are well-supported and which topic areas have gaps due to
unavailable sources.** A report that silently omits what it could not reach reads as
complete.

## Tips

Things the documentation does not tell you.

**A refusal raised as an exception loses your `guidance` field.** The agent reports "the
tool failed" and the remedy you carefully wrote never reaches anyone. Return it.

**`is_retryable: false` on a business rule saves more time than any retry policy.** Three
automatic retries against a policy violation is three identical rejections and a slower
answer.

**Write `guidance` as the cheapest correction, never as a restatement of the rule.** "The
path must be inside the project" is the rule. The fix is an example path.

**An empty list and a failed read must be different types, not the same type with a
flag.** A flag gets dropped by the next caller; a type cannot be.

**Populate "what this does not show" on SUCCESS, not only on failure.** A successful reply
that cannot say what it did not cover is the quietest failure in this domain — and it is
the one your own reports will have, because nobody writes that field for the happy path.

## The anti-pattern

The guide names two directly, and they are opposites:

> **Silently suppressing errors — returning empty results as success.**

> **Terminating an entire workflow on a single failure.**

Both are named anti-patterns, which tells you the answer is neither extreme: recover
what you can locally, propagate what you cannot with enough context to decide, and never
let a failure render as a clean result.

And the one underneath them:

> **A generic error status that hides context from the coordinator**, "search
> unavailable" being the guide's own example.

## What this lesson does not cover

- **Error propagation across a multi-agent system** — Domain 5 TS 5.3 treats it as the
  subject; here it is the shape of one tool's reply.
- **Retry and validation loops for extraction** — Domain 4 TS 4.4.
- **Escalation to a human** — Domain 5 TS 5.2.
- **Tool descriptions** — lesson 2.1.
- **The `isError` flag's wire-level detail.** Named by the guide as the MCP pattern for
  communicating failure; the protocol specifics are out of scope for Foundations.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.2.

| Claim | Source |
|---|---|
| The MCP `isError` flag communicates tool failures back to the agent | EG §6, TS 2.2 |
| Four error categories: transient, validation, business, permission | EG §6, TS 2.2 |
| Uniform error responses such as a generic "Operation failed" prevent appropriate recovery decisions | EG §6, TS 2.2 |
| Structured metadata prevents wasted retry attempts by distinguishing retryable from non-retryable | EG §6, TS 2.2 |
| Returning `errorCategory`, an `isRetryable` boolean, and human-readable descriptions | EG §6, TS 2.2 |
| `retriable: false` plus customer-friendly explanations for business rule violations | EG §6, TS 2.2 |
| Subagents recover locally from transient failures and propagate only unresolvable errors, with partial results and what was attempted | EG §6, TS 2.2 |
| Distinguishing access failures from valid empty results is a tested skill | EG §6, TS 2.2 |
| Structuring synthesis output with coverage annotations for well-supported findings versus gaps from unavailable sources | EG §6, TS 2.2 and TS 5.3 |
| Silently suppressing errors, and terminating a workflow on a single failure, are both named anti-patterns | EG §6, TS 5.3 |

---

# Lesson 2.3 — Fewer tools, and forcing the first one

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.3:** Distribute tools appropriately across agents and configure tool
choice.

Lab artifact: Course Doctor's tools scoped per agent role, with one extraction forced to
run first.

## What you will be able to do afterwards

Decide which agent in a system should hold which tools, and say what `tool_choice` buys
in each of its three settings.

## Why the exam cares

The guide gives a number, which is unusual enough to be worth noticing: **giving an agent
access to too many tools — "18 instead of 4-5" — degrades tool selection reliability by
increasing decision complexity.**

That single figure is the heart of the task statement, and it has a direct consequence for
lesson 2.4: if every configured MCP server's tools are live simultaneously, then adding
servers quietly moves you toward the eighteen.

The second half is `tool_choice`, and the guide names three settings precisely. Expect an
item where the right answer is forcing a specific tool and the tempting one is a firmer
instruction.

## Fundamentals

**Decision complexity.** The cost of choosing grows with the number of options. *Why it
matters here:* it is the stated mechanism — more tools, less reliable selection. *Depth:*
any treatment of choice overload; the effect transfers.

**Specialisation.** Giving a component only what its role needs. *Why it matters here:*
the guide observes agents with tools outside their specialisation tend to misuse them.
*Depth:* single responsibility again, one level up.

**Scoped access.** Permission narrowed to a role rather than granted globally. *Why it
matters here:* this is least privilege applied to an agent's toolbox. *Depth:* RBAC
literature.

**Forced dispatch.** Requiring a specific call rather than letting the model choose. *Why
it matters here:* that is `tool_choice` with a named tool, and it is a guarantee where a
prompt is a request. *Depth:* Domain 4 TS 4.3, which uses the same mechanism for
structured output.

## The idea, before any configuration

**Give each agent the tools its role needs and nothing else.** The guide's own example of
the failure is a synthesis agent attempting web searches — not because it is broken, but
because the tool was there.

**Then handle the high-frequency exception deliberately.** A pure separation forces every
cross-role need through the coordinator, which is a round trip. The guide's answer is a
*scoped cross-role tool*: give the synthesis agent a narrow `verify_fact` and route the
complex cases through the coordinator anyway. One tool, one purpose, not a general
capability.

**Replace generic tools with constrained ones.** The guide's example is swapping
`fetch_url` for `load_document` that validates document URLs. Same job, smaller blast
radius, and a description you can write precisely — which loops straight back to 2.1.

**And when order matters, force it.** If metadata extraction must happen before
enrichment, a prompt asking for that order has a non-zero failure rate. `tool_choice`
naming the tool does not.

## The build

### Step 1 — scope by role

Course Doctor's roles and their tools:

```
coordinator   : Task, read_manifest                      (delegates; does not fetch)
reader        : read_material_file                       (reads; does not fetch)
fetcher       : fetch_source                             (fetches; does not judge)
synthesiser   : write_findings, verify_claim             (judges; narrow cross-role tool)
```

Four roles, two to three tools each — inside the guide's 4–5 band rather than near its
eighteen. The synthesiser's `verify_claim` is the deliberate scoped exception: it is
high-frequency, and routing every instance through the coordinator would double the
traffic for no judgement gain.

### Step 2 — the three `tool_choice` settings

| Setting | Meaning |
|---|---|
| `"auto"` | The model may call a tool **or return text instead**. |
| `"any"` | The model **must** call a tool, but chooses which. |
| `{"type": "tool", "name": "..."}` | The model must call **that** tool. |

Read the first row again, because it is where the exam item lives: under `auto`, "please
always use the tool" is a request the model can decline by answering in prose. If you need
structured output rather than a sentence, `any` guarantees a tool call.

### Step 3 — force the one that must go first

```python
tool_choice = {"type": "tool", "name": "extract_metadata"}
```

The guide's own case: force `extract_metadata` so it runs before enrichment, then handle
the subsequent steps in follow-up turns. The forcing applies to one turn; the sequence is
built from turns.

### Step 4 — count before you add a server

Every configured MCP server's tools are available at once. So the audit is: list what each
agent can actually see, and if the number has drifted toward the teens, the fix is
narrowing per role — not better prompting.

## Tips

Things the documentation does not tell you.

**`tool_choice: "auto"` plus "always call the tool" is not a guarantee, and it fails
intermittently.** It works most of the time, which is worse than failing always, because
you will ship it.

**An agent misusing a tool outside its specialisation is a configuration finding, not a
prompt finding.** The guide's framing is that agents *tend* to misuse such tools. Removing
the tool is one line; teaching the agent not to reach for it is an ongoing argument.

**Forcing a tool constrains one turn, not a sequence.** If you need A then B, that is a
forced call followed by another turn — not one call with a plan in it.

**The 4–5 versus 18 figure is the most quotable thing in this domain.** It is also a
*modelling* claim in the guide rather than a measurement you can reproduce, so quote it as
the guide's number rather than as physics.

**A scoped cross-role tool beats both purity and generosity.** Full separation costs round
trips; shared access costs misuse. One narrow tool for the frequent case, coordinator for
the rest.

## The anti-pattern

From the guide's objectives:

> **Giving one agent access to too many tools** — 18 where 4–5 would do — degrading
> selection reliability.

> **Agents holding tools outside their specialisation**, which they tend to misuse.

And the `tool_choice` form, which is the same shape as every other failure in this course:

> **Relying on an instruction where a setting would guarantee it.**

A prompt asking the model to always call a tool, under `auto`, is context. `any` is a
control. On exam day, when one option is firmer wording and another is a configuration
value, the configuration is the answer.

## What this lesson does not cover

- **Tool descriptions** — lesson 2.1, and the first thing to fix if selection is
  unreliable *within* a small tool set.
- **MCP server configuration and scoping** — lesson 2.4.
- **Coordinator and subagent architecture** — Domain 1 TS 1.2 and 1.3. Here distribution
  is a configuration decision, not a system design.
- **Using `tool_choice` for structured output** — Domain 4 TS 4.3, same mechanism,
  different purpose.
- **Built-in tools** — lesson 2.5.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.3.

| Claim | Source |
|---|---|
| Too many tools (18 instead of 4-5) degrades tool selection reliability by increasing decision complexity | EG §6, TS 2.3 |
| Agents with tools outside their specialisation tend to misuse them, e.g. a synthesis agent attempting web searches | EG §6, TS 2.3 |
| Scoped tool access: only the tools a role needs, with limited cross-role tools for high-frequency needs | EG §6, TS 2.3 |
| `tool_choice` options are `"auto"`, `"any"`, and forced selection `{"type": "tool", "name": "..."}` | EG §6, TS 2.3 |
| Under `"auto"` the model may return text instead of calling a tool | EG §6, TS 4.3 |
| `"any"` guarantees the model calls a tool rather than returning conversational text | EG §6, TS 2.3 |
| Forcing a specific tool to run first, e.g. `extract_metadata` before enrichment, then processing subsequent steps in follow-up turns | EG §6, TS 2.3 |
| Replacing generic tools with constrained alternatives, e.g. `fetch_url` with `load_document` that validates document URLs | EG §6, TS 2.3 |
| Providing a scoped cross-role tool such as `verify_fact` for the synthesis agent while routing complex cases through the coordinator | EG §6, TS 2.3 |
| Tools from all configured MCP servers are available simultaneously | EG §6, TS 2.4 |

---

# Lesson 2.4 — Wiring a server in, and what a populated `/mcp` does not prove

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.4:** Integrate MCP servers into Claude Code and agent workflows.

Lab artifact: Course Doctor's server wired at project scope, with its credential supplied
by the environment rather than written down.

## What you will be able to do afterwards

Configure a server at the right scope, pass it a secret without committing one, and say
what a server appearing in `/mcp` does and does not tell you.

## Why the exam cares

The guide names three things precisely: project-level `.mcp.json` for shared team tooling
against user-level `~/.claude.json` for personal and experimental servers, environment
variable expansion for credentials, and that **tools from all configured servers are
discovered at connection time and available simultaneously.**

That last one is the setup for a question. If every server's tools are live at once, then
adding servers is not free — it is Domain 2's own `tool_choice` problem arriving by the
back door, which lesson 2.3 covers.

## Fundamentals

**Client and server.** The client — Claude Code — connects to a server, asks what tools
it has, and calls them. The server does the work. *Why it matters here:* configuration is
entirely about telling the client where servers are. *Depth:* the protocol spec at
`modelcontextprotocol.io`.

**Transport.** How the two talk: `stdio` spawns a local process and speaks over its pipes;
`http` and `sse` reach a URL. *Why it matters here:* it decides which config fields apply
— `command` and `args` for stdio, `url` and `headers` for the rest. *Depth:* same spec.

**Environment variables.** Named values supplied by the shell rather than written in a
file. *Why it matters here:* the whole secret-handling answer. *Depth:* the twelve-factor
config chapter.

**Capability discovery.** Asking a server what it offers rather than being told in
advance — `tools/list`, `prompts/list`, `resources/list`. *Why it matters here:* it is why
a server's tool list can be present without the server being connected. *Depth:* the spec.

**Scope.** Who a configuration applies to. *Why it matters here:* same three-way split as
Domain 3, different file. *Depth:* lesson 3.1.

## The idea, before any files

**Who needs this server?** The team gets `.mcp.json`, committed. You alone get the user
or local scope in `~/.claude.json`. The guide frames the second as the experimental slot —
how you trial a server without pushing it on anyone.

**Where does the secret live?** Never in the file. The file names a variable; the
environment supplies the value. `.mcp.json` is committed, so a literal key there is a
published key, and rotating it becomes the cheapest part of a bad afternoon.

**What does the server's presence actually mean?** This is the question this lesson exists
for, and the answer is less than you would assume. See step 3.

## The build

### Step 1 — project scope, with the secret by reference

`.mcp.json` at the repository root:

```json
{
  "mcpServers": {
    "course-doctor": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "-m", "course_doctor.server"],
      "env": {
        "COURSE_DOCTOR_ROOT": "${CLAUDE_PROJECT_DIR}"
      }
    }
  }
}
```

Expansion works in `command`, `args`, `env`, `url` and `headers`, in two forms:
`${VAR}`, and `${VAR:-default}` which falls back when the variable is unset.

Three scopes, and they are easy to confuse because two share one file: **project** is
`.mcp.json` at the root and is shared via version control; **user** is `~/.claude.json`
globally and applies to all your projects; **local** is also `~/.claude.json` but stored
under this project's path, so it is this project only and not shared.

### Step 2 — the credential rule, and its boundary

For a **remote** server's `url` and `headers`, certain credential variables deliberately
read as **empty** rather than expanding:

> "Claude Code reads credential variables from your environment as empty rather than
> expanding them. This keeps a project's `.mcp.json` or a plugin from sending your Claude
> Code or cloud provider credentials to a server it names."

Covered: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `AWS_BEARER_TOKEN_BEDROCK`,
`HTTPS_PROXY`, `NPM_TOKEN` and others your environment carries.

**And here is the part to actually remember: your own names are not covered.** `API_KEY`
and `MY_CUSTOM_TOKEN` expand normally. So "credentials are protected in `.mcp.json`" is
the wrong lesson. The protection is specifically against a config file exfiltrating *the
credentials Claude Code itself uses*. Your service's token is yours to be careful with.

### Step 3 — what the server's presence proves

```
/mcp
```

Two documented behaviours make this weaker evidence than it looks.

**An unset variable with no default does not stop the server loading.** Claude Code
reports a missing-variable warning and uses the unexpanded `${VAR}` text as-is. So the
server registers, looks configured, and fails when a tool is first called — mid-task,
not at startup.

**A tool list can come from a cache rather than a connection.** A remote server you have
used before can show a status like `cached 2h ago · connects on first use · 5 tools`.
The tools appear immediately; the server is contacted when one is called.

So a populated `/mcp` tells you *a tool list exists*. It does not tell you the server is
reachable, authenticated, or currently working. **Call something.**

### Step 4 — expose a catalogue instead of making it guess

The guide names MCP **resources** as a way to expose content catalogues — issue
summaries, documentation hierarchies, database schemas — specifically to reduce
exploratory tool calls. An agent that can read a list of what exists does not need three
calls to discover it.

## Tips

Things the documentation does not tell you.

**A missing environment variable produces a mid-task failure, not a startup failure.**
The warning scrolls past, the server registers, and the break arrives when the tool is
called. If a server works for you and not a colleague, compare exported variables before
anything else — and check the shell you launched from, not the dotfile you think sets it.

**`${VAR:-default}` is the fix for the above and nearly free.** A default that is wrong
but present fails loudly at call time with a sensible message, where an unexpanded
`${VAR}` fails strangely.

**Both scopes are live at once, so a personal server can silently duplicate a team one.**
That is intended — it is how you trial a replacement — but two entries doing the same job
is a normal-looking state rather than an error, and you will debug the wrong one.

**An organisation `ask` control cannot be allowed away.** On claude.ai connectors, a tool
set to `ask` prompts on **every** call, in `acceptEdits`, `auto` and even
`bypassPermissions`, never offers to remember your choice, and an allow rule matching the
tool does not skip the prompt. A tool set to `blocked` is filtered out before Claude sees
it at all. If a tool prompts no matter what you configure, stop editing your settings.

**`timeout` is per-server and overrides the global.** Worth setting on a server whose
work is genuinely slow, rather than raising the global timeout for all of them.

## The anti-pattern

From the guide's objectives:

> **A secret written literally into a committed file.**

And the one this lesson adds, which the caching and warning behaviour hand you:

> **Reading a populated server list as a working server.**

Same shape as every other failure in this course: the absence of an error read as
evidence that nothing is wrong. A cached tool list and a live connection render
identically, and a server with an unexpanded variable looks exactly like one configured
correctly until something calls it.

The guide also names a third, worth knowing because it is counterintuitive:

> **Writing a custom server for a standard integration.**

Its stated preference is existing community servers for standard systems, with custom
servers reserved for team-specific workflows.

## What this lesson does not cover

- **Writing a server.** Lessons 2.1 and 2.2 are the tool surface and its error shapes.
- **Too many tools at once.** Lesson 2.3 — and it is the direct consequence of every
  server's tools being live simultaneously.
- **OAuth flows** for remote servers. Real, and not in this task statement's objectives.
- **MCP resources in depth.** Named here because the guide names them; the protocol
  detail is out of scope for Foundations.
- **Built-in tools** — lesson 2.5.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.4.

| Claim | Source |
|---|---|
| Project-level `.mcp.json` for shared team tooling vs user-level `~/.claude.json` for personal/experimental | EG §6, TS 2.4 |
| Environment variable expansion in `.mcp.json`, e.g. `${GITHUB_TOKEN}`, for credentials without committing secrets | EG §6, TS 2.4 |
| Tools from all configured servers are discovered at connection time and available simultaneously | EG §6, TS 2.4 |
| MCP resources expose content catalogues to reduce exploratory tool calls | EG §6, TS 2.4 |
| Prefer existing community servers for standard integrations; reserve custom ones for team-specific workflows | EG §6, TS 2.4 |
| Three scopes: local and user both in `~/.claude.json`, project in `.mcp.json` at the root | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| `${VAR}` and `${VAR:-default}` expand in `command`, `args`, `env`, `url`, `headers` | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| Credential variables read as EMPTY in a remote server's `url` and `headers`; `ANTHROPIC_API_KEY`, `AWS_BEARER_TOKEN_BEDROCK`, `NPM_TOKEN` and others covered — `API_KEY` and `MY_CUSTOM_TOKEN` are NOT | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| An unset variable with no default still loads the server, warns, and uses the literal `${VAR}` | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| Discovery happens via `tools/list`, `prompts/list`, `resources/list` after connection | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| A cached server can show `cached 2h ago · connects on first use · 5 tools` and connects on first call | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| An organisation `ask` control prompts every call in all permission modes, never remembers, and is not skipped by an allow rule; `blocked` filters the tool out before Claude sees it | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |
| `timeout` is a per-server tool execution timeout overriding `MCP_TOOL_TIMEOUT` | [MCP docs](https://code.claude.com/docs/en/mcp), read 2026-10-17 |

---

# Lesson 2.5 — The built-in tools, and the two that are not there

**Domain 2: Tool Design & MCP Integration — 18% of CCAR-F**
**Task Statement 2.5:** Select and apply built-in tools (Read, Write, Edit, Bash, Grep,
Glob) effectively.

Lab artifact: tracing Course Doctor's own call path using the search strategy below,
rather than reading the whole package.

## What you will be able to do afterwards

Choose the right tool for a search or an edit, build understanding of an unfamiliar
codebase without reading all of it — and know why a permission rule written for `Grep`
may match nothing on your machine.

## Why the exam cares

The guide's framing is selection: Grep for content, Glob for paths, Read and Write for
whole files, Edit for targeted changes. And it names a *strategy*, not just a mapping —
**start with Grep to find entry points, then Read to follow imports and trace flows,
rather than reading all files upfront.**

That is a context-management answer wearing a tooling hat, which is why it sits here and
pays off in Domain 5. Reading twenty files to answer one question spends the budget you
needed for the answer.

## Fundamentals

**Content search versus path search.** Finding text inside files against finding files by
name. *Why it matters here:* it is the Grep/Glob distinction and the guide's first
knowledge item. *Depth:* `man grep`, `man find`.

**Anchored editing.** Changing a file by matching surrounding text rather than by line
number. *Why it matters here:* it is how Edit works, and why it fails when the anchor is
not unique. *Depth:* any treatment of patch application.

**Incremental exploration.** Building understanding by following references from an entry
point. *Why it matters here:* it is the named strategy, and the alternative is reading
everything. *Depth:* Domain 5 TS 5.4.

**Default tool sets.** Which tools a session actually has, which is not the same as which
tools exist. *Why it matters here:* see the build. It is the whole surprise in this
lesson. *Depth:* `/docs/en/tools-reference`.

## The idea, before any commands

**Match the tool to the question.**

- *Where is this string?* → content search.
- *Which files are named like this?* → path search.
- *What does this file say?* → Read.
- *Change this one part* → Edit.
- *Replace the whole thing* → Write.

**Then sequence it.** The guide's strategy is Grep to locate, Read to follow. For tracing
a function across wrapper modules it names a two-step: identify all exported names first,
then search for each across the codebase. That beats opening files and hoping.

**And know what your session actually has.** Which is the part nobody expects.

## The build

### Step 1 — the surprise, and it matters for your permission rules

> **"On macOS, Linux, and WSL, Claude Code leaves Glob and Grep out of the default tool
> set, and Claude searches with `find` and `grep` through the Bash tool instead. In
> Claude's shell those two commands run embedded versions of `bfs` and `ugrep`, and the
> searches reach your hooks and permission rules as `Bash` calls."**

On Windows, `Glob` is in the default set. On the platforms most developers use, **it and
`Grep` are not.**

Three consequences:

1. A **permission rule** written for `Grep` matches nothing on macOS or Linux, because the
   search never arrives as a `Grep` call. It arrives as `Bash`.
2. A **hook** matching `Grep` never fires there either.
3. A **subagent tool list** naming `Grep` and `Glob` is naming tools that may not be in
   the set to begin with.

The exam guide's TS 2.5 discusses *selecting* Grep and Glob as though they are simply
available, which is true of the objective and not of every platform. Both facts are worth
holding: the guide tests the selection reasoning; the documentation tells you what your
session has.

### Step 2 — Edit, and the uniqueness rule

> **"`old_string` must appear exactly once. When it appears more than once, Claude either
> supplies a longer string with enough surrounding context to pin down one occurrence, or
> sets `replace_all: true` to replace them all."**

Which is why the guide names the fallback as a tested skill: **when Edit cannot find a
unique anchor, use Read followed by Write.** Read the whole file, write the whole file,
no anchor needed.

### Step 3 — explore incrementally

Tracing how a lesson's cited URLs reach the fetch layer:

```
1. search content for "urls"           -> finds the extractor and its tests
2. Read the extractor                  -> gives the function name and its caller
3. search content for that name        -> finds every call site
4. Read only those                     -> the flow, without the package
```

Four steps, four files read instead of twenty. The guide's words for the alternative are
*reading all files upfront*, and it names the incremental version as the skill.

### Step 4 — note what prompts and what does not

Permission behaviour differs by tool, and in Manual mode for paths inside the working
directory: `Read`, `Grep` and `Glob` do not prompt; `Edit`, `Write` and `Bash` do. But
**`Read`, `Grep` and `Glob` still prompt for paths outside the working directory**, and
`Bash` runs a built-in set of read-only commands without prompting even though it is
marked as requiring permission.

So "read tools are free" is nearly true and wrong at the boundary — which is the boundary
that matters, because that is where somebody reaches outside the project.

## Tips

Things the documentation does not tell you.

**If a permission rule or hook for `Grep` never fires, check your platform before your
syntax.** On macOS, Linux and WSL the search is a `Bash` call. This is the single most
expensive surprise in this task statement, and nothing warns you — the rule is valid, it
simply never matches.

**`Bash` is marked as requiring permission and still runs read-only commands without
prompting.** So the permission column tells you less than it appears to, in both
directions.

**An Edit that fails on a non-unique anchor is not an error to work around with a longer
anchor every time.** Sometimes the honest answer is Read plus Write, which the guide names
as the fallback — and it is more reliable on a file where the same line appears five
times.

**Reading a file to find out whether it is relevant is the expensive habit.** Search
first. The file list from a content search is itself information, and it costs almost
nothing next to opening each one.

**Export names first, then search each one** when tracing through wrapper modules. The
guide names this specifically, and it is the difference between finding every caller and
finding the ones you guessed.

## The anti-pattern

From the guide's objectives:

> **Reading all files upfront** instead of building understanding incrementally from an
> entry point.

And the one the documentation adds:

> **Assuming a tool is in your session's tool set because it exists.**

Same family as the rest of this course: configuration that looks correct and does nothing.
A rule naming a tool the session does not have is not an error — it is silently inert,
which is the worst of both.

## What this lesson does not cover

- **Context management as a subject** — Domain 5, especially TS 5.4 on large codebases.
- **Subagents for exploration** — Domain 1 TS 1.3, and lesson 3.4 for the `Explore` agent.
- **Permission rule syntax** in depth. Named here for where tool names appear; the rules
  themselves are configuration rather than tool selection.
- **Custom tools via MCP** — lessons 2.1 through 2.4.
- **Every built-in tool.** There are far more than six. This covers the six the task
  statement names, plus the availability fact that changes how two of them behave.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 2.5.

| Claim | Source |
|---|---|
| Grep for content search; Glob for file path pattern matching; Read/Write for full file operations; Edit for targeted modifications using unique text matching | EG §6, TS 2.5 |
| When Edit fails due to non-unique text matches, using Read + Write as a fallback | EG §6, TS 2.5 |
| Building codebase understanding incrementally — Grep for entry points, then Read to follow imports — rather than reading all files upfront | EG §6, TS 2.5 |
| Tracing function usage across wrapper modules by identifying exported names, then searching each across the codebase | EG §6, TS 2.5 |
| Selecting Glob for files matching naming patterns, e.g. `**/*.test.tsx` | EG §6, TS 2.5 |
| "On macOS, Linux, and WSL, Claude Code leaves Glob and Grep out of the default tool set, and Claude searches with `find` and `grep` through the Bash tool instead... the searches reach your hooks and permission rules as `Bash` calls." | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| On Windows, Glob is part of the default tool set | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| Tool names are the exact strings used in permission rules, subagent tool lists and hook matchers | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| Edit: "`old_string` must appear exactly once"; otherwise more surrounding context or `replace_all: true` | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| `Read`, `Grep` and `Glob` do not prompt inside the working directory but still prompt outside it; `Bash` is marked as requiring permission yet runs a built-in read-only command set without prompting | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |
| `Read` reads file contents; `Write` creates or overwrites files; `Bash` executes shell commands; `Edit` makes targeted edits | [tools reference](https://code.claude.com/docs/en/tools-reference), read 2026-10-17 |

---

# Lesson 3.1 — Where an instruction lives decides who gets it

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
**Task Statement 3.1:** Configure CLAUDE.md files with appropriate hierarchy, scoping,
and modular organization.

Lab artifact: the Course Doctor repository gets its instructions, split so that only the
relevant ones load.

## What you will be able to do afterwards

Diagnose why a teammate is not getting an instruction you wrote, and put it at the level
that fixes it — without guessing.

And one thing more important than any of the file paths: say, correctly, what a
`CLAUDE.md` can and cannot make happen.

## Why the exam cares

The guide puts this first in the domain, and its own stated skill is **"diagnosing
configuration hierarchy issues (e.g., a new team member not receiving instructions
because they're in user-level rather than project-level configuration)."**

Read that carefully, because it tells you the shape of the question. You will not be
asked to recite file paths. You will be given a symptom — someone is not getting a rule
— and asked which level it belongs at. The test is never "how important is this rule."
It is **"who does it apply to."**

Get it backwards and nothing errors. It applies to the wrong people, silently, which is
why it makes a good exam item and a bad afternoon.

## Fundamentals

Skip what you know. Here so a newcomer has somewhere to go and a senior gets the
one-line refresh.

**Configuration scope.** Whether a setting belongs to you, to this project, or to your
organisation. *Why it matters here:* scope is the entire subject of this task statement,
and nearly every mistake in it is a scope mistake. *Depth:* any tool with both a home
dotfile and a committed config — `git`, `ssh`, `editorconfig` — resolves the same way.

**Context versus control.** A *control* prevents an action. *Context* informs a
decision. *Why it matters here:* this is the distinction the lesson turns on, and the
documentation states it outright — see the build. *Depth:* `/docs/en/hooks-guide`, which
is where the controls live.

**Version control hygiene.** Which files belong in the repository, which belong only on
your machine, and which belong in neither. *Why it matters here:* it is what makes the
user/project split meaningful rather than cosmetic. *Depth:* `git`'s own `.gitignore`
documentation.

**Glob patterns.** `*`, `**` and `?` matching file paths; `src/**/*.py` is every Python
file at any depth under `src`. *Why it matters here:* `.claude/rules/` files select the
files they apply to with a glob. *Depth:* `man 7 glob`. Lesson 3.3 is the full treatment.

**Monolith versus modules.** One large instruction file against several focused ones
loaded as needed. *Why it matters here:* the guide names `.claude/rules/` as the
alternative to a monolithic `CLAUDE.md`, and the reason is token cost rather than
tidiness. *Depth:* Domain 5, where context budget is the subject.

## The idea, before any files

Three questions, in this order.

**Who does this apply to?** Only you, or everyone who clones the repository? That single
question picks the level, and it is the one the exam asks.

**Is it context, or is it a control?** This is the distinction that catches people, and
the documentation is unusually blunt about it:

> "Claude treats them as context, not enforced configuration. **To block an action
> regardless of what Claude decides, use a PreToolUse hook instead.**"

So a line in `CLAUDE.md` saying *never force-push* is a request. A hook is a refusal.
Writing the request and believing you installed the refusal is the most expensive
mistake available in this domain, and it fails quietly — nothing blocks, because nothing
was ever configured to block.

**When does it need to load?** Everything loaded costs context, and context spent is
unavailable for the work. An instruction that matters only when editing test files
should not load while you edit the API.

## The build

### Step 1 — the project instruction file

```
mkdir course-doctor && cd course-doctor
git init
printf '# Course Doctor\n\nPython 3.12+. Tests live in tests/.\n' > CLAUDE.md
```

Project instructions go at `./CLAUDE.md` or `./.claude/CLAUDE.md`. Either is the
project level; both are committed; everyone who clones gets them.

### Step 2 — know what loads, and when

Two behaviours to hold, because they are the ones the symptom questions rest on.

**Files in the hierarchy above your working directory load at launch. Files in
subdirectories load on demand.** So a `CLAUDE.md` three directories up is already in
context when the session starts, and one in `src/api/` arrives only when you touch
something there.

**A project file does not suppress a parent one — they combine.** This is worth
verifying yourself rather than believing, and it is verifiable: put a line in a parent
directory's `CLAUDE.md`, start a session in the child, and look. Both load.

### Step 3 — split the monolith

As the instruction file grows, move topic-specific material into `.claude/rules/`:

```
mkdir -p .claude/rules
```

A rules file carries frontmatter naming the paths it applies to, so it loads only when a
matching file is in play. `paths: ["tests/**/*"]` keeps your testing conventions out of
context while you are editing something else. Lesson 3.3 is the full treatment; what
matters here is that it is the documented alternative to one large file.

The guide also names **`@import`** for referencing external files to keep `CLAUDE.md`
modular — importing a standards file into each package's instructions. See the sources
note below: that syntax is in the exam guide and I have not yet located it in the
documentation, so it is listed as an objective and not yet taught here.

### Step 4 — look at what actually loaded

```
/memory
```

Browse and open the instruction files the session is working from. And `/status` is
worth a look for a different reason: **if an instruction file is over the recommended
length you get a warning at startup and in `/status`, and you also get one when several
files that are each fine add up past a combined limit.** Each `CLAUDE.md`, each rules
file and each `@path` import counts separately toward that.

That is a real failure mode: no single file looks wrong, and together they are too much.

## Tips

Things the documentation does not tell you.

**There is no precedence between user and project rules, and this is the one to
remember.** The documentation says it plainly: *"Neither set overrides the other: if a
user rule and a project rule conflict, Claude may follow either one, so keep the two
consistent."* Everyone assumes the more specific level wins. It does not. If you have a
conflict, you do not have a precedence puzzle — you have a bug, and the fix is to remove
the conflict.

**A rule on one laptop is a personal habit, not a team convention.** The next person
does not inherit it, and you will not find out until their work diverges from yours for
reasons neither of you can see.

**Your own preferences in the project file get imposed on everyone who clones.** The
mirror of the mistake above, and the more annoying one to be on the receiving end of.

**A subdirectory instruction file is the hardest one to find later.** When something is
applying and you cannot see where it came from, you check the project file first and a
nested one last. Knowing they exist is most of the fix.

**Four short files can breach the limit that none of them breaches alone.** The combined
warning is easy to miss at startup. `/status` is where you look on purpose.

## The anti-pattern

From the guide's own skill statement for this task statement, the named failure is:

> **A new team member not receiving instructions because they are in user-level rather
> than project-level configuration.**

And the broader shape, which the documentation's own wording hands you:

> **Treating context as if it were a control.**

An instruction file asks. A hook prevents. If what you need is a guarantee — a
destructive command refused, a prerequisite enforced — then `CLAUDE.md` is the wrong
tool no matter how firmly it is worded, and on exam day an option offering a hook will
beat an option offering stronger instructions.

## What this lesson does not cover

- **`.claude/rules/` frontmatter and glob semantics in depth** — lesson 3.3.
- **Skills and slash commands** — lesson 3.2.
- **Hooks.** Named here because the context/control distinction is meaningless without
  them, taught in Domain 1 TS 1.5.
- **Auto memory.** Claude writes its own notes alongside the instructions you write.
  Adjacent, real, and not in this task statement's objectives.
- **`AGENTS.md`.** The documentation says Claude Code can read it in place of or
  alongside project instructions, with a table per file combination. Not in the exam
  guide's objectives for TS 3.1, so it is out of scope here — and I have an unresolved
  note claiming a `CLAUDE.md` suppresses it entirely, which that table may contradict.
  Unresolved is recorded as unresolved.
- **`@import`** — an objective, not yet traced to documentation. See sources.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 3.1.

| Claim | Source |
|---|---|
| The hierarchy is user-level, project-level, and directory-level | EG §6, TS 3.1 |
| User-level instructions are not shared with teammates via version control | EG §6, TS 3.1 |
| `@import` references external files to keep CLAUDE.md modular | EG §6, TS 3.1 |
| `.claude/rules/` organises topic-specific rules as an alternative to a monolithic CLAUDE.md | EG §6, TS 3.1 |
| Diagnosing hierarchy issues is a tested skill, with the new-team-member symptom named | EG §6, TS 3.1 |
| `/memory` browses and opens the instruction files in use | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Project instructions live at `./CLAUDE.md` or `./.claude/CLAUDE.md` | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Files above the working directory load at launch; subdirectory files load on demand | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead." | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| "Neither set overrides the other: if a user rule and a project rule conflict, Claude may follow either one" | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Over-length warning at startup and in `/status`; separate combined-length warning; each CLAUDE.md, rules file and `@path` import counts separately | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |

**Outstanding, and stated rather than papered over:**

- [ ] **`@import` syntax.** The exam guide lists it under TS 3.1. Searched the memory
      documentation on 2026-10-17 and did not find it. It may be on another page, named
      differently, or the guide and the docs may disagree. **Not taught until resolved** —
      teaching a syntax from memory is the failure this course is about.
- [ ] The `AGENTS.md` per-combination table, for the scope note above.

**Verified by running it, 2026-10-13**, and now corroborated by the documentation above —
recorded as `OBSERVED` first and upgraded rather than quietly restated:

- A project `CLAUDE.md` does **not** suppress a parent one. Both loaded together.

---

# Lesson 3.2 — Packaging a procedure, and deciding what it may touch

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
**Task Statement 3.2:** Create and configure custom slash commands and skills.

Lab artifact: Course Doctor gets a `check-sources` skill that runs isolated and cannot
write.

## What you will be able to do afterwards

Package a repeatable procedure as a skill, choose its scope, restrict what it can reach,
and say what you give up by running it in a forked context.

## Why the exam cares

The guide lists two frontmatter options as explicitly tested — `context: fork` and
`allowed-tools` — and **both are about containment**, not convenience. It also names
`argument-hint`, and the choice between a skill and an always-loaded instruction file.

So the items here are not "how do I make a slash command." They are *should this be a
skill or a CLAUDE.md rule*, and *what should it be allowed to do*. Both are judgment,
and both have a defensible wrong answer sitting next to the right one.

## Fundamentals

**Procedure versus convention.** A procedure is a thing you *do* on request; a
convention is a thing that is *always true*. *Why it matters here:* it is the whole
skill-versus-instruction-file decision. *Depth:* lesson 3.1 covers the instruction-file
side.

**Least privilege.** Grant the narrowest access that lets the work happen. *Why it
matters here:* `allowed-tools` and `disallowed-tools` are this principle with a config
key. *Depth:* Saltzer and Schroeder's original paper is short and still clearest.

**Process isolation.** Running work in a separate context so its intermediate state does
not persist into yours. *Why it matters here:* that is `context: fork`. *Depth:* any
treatment of subprocess isolation transfers.

**Pre-approval.** Deciding in advance that an action does not need a prompt. *Why it
matters here:* `allowed-tools` pre-approves rather than expands — it removes the prompt
for things the skill was going to do anyway. *Depth:* `/docs/en/permissions`.

**Interface hints.** Telling a caller what arguments a thing takes before they get it
wrong. *Why it matters here:* `argument-hint` is autocomplete text, and it is the
cheapest usability fix in the whole domain.

## The idea, before any files

**Is this always true, or is it something I do?** An always-true convention belongs in
`CLAUDE.md` or a rules file and loads every session. A procedure belongs in a skill and
loads when invoked. Putting a procedure in the instruction file spends context on every
session for something you run weekly.

**What must it not be able to do?** The default is everything the session can do. A skill
that reads and reports has no business holding write tools, and saying so costs one line.

**Do I need the detail afterwards, or only the conclusion?** This is the fork decision
and the one people get wrong, because the cost is invisible until you hit it. A forked
skill returns its answer and **does not see your conversation history** — so it also
cannot be asked a follow-up about its own working.

## The build

### Step 1 — a skill, in the project

```
mkdir -p .claude/skills/check-sources
```

`.claude/skills/check-sources/SKILL.md`:

```yaml
---
name: check-sources
description: Verify every documentation URL in a lesson still resolves and still says what the lesson claims
argument-hint: [lesson-path]
context: fork
agent: Explore
allowed-tools: Read, Glob, Grep, WebFetch
---

Read the lesson at $ARGUMENTS. For each documentation URL it cites, fetch the
page and report whether it still supports the claim, contradicts it, or does
not address it. Report the URL and today's date for each. Do not edit anything.
```

Five frontmatter fields doing five distinct jobs. `name` sets what you type. `description`
is what Claude matches on to auto-invoke. `argument-hint` is the autocomplete text.
`context: fork` runs it isolated. `allowed-tools` pre-approves exactly four tools and
nothing else.

Project skills live at `.claude/skills/<name>/SKILL.md` and are committed, so the team
gets them. Yours alone go in `~/.claude/skills/<name>/SKILL.md`.

### Step 2 — understand what you just isolated

`context: fork` spawns a subagent. Four consequences, and the second is the one that
bites:

1. Separate context, so the skill's working does not land in your conversation.
2. **It does not see your conversation history.** The `SKILL.md` is its entire prompt, so
   it has to be self-contained. A skill that says "check the lesson we were just
   discussing" has no idea which one.
3. It runs in the **background by default** — you keep working and the result arrives.
   Set `background: false` to wait for it.
4. `agent` picks the type: `Explore` is read-only with a small context, `Plan` is
   analytical, `general-purpose` is the general case. Background forked skills also get
   a reduced toolset.

### Step 3 — invoke it three ways

```
/check-sources course/domain-3-configuration/lesson-3-1-claude-md-hierarchy.md
```

Typed with an argument, available as `$ARGUMENTS`. Claude can also invoke it itself when
a request matches the `description` — unless you set `disable-model-invocation: true`,
which is what you want for anything with a side effect like `/deploy` or `/commit`.

### Step 4 — know the legacy shape when you meet it

A single file at `.claude/commands/<name>.md` creates the same `/name` command. It still
works; it is the older form. Differences worth knowing: a command is one file where a
skill is a directory that can carry supporting files loaded only when needed; a skill
reloads live during a session where a command needs a restart; and plugins support
skills only.

The exam guide names project-scoped `.claude/commands/` versus user-scoped
`~/.claude/commands/` directly, so both shapes are fair game.

## Tips

Things the documentation does not tell you.

**`allowed-tools` pre-approves; it does not grant.** It removes the prompt for tools the
skill would have used anyway. To *restrict* what a skill can reach, you want
`disallowed-tools`, which removes tools from the pool. Reading the first as the second is
how a skill ends up with more reach than you think.

**A forked skill costs you the follow-up question.** You get the conclusion without the
debris, which is the point — then you cannot ask "which of those files was it?" without
running the whole thing again. Decide which you need before you fork.

**`description` is the routing logic, not documentation.** It is what Claude matches on
to auto-invoke. A vague description produces a skill that never fires, or one that fires
on the wrong request — and both look like the skill being broken rather than described
badly.

**`disable-model-invocation: true` is the line you want on anything destructive.**
Otherwise a skill named `/commit` can be chosen for you because your request sounded like
committing.

**Skills reload live; legacy commands do not.** If you are iterating on wording and
nothing is changing, check which shape you are editing before debugging the content.

## The anti-pattern

For this task statement the shape to recognise is:

> **An always-loaded instruction file holding a procedure you run occasionally.**

It works, and it spends context every session on something you use once a week. The
guide frames the choice as skills for on-demand task-specific workflows against
CLAUDE.md for always-loaded universal standards, so an exam option offering a skill for a
recurring *task* beats one offering a rule.

And the containment form:

> **A skill with the session's full tool access because nobody said otherwise.**

The default is everything. A read-and-report skill holding write tools is one
misunderstanding away from editing something, and the guide's own example of the fix is
limiting file-write operations to prevent destructive actions.

## What this lesson does not cover

- **Hooks.** The `hooks` frontmatter field exists; hooks are Domain 1 TS 1.5.
- **Subagents as an architecture** — Domain 1 TS 1.2 and 1.3. Here a forked skill is a
  configuration choice, not a system design.
- **Plan mode and the Explore agent as a planning tool** — lesson 3.4.
- **Plugin distribution.** Skills can ship in plugins as `/plugin-name:skill-name`. Out
  of scope for Foundations.
- **The full frontmatter list.** Around twenty fields exist; this lesson teaches the five
  the exam guide names and the two that change what a skill may touch.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 3.2.

| Claim | Source |
|---|---|
| Project-scoped commands in `.claude/commands/` vs user-scoped in `~/.claude/commands/` | EG §6, TS 3.2 |
| Skills in `.claude/skills/` with `SKILL.md` supporting `context: fork`, `allowed-tools`, `argument-hint` | EG §6, TS 3.2 |
| `context: fork` runs a skill in an isolated sub-agent context, preventing output polluting the main conversation | EG §6, TS 3.2 |
| Personal skill variants in `~/.claude/skills/` avoid affecting teammates | EG §6, TS 3.2 |
| Choosing skills (on-demand, task-specific) over CLAUDE.md (always-loaded, universal) is a tested judgment | EG §6, TS 3.2 |
| Project skills at `.claude/skills/<name>/SKILL.md`; personal at `~/.claude/skills/<name>/SKILL.md` | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |
| `context: fork` spawns a subagent that does NOT see conversation history; `SKILL.md` must be self-contained | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |
| Forked skills run in the background by default; `background: false` waits | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |
| `agent` selects `Explore` (read-only, small context), `Plan`, or `general-purpose` | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |
| `allowed-tools` pre-approves tools without prompting; `disallowed-tools` removes tools from the pool | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |
| `description` is what Claude uses to auto-invoke; `disable-model-invocation: true` prevents it | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |
| `.claude/commands/<name>.md` is the legacy form and creates the same `/name`; one file, no live reload, no plugin support | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |

---

# Lesson 3.3 — Rules that only load when they are relevant

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
**Task Statement 3.3:** Apply path-specific rules for conditional convention loading.

Lab artifact: Course Doctor's conventions split so that the test rules are absent from
context while you edit the library.

## What you will be able to do afterwards

Choose between a path-specific rule and a subdirectory instruction file for a given
convention, and say which one you chose and why in one sentence.

And demonstrate that a rule did **not** load — which is the harder and more useful half.

## Why the exam cares

The guide's own stated skill is **"choosing path-specific rules over subdirectory
CLAUDE.md files when conventions must apply to files spread across the codebase."**

That is a judgment item, and it has a clean discriminator. A subdirectory instruction
file is scoped by *location*. A path-specific rule is scoped by *pattern*. So the
question is always: are the files this convention governs **in one place**, or **spread
by type**?

Test files are the canonical example — they live beside the code they test, scattered
through the tree. There is no directory to put their conventions in. `**/*.test.tsx`
catches all of them regardless of where they sit, which is the thing a subdirectory file
structurally cannot do.

And the reason this sits in Domain 3 but pays off in Domain 5: **instructions cost
context.** A convention loaded while irrelevant is budget spent on nothing.

## Fundamentals

Skip what you know.

**Glob patterns.** Wildcards that match paths. `*` matches within one path segment;
`**` crosses segments; so `src/api/**/*` is everything at any depth under `src/api`, and
`**/*.test.tsx` is every file of that type anywhere. *Why it matters here:* the pattern
*is* the scoping mechanism, so a wrong glob is a rule that never loads. *Depth:*
`man 7 glob`, or your shell's pattern documentation.

**YAML frontmatter.** A short block of key/value metadata at the top of a file, fenced
by `---` lines. *Why it matters here:* it is where a rules file declares its `paths`.
*Depth:* `yaml.org`; you need only the mapping and list forms.

**Conditional loading.** Content read only when a trigger fires, rather than always.
*Why it matters here:* it is the whole mechanism. *Depth:* lazy loading in any build
system is the same idea with a different trigger.

**The context window as a budget.** Everything loaded occupies finite space, and what
you spend is unavailable for the work. *Why it matters here:* it is the reason the
mechanism exists at all. *Depth:* Domain 5, where this is the subject rather than a
consequence.

**Scoping by location versus by type.** Two different ways to say "this applies here."
*Why it matters here:* this is the exam's discriminator, stated above. *Depth:* none
needed — it is a distinction rather than a technology.

## The idea, before any files

One question decides it: **can you draw a directory around the files this convention
governs?**

If yes — everything under `terraform/`, say — a subdirectory instruction file is simpler
and needs no pattern.

If no, because the files are defined by *what they are* rather than *where they live*,
you need a pattern. Tests, migrations, generated files, anything with a naming
convention: all scattered by design.

The second question is cheaper and people skip it: **would this convention be noise on a
task that does not touch those files?** If yes, conditional loading is not tidiness, it
is the point.

## The build

Course Doctor has two sets of conventions that should not travel together: how its MCP
tools are written, and how its tests are written.

### Step 1 — a rule scoped by pattern

```
mkdir -p .claude/rules
```

`.claude/rules/tests.md`:

```
---
paths: ["tests/**/*"]
---

Tests that assert an ABSENCE must be mutated inverted: add the forbidden thing
and confirm the test fails. A test that passes because the thing is missing
goes on passing after it arrives.
```

`.claude/rules/mcp-tools.md`:

```
---
paths: ["src/course_doctor/server.py", "src/course_doctor/contracts.py"]
---

Every tool parameter description says what a WRONG value does, not what type
it is. A bare type restatement passes a truthiness check and tells a caller
nothing.
```

Two files, two patterns, neither loading unless a matching file is in play.

### Step 2 — prove the negative

This is the step that matters and the one almost everybody skips.

Start a session and touch nothing. Both rule files exist on disk. **Neither should be in
context**, because no matching file has been opened.

Then edit something under `tests/`. The test rule arrives. Then edit a file matching
neither pattern. It should not.

**Verifying only the matching case tells you something loaded. It does not tell you the
pattern is doing the selecting.** A glob with a typo matches nothing, loads nothing, and
reports nothing — and a rule that never fires looks exactly like a rule you have not
needed yet.

### Step 3 — choose deliberately, and write down which

For each convention, say in one line whether it is location-scoped or type-scoped:

- MCP tool conventions → two named files. Could be a subdirectory file; the pattern is
  more precise, because `src/course_doctor/` holds the library too and the library has
  no MCP dependency on purpose.
- Test conventions → `tests/**/*` today, and would become `**/*_test.py` the moment
  tests move beside the code they test. **Type-scoped, so pattern-scoped.**

## Tips

Things the documentation does not tell you.

**A rule that has never fired is indistinguishable from a rule with a broken glob.** The
only evidence you have a working pattern is having watched it not match something.

**There is no precedence between user rules and project rules.** The documentation is
explicit: *"Claude Code loads user-level rules before project rules... Neither set
overrides the other: if a user rule and a project rule conflict, Claude may follow either
one, so keep the two consistent."* Everyone assumes the more specific wins. A conflict is
not a precedence puzzle; it is a bug, and the fix is removing the conflict.

**Each rules file counts separately toward the combined instruction-length warning.**
Splitting one long instruction file into six rules files does not reduce the total if
they all match the file you are editing — it only helps when they *don't*. Splitting by
topic and splitting by path are different moves, and only the second buys context back.

**Pin the pattern you expect to change.** `tests/**/*` is a directory assumption wearing
a glob. The day tests move next to their code, the rule silently stops matching. A
pattern written against the file *type* survives the reorganisation; one written against
the current layout does not.

**Narrow patterns beat clever ones.** Two explicit filenames are easier to verify than
one regex-ish glob that covers both plus something you did not intend.

## The anti-pattern

From the guide's objectives for this domain, the failure is:

> **Every rule loading on every task regardless of what you are touching.**

The monolithic instruction file is the common form: one file, every convention,
always loaded. It works, it is simple, and it spends context on API conventions while
you edit a test.

The subtler form, and the one the task statement is actually pointing at:

> **Reaching for a subdirectory instruction file when the files are spread by type.**

It is the intuitive move — put the convention near the code — and it quietly covers only
the files that happen to live in that directory today. The convention appears to be in
force and is absent everywhere else, which is worse than not having written it, because
you believe it is handled.

## What this lesson does not cover

- **CLAUDE.md hierarchy and scoping** — lesson 3.1, and worth reading first.
- **The exact frontmatter schema and glob matching semantics.** Named as outstanding in
  the sources below. The `paths` key and the two example patterns are from the exam
  guide; I have not yet traced the full schema to a documentation page, so this lesson
  teaches the *decision* and demonstrates the *behaviour* rather than asserting the
  grammar.
- **Hooks.** A rule is context; a hook is a control. Lesson 3.1 covers the distinction,
  Domain 1 TS 1.5 covers hooks.
- **Context budget as a subject** — Domain 5.
- **Skills and slash commands** — lesson 3.2.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 3.3.

| Claim | Source |
|---|---|
| `.claude/rules/` files use YAML frontmatter `paths` fields containing glob patterns for conditional rule activation | EG §6, TS 3.3 |
| Path-scoped rules load only when editing matching files, reducing irrelevant context and token usage | EG §6, TS 3.3 |
| Glob-pattern rules are advantageous over directory-level CLAUDE.md for conventions spanning multiple directories | EG §6, TS 3.3 |
| Example patterns `paths: ["terraform/**/*"]` and `**/*.test.tsx` | EG §6, TS 3.3 |
| Choosing path-specific rules over subdirectory CLAUDE.md when conventions apply to spread-out files is a tested skill | EG §6, TS 3.3 |
| "Neither set overrides the other: if a user rule and a project rule conflict, Claude may follow either one" | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| Each CLAUDE.md, rules file and `@path` import counts separately toward the combined-length warning | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |
| `.claude/rules/` organises topic-specific rule files as an alternative to a monolithic CLAUDE.md | [memory docs](https://code.claude.com/docs/en/memory), read 2026-10-17 |

**Verified by running it, 2026-10-13** — recorded as `OBSERVED`, a weaker claim than a
citation:

- Both rule files were present on disk and **not** in context, because no matching file
  had been touched. This is the lesson's central claim and it is demonstrable rather
  than asserted.

**Outstanding:**

- [ ] The `.claude/rules/` frontmatter schema and exact glob matching semantics, from a
      documentation page. Until then this lesson does not state the grammar.

---

# Lesson 3.4 — Planning first, and when plan mode is not actually a block

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
**Task Statement 3.4:** Determine when to use plan mode vs direct execution.

Lab artifact: the Course Doctor work split into a planned phase and a directly executed
one, with the planning discovery isolated.

## What you will be able to do afterwards

Decide between planning and executing for a given task on a stated criterion rather than
by feel — and say, correctly, where plan mode enforces its blocks and where it only asks.

That second half is the part most people have wrong.

## Why the exam cares

This is a pure judgment task statement. The guide gives both sides concretely: plan mode
for "large-scale changes, multiple valid approaches, architectural decisions, and
multi-file modifications"; direct execution for "simple, well-scoped changes (e.g.,
adding a single validation check to one function)."

Its own worked examples are the giveaway for how items will read — **"library migrations
affecting 45+ files"** and **"a single-file bug fix with a clear stack trace"**. One of
those is not about size. A 45-file migration is expensive to get wrong because the wrong
approach gets applied consistently forty-five times.

The guide also names the **Explore subagent** here, for isolating verbose discovery
output to preserve main-conversation context. Planning is where context gets eaten.

## Fundamentals

**Cost of rework.** What it costs to discover a wrong direction late. *Why it matters
here:* it is the actual decision criterion, and it is not the same as task size. *Depth:*
any treatment of the cost-of-change curve.

**Read-only operations.** Actions that inspect without modifying. *Why it matters here:*
plan mode's whole proposition is that research is safe and edits are not. *Depth:*
`/docs/en/permissions#read-only-commands` lists the built-in set.

**Context budget.** Everything loaded occupies finite space. *Why it matters here:*
discovery is verbose, and a planning phase that fills the window leaves nothing for the
implementation. *Depth:* Domain 5.

**Delegation for isolation.** Handing verbose work to something else so only its
conclusion returns. *Why it matters here:* that is the Explore subagent's job.
*Depth:* lesson 3.2 for the forked-skill form, Domain 1 TS 1.3 for subagents proper.

**Control versus instruction.** Whether a thing is prevented or merely asked for. *Why it
matters here:* this is the fact that makes plan mode subtle, and it is below in the
build. *Depth:* lesson 3.1, where the same distinction decides what a `CLAUDE.md` can do.

## The idea, before any commands

**One question: if this goes the wrong way, how expensive is it to find out late?**

Not "is this big." Three cases from the guide, in order of how strongly they argue for
planning:

- **One obvious correct change**, a single-file fix with a clear stack trace. Planning
  buys a delay.
- **A wrong approach applied consistently to many files.** Plan first — not because it is
  large, but because forty-five correct-looking edits are forty-five things to undo.
- **Several defensible designs.** The strongest case. When more than one answer is
  reasonable, what you most need is to see which one is being chosen while it is still
  cheap to choose differently.

And the guide names a fourth move that is better than either pure option: **plan for the
investigation, then execute directly for the implementation.** The two are not exclusive.

## The build

### Step 1 — enter plan mode three ways

```
claude --permission-mode plan
```

In a running session, `Shift+Tab` cycles into it, or prefix a single prompt with `/plan`
to plan just that one. To make it a project default, set `defaultMode` to `plan` in
`.claude/settings.json`.

### Step 2 — what plan mode does

Claude reads files, runs shell commands to explore, and writes a plan. It does not edit
your source. When the plan is ready you get three choices: approve and use auto mode,
approve and review each edit individually, or keep planning and say what to change.
`Ctrl+G` opens the proposed plan in your editor so you can change it before Claude
proceeds.

Approving **exits** plan mode and switches the session to whichever mode the option
described. To plan again, cycle back.

### Step 3 — the fact almost nobody knows

Read this slowly, because it is the exam-relevant part and it is counterintuitive:

> **"In interactive terminal sessions with bypass permissions available, Claude Code also
> doesn't enforce plan mode's blocks. Claude is still instructed to plan without editing,
> but a file edit or shell command it attempts during planning runs without prompting."**

And the complement:

> **"Plan mode keeps its blocks wherever Claude Code runs without an interactive
> terminal, including non-interactive runs with `-p`, Agent SDK sessions, and
> conversations in the VS Code extension's chat panel."**

So plan mode is **a control in some contexts and an instruction in others.** In a
headless `-p` run or the Agent SDK it genuinely blocks. In an interactive terminal with
bypass permissions available, it is a request that Claude is very likely to honour and
nothing stops it from not honouring.

This is lesson 3.1's distinction again, in the place it costs the most: *"it did not edit
anything"* is not the same claim as *"it could not edit anything."*

### Step 4 — keep discovery out of your context

A planning phase on an unfamiliar codebase is almost all verbose reading. Delegate it:

```yaml
---
name: map-the-flow
context: fork
agent: Explore
---

Trace how a lesson's cited URLs reach the fetch layer. Report the files and
the call order. Do not propose changes.
```

`Explore` is read-only with a small context. The discovery happens elsewhere and only the
summary comes back, which is what leaves room for the implementation you are planning.

## Tips

Things the documentation does not tell you.

**Plan mode in an interactive terminal with bypass available is not a guarantee.** If
you need a hard block — demoing to someone, or running against something you cannot undo
— the enforcement you are relying on lives in headless and SDK contexts, not that one.

**Approving a plan changes your permission mode for the rest of the session.** It does
not return you to where you were. People approve a plan, keep working, and are surprised
that edits stop prompting an hour later.

**`Ctrl+G` is the most underused key here.** Editing the plan directly beats three rounds
of "no, keep planning" with a correction each time.

**Planning expensively is still a cost.** Discovery fills the window, and a plan produced
by a nearly full context is produced by the worst version of the session. That is the
argument for `Explore`, and it is why the guide pairs them.

**The guide's two examples are a template for the items.** "A single-file bug fix with a
clear stack trace" against "library migrations affecting 45+ files" — when an exam option
describes scope that precisely, it is telling you which side of the line it sits on.

## The anti-pattern

From the guide's own framing for this task statement:

> **Reaching for plan mode by task size rather than by the cost of being wrong.**

Big-therefore-plan is the intuitive rule and it is wrong in both directions: it plans
a large mechanical change with one obvious approach, and it executes directly on a small
change with three defensible designs — which is the one that actually needed the plan.

And the one this lesson adds, which the documentation hands you:

> **Treating plan mode as a guarantee in a context where it is not enforced.**

Same shape as believing a `CLAUDE.md` line blocks an action. The mode reads identically
in both contexts; only one of them stops anything.

## What this lesson does not cover

- **Auto mode and the classifier.** It changes what happens to shell commands during
  planning, and it is its own subject.
- **Every permission mode.** `acceptEdits`, `dontAsk`, `bypassPermissions` and the rest
  are adjacent; this task statement is plan versus direct.
- **Subagents as architecture** — Domain 1 TS 1.2 and 1.3. Here `Explore` is a context
  tool.
- **Sandboxing**, which interacts with what runs during planning.
- **Iterative refinement**, which is TS 3.5 and sits in the lesson after this one.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 3.4.

| Claim | Source |
|---|---|
| Plan mode is for large-scale changes, multiple valid approaches, architectural decisions, multi-file modifications | EG §6, TS 3.4 |
| Direct execution suits simple, well-scoped changes, e.g. a single validation check | EG §6, TS 3.4 |
| Worked examples: library migrations affecting 45+ files; a single-file bug fix with a clear stack trace | EG §6, TS 3.4 |
| The Explore subagent isolates verbose discovery output to preserve main-conversation context | EG §6, TS 3.4 |
| Combining plan mode for investigation with direct execution for implementation is a tested skill | EG §6, TS 3.4 |
| "Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source." | [permission modes](https://code.claude.com/docs/en/permission-modes), read 2026-10-17 |
| Enter via `Shift+Tab`, a `/plan` prefix, `claude --permission-mode plan`, or `defaultMode: plan` | [permission modes](https://code.claude.com/docs/en/permission-modes), read 2026-10-17 |
| Three approve options; approving exits plan mode and switches the session's permission mode | [permission modes](https://code.claude.com/docs/en/permission-modes), read 2026-10-17 |
| `Ctrl+G` opens the proposed plan in your editor | [permission modes](https://code.claude.com/docs/en/permission-modes), read 2026-10-17 |
| **"In interactive terminal sessions with bypass permissions available, Claude Code also doesn't enforce plan mode's blocks."** | [permission modes](https://code.claude.com/docs/en/permission-modes), read 2026-10-17 |
| **"Plan mode keeps its blocks wherever Claude Code runs without an interactive terminal, including non-interactive runs with `-p`, Agent SDK sessions, and conversations in the VS Code extension's chat panel."** | [permission modes](https://code.claude.com/docs/en/permission-modes), read 2026-10-17 |
| `agent: Explore` is read-only with a small context | [skills docs](https://code.claude.com/docs/en/skills), read 2026-10-17 |

---

# Lesson 3b — Iterating on purpose, and reviewing without yourself

**Domain 3: Claude Code Configuration & Workflows — 20% of CCAR-F**
Covers **TS 3.5** (iterative refinement techniques for progressive improvement) and
**TS 3.6** (integrate Claude Code into CI/CD pipelines). Episode 1 covers TS 3.1
through 3.4; these two complete the domain.

Written lesson. Lab artifact: Course Doctor gains a non-interactive invocation that
emits schema-valid JSON.

## What you will be able to do afterwards

Get a better result on the second attempt for a stated reason rather than by
rephrasing, and run the same agent in a pipeline where its output is parsed by a
machine instead of read by you.

## Why the exam cares

These two are a third of Domain 3 and they are the two that look least like
configuration, so they get skipped.

They also share a single idea, which is the reason to teach them together: **the
quality of what you get back is set by what you put in front of the model, not by how
firmly you ask.** TS 3.5 is that idea applied to your own iteration. TS 3.6 is the same
idea applied when there is no human in the loop to iterate at all.

Expect judgment items. "A reviewer's prose instructions produce inconsistent severity
classifications. What is the most effective fix?" has four plausible options, and the
tempting one — write firmer instructions — is the wrong answer the guide names.

## Fundamentals

Skip what you know. Here so a newcomer has somewhere to go and a senior gets a
one-line refresh.

**Few-shot examples.** Showing two or three worked input/output pairs instead of
describing the transformation. *Why it matters here:* the guide states concrete
examples are the most effective way to communicate an expected transformation when
prose is interpreted inconsistently. This is Domain 4's central subject and it arrives
here first. *Depth:* Domain 4, TS 4.2.

**Test-driven development.** Write the failing test first, then make it pass. *Why it
matters here:* TS 3.5 names test-driven iteration explicitly — write the suite
covering expected behaviour, edge cases and performance, then iterate by *sharing the
failures*. The test output is the specific feedback that prose cannot be. *Depth:* any
TDD treatment; the mechanics transfer unchanged.

**Non-interactive execution.** Running a program with no terminal attached, so nothing
can answer a prompt. *Why it matters here:* this is what `-p` is for, and it is why an
interactive invocation in CI hangs rather than fails. *Depth:* the distinction between
a login shell and a batch job — `ssh host command` versus `ssh host`.

**JSON Schema.** A machine-readable description of what a JSON document must contain.
*Why it matters here:* `--json-schema` is how a CI step gets output it can parse
rather than prose it has to scrape. *Depth:* `json-schema.org`; Domain 4 TS 4.3 treats
it as a subject.

**Reviewer independence.** The idea that the author of a thing is the worst person to
check it. *Why it matters here:* the guide states that a session which generated code
is less effective at reviewing its own changes than an independent instance. This is
the same reason human code review exists, and it is the most transferable idea in the
lesson. *Depth:* Domain 4 TS 4.6 covers multi-instance review architectures.

**Idempotence.** An operation that can be run twice with the same result as once.
*Why it matters here:* a CI step that re-runs on every push must not post the same
finding twice, which is why prior findings go into context. *Depth:* REST method
semantics explain it cleanly.

## The idea, before any commands

**For iteration: replace the adjective with an artifact.**

The instinct when a result is wrong is to describe the problem better. The guide says
the opposite works: give a concrete input and the output you expected. Two or three
pairs beats a paragraph, because a paragraph can be read several ways and a pair
cannot.

The same move in three forms, all named in TS 3.5:

- A **worked example** instead of a description of the transformation.
- A **failing test** instead of a description of the bug.
- An **interview** — have Claude ask you questions before implementing — instead of a
  description of the requirements, when you are in a domain unfamiliar enough that you
  do not yet know what you have left out.

And one decision that is genuinely a judgment call: **when problems interact, put them
all in one message; when they are independent, fix them one at a time.** Interacting
fixes applied sequentially fight each other, and each round undoes the last.

**For pipelines: the human is not there, so the contract has to be explicit.**

Three things change when nobody is watching. There is no one to answer a prompt, so
interactive mode hangs. There is no one to read prose, so output has to be parseable.
And there is no one to notice that the reviewer and the author are the same session —
which the guide calls out as a real degradation, not a stylistic preference.

## The build

### Part one — iterate with artifacts

Course Doctor's drift report is returning inconsistent severities. The tempting fix:

```
"Be more conservative about what you flag as high severity."
```

The guide specifically names this shape as ineffective — "be conservative" and "only
report high-confidence findings" do not improve precision. Replace it with examples:

```
Example 1
  input:  a lesson citing a quota of 10 GB; the doc now says 20 GB
  output: severity HIGH, reason "numeric claim contradicted by current doc"

Example 2
  input:  a lesson citing a console path that has been renamed
  output: severity MEDIUM, reason "navigation changed, concept intact"

Example 3
  input:  a lesson whose cited page 404s
  output: severity UNKNOWN, reason "could not verify; not evidence of error"
```

Three pairs, and the third is doing the most work — it demonstrates the
ambiguous case, which is what the guide says few-shot examples are for.

Then the test-driven form. Write the assertion first:

```
./scripts/run-tests.sh 2>&1 | tail -20
```

Share the failure text, not a description of it. The test output names the expected
value, the actual value and the line — three facts your paragraph would have
approximated.

### Part two — run it with no human in it

Non-interactive, with machine-readable output:

```
claude -p "Check the lessons in course/ against their cited sources" \
  --output-format json \
  --json-schema schema/findings.json
```

Three flags, three jobs. `-p` (`--print`) runs without an interactive session, so
nothing waits for input. `--output-format json` makes the result parseable.
`--json-schema` constrains it to a shape your pipeline already knows how to read, so a
later step can post findings as inline comments without scraping prose.

Three more flags decide what happens when the run misbehaves, and all three are
documented and print-mode only:

```
claude -p "..." --max-turns 10 --max-budget-usd 2.00 --permission-prompts none
```

`--max-turns` limits agentic turns and **exits with an error** when the limit is
reached. `--max-budget-usd` stops the run once estimated spend reaches the amount —
note *estimated*, against a client-side figure that can differ from your bill, and
spend can pass the cap, so leave headroom. `--permission-prompts none` says nobody can
answer, so Claude Code denies prompts rather than waiting on them.

That last one matters more than it looks. By default in print mode, prompts go to the
Agent SDK host or a `--permission-prompt-tool`. If neither exists, you want the denial
rather than the wait.

**And `CLAUDE.md` is how the CI run learns about your project** — testing standards,
fixture conventions, review criteria. A CI-invoked run has no conversation history to
draw on, so whatever is not in the repository's instructions is not available to it.
That is the same hierarchy from episode 1, doing its most load-bearing work in the
place you cannot watch.

Then the part people get wrong. **Do not have the session that generated the code
review it.** Run the review as an independent invocation with no prior context. And
when re-running after new commits, include the previous findings in context with an
instruction to report only new or still-unaddressed issues — otherwise every push
posts the same comments again.

## Tips

Things that cost somebody an hour. None is in the documentation.

**A missing `-p` in CI costs you the whole timeout, not a fast failure.** Without print
mode there is no one to answer a permission prompt, and the job's error names the
timeout rather than the flag. If a step takes exactly as long as your timeout setting,
suspect the invocation before anything else — and pass `--permission-prompts none` so a
prompt becomes a denial instead of a wait.

**"Be more conservative" is the instruction that feels like a fix and is not.** It
reads as a tightening and changes nothing measurable. The guide names it. When you
catch yourself adding an adverb to a prompt, you want an example instead.

**Redirect stderr or you lose the only useful line.** `> log.txt` saves stdout and
leaves the traceback on a stream nobody captured. `2>&1` is four characters.

**Re-running a review without the prior findings duplicates every comment.** The second
run has no memory of the first, so it is not repeating itself — it is seeing the
repository for the first time, again. Feeding yesterday's findings in is what makes it
incremental.

**The third few-shot example is the one that earns its place.** Two examples show the
format. The third, covering the ambiguous case, is what lets the model generalise
rather than pattern-match — which is the difference the guide is pointing at.

## The anti-pattern

The guide names these explicitly, and the shapes to recognise are:

> **Firmer prose where a concrete example is needed.**

"Be conservative", "only report high-confidence findings", "be more careful about
severity" — all named as failing to improve precision compared to specific categorical
criteria. On exam day, if one option is an adverb and another is an input/output pair,
the pair is the answer.

> **Self-review in the generating session.**

Asking the same instance to check its own work, or reaching for a "review your output
carefully" instruction, instead of an independent instance with no reasoning context.
The failure is not that the model is careless; it is that it retains the reasoning that
produced the thing and is therefore unlikely to question it.

> **Sequential fixes for interacting problems.**

Fixing three issues one at a time when each change affects the others, so every round
partially undoes the last. The published distinction is interacting versus independent,
and it decides the batching.

## What this lesson does not cover

- **Few-shot prompting as a subject.** Introduced here because TS 3.5 depends on it;
  Domain 4 TS 4.2 is where it is taught properly.
- **JSON Schema design.** Same — used here, taught in Domain 4 TS 4.3.
- **Multi-instance review architecture.** The *why* is here because TS 3.6 names it;
  the architecture is Domain 4 TS 4.6.
- **Batch processing.** Adjacent and tempting to bolt on. It is Domain 4 TS 4.5, and
  the Message Batches API has its own latency and tool-calling constraints.
- **A specific CI provider's syntax.** The task statement is Claude Code in a pipeline,
  not any one pipeline. The flags transfer; the YAML does not.
- **Cost figures.** None appear here. Any number would be one person's usage.

## Sources

CCAR-F exam guide **Version 1.0, effective July 2026**, §6:

| Claim | Source |
|---|---|
| Concrete input/output examples beat prose when prose is read inconsistently | EG §6, TS 3.5 |
| "Be conservative" style instructions fail to improve precision | EG §6, TS 3.5 and TS 4.1 |
| Test-driven iteration: suite first, then share failures | EG §6, TS 3.5 |
| The interview pattern surfaces unanticipated considerations | EG §6, TS 3.5 |
| Interacting issues in one message; independent issues sequentially | EG §6, TS 3.5 |
| `-p` / `--print` runs Claude Code non-interactively in pipelines | EG §6, TS 3.6 |
| `--output-format json` and `--json-schema` enforce structured output in CI | EG §6, TS 3.6 |
| CLAUDE.md supplies project context to a CI-invoked run | EG §6, TS 3.6 |
| A session that generated code is less effective at reviewing its own changes | EG §6, TS 3.6 |
| Including prior findings avoids duplicate PR comments on re-run | EG §6, TS 3.6 |
| `-p` / `--print`: "Print response without interactive mode" | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--output-format` takes `text`, `json`, `stream-json`; print mode only | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--json-schema` returns validated JSON matching a schema; print mode only | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--max-turns` limits agentic turns and exits with an error at the limit | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--max-budget-usd` stops on ESTIMATED spend; spend can pass the cap | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |
| `--permission-prompts none` denies prompts when nobody can answer | [CLI reference](https://code.claude.com/docs/en/cli-reference), read 2026-10-17 |

**Official documentation links — REQUIRED BEFORE PUBLICATION, not yet fetched.** Each
needs a URL and a read date, and per this repo's rule a live link is not a verified
claim: the page has to still say what the row claims. Deliberately left unfilled rather
than written from memory, which is the failure this course is about.

- [x] **CLI reference** — `-p`/`--print`, `--output-format`, `--json-schema`,
      `--max-turns`, `--max-budget-usd`, `--permission-prompts`. Fetched and quoted
      2026-10-17: https://code.claude.com/docs/en/cli-reference
- [ ] `/docs/en/headless` — "Turn off permission prompts in unattended runs", and bare
      mode. Named by the CLI reference; not yet fetched.
- [ ] CLAUDE.md and memory documentation, for the CI-context mechanism —
      https://code.claude.com/docs/en/memory (fetched 2026-10-17 for Domain 3 facts;
      the CI-context claim specifically is not yet confirmed from it)
- [ ] Any documented guidance on independent review instances

Everything in **Tips** is `OBSERVED`, not cited — behaviour measured on one version,
a weaker claim than a documentation URL, labelled as such per the existing convention.

---
