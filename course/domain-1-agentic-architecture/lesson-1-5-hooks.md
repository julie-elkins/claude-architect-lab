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

The other accepted value is `"continue"`, which is the default behaviour written down.
Setting it explicitly is worth doing on a hook you have decided may fail quietly, because
it records the decision instead of leaving it to be inferred from an absent key.

**And there is a version floor: `onFailure` requires Claude Code v2.1.295 or later.** On
anything older the key is simply not recognised — which means it is ignored, the hook
stays fail-open, and *the config file still reads as though the rule is enforced.* That is
this lesson's own failure mode applied to the fix for this lesson's failure mode. Check
`claude --version` before you rely on the line, and on a shared repo say which version the
hook config assumes, because a colleague on an older build gets different enforcement from
the same committed file and nothing tells either of you.

### Step 4 — know which events a block even applies to

Exit code 2 blocks `PreToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`
and a few others. It **does not** block `PostToolUse`, `PostToolUseFailure`,
`PermissionRequest` or `Notification`.

Which means: you cannot undo a tool call from `PostToolUse`. By then it has run. You can
rewrite what the model is told about it, and that is all. If something must not happen,
the hook belongs on `PreToolUse`.

**`onFailure: "block"` inherits that table with one exception worth knowing.** A failure
with `"block"` set does whatever exit code 2 does *on that event* — so on `PostToolUse` it
still cannot undo anything, because the limit is the event and not the setting. The
exception is `PermissionRequest`, where a blocked failure **denies the request** rather
than doing nothing. So `onFailure` is not a way to make a late event behave like an early
one; it is a way to stop a broken hook being read as a passing one.

## Tips

Things the documentation does not tell you plainly enough.

**Verify a hook by firing it, once, deliberately, the day you write it.** A hook that has
never fired is indistinguishable from a hook with a wrong path — in both cases nothing
happens and nothing complains.

**A hook that crashes is worse than no hook, because you believe you have one.** This is
the practical reason `onFailure: "block"` exists, and the reason to prefer a tiny hook
script over a clever one.

**A config key your Claude Code version does not know is ignored, not rejected.** This is
why `onFailure` needs a version check rather than trust. Generalise it: on any
settings file, a key that is too new for the running build fails open and looks correct in
review. The only honest check is firing the behaviour, which is the tip above.

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
| **`onFailure: "block"` makes each of those cases block the action instead** | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17; re-verified verbatim 2026-10-18 |
| `onFailure` accepts `"block"` or `"continue"`, and is settable on a `command` or `http` hook | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-18 |
| **"Requires Claude Code v2.1.295 or later"** for `onFailure` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-18 |
| With `"block"` set, a failure does what exit code 2 does on that event, except on `PermissionRequest`, where it denies the request | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-18 |
| Exit code 2 does not block `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` or `Notification` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| Hooks are configured in `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, managed policy, plugin `hooks/hooks.json`, or skill and subagent frontmatter | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
| Handler types are `command`, `http`, `mcp_tool`, `prompt` and `agent` | [hooks docs](https://code.claude.com/docs/en/hooks), read 2026-10-17 |
