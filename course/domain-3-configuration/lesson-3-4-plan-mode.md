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

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

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
