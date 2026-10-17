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

- [~] **Settled as a two-layer description, not a conflict.** The guide's **appendix (§17)
      lists `stop_reason` values `"tool_use"` and `"end_turn"` under *Claude API***, which
      confirms it means the Messages API level deliberately. The SDK's *result* carries a
      `stop_reason` whose common values are `end_turn`, `max_tokens` and `refusal`, and
      describes loop termination through the no-tool-calls condition. Same mechanism, two
      altitudes, and an exam item framed as "Claude API" means the first. Nothing further
      to fetch.
