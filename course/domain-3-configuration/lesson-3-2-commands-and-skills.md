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
