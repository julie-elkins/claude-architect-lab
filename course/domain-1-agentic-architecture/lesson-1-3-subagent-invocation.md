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
| A non-fork subagent starts fresh: no conversation history, no previous file reads, receiving only a delegation message | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17; re-verified verbatim 2026-10-18 |
| A fork inherits the entire conversation — same system prompt, tools, model and message history | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| Required fields `name` and `description`; optional `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `memory`, `background` | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| `maxTurns` caps agentic turns and the output is marked partial | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| "Claude Code removes every other built-in tool from a background subagent, whether inherited or listed in the `tools` field" | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17; re-verified verbatim 2026-10-18 |
| The spawning tool is automatically removed at the depth limit, three layers by default | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
| A returned subagent result consumes the parent's context, and each subagent spends its own tokens | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |

**Outstanding:**

- [~] **Not resolvable by fetching, and now partly settled.** The guide's **appendix (§17)
      names "subagent spawning via Task tool, allowedTools configuration"** as in-scope —
      so `Task` is the guide's deliberate wording in two places, not a slip in one. The
      documentation names `Agent`, and the tools reference has no `Task` row. Both stand:
      answer `Task` for an exam item, write `Agent` in a settings file. The lesson teaches
      the requirement under both names, which is the whole of what is testable.
