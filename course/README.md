# Build to Pass — the course

Twenty-nine lessons, one per task statement in the published CCAR-F exam guide
(**Version 1.0, effective July 2026**). Read them in this order; it is dependency
order, not exam-weight order, because the tools have to exist before the loop that
calls them.

**Each lesson is a `lesson.md` you can read start to finish.** Where a `script.md`
and `slides.md` sit beside it, those are production assets for the video version —
narration and deck. You do not need them to take the course.

Every lesson carries the same six-part shape: what you will be able to do afterwards ·
why the exam cares · **fundamentals** (skippable; glosses for a newcomer, a refresh for
a senior) · the build with real commands · **tips** the documentation does not tell you
· the published anti-pattern · what the lesson does not cover · sources.

## Status

**2 of 29 written.** Nothing below is a stub — a lesson appears as a link only when it
exists. The rest are listed so you can see the shape of the whole thing, and so I
cannot quietly drop one.

## Domain 3 — Claude Code Configuration & Workflows (20%)

| | Task statement | Lesson |
|---|---|---|
| 3.1 | Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization | planned |
| 3.2 | Create and configure custom slash commands and skills | planned |
| 3.3 | Apply path-specific rules for conditional convention loading | planned |
| 3.4 | Determine when to use plan mode vs direct execution | planned |
| 3.5 | Apply iterative refinement techniques for progressive improvement | [written](episode-01b-iteration-and-pipelines/lesson.md) |
| 3.6 | Integrate Claude Code into CI/CD pipelines | [written](episode-01b-iteration-and-pipelines/lesson.md) |

TS 3.1 through 3.4 are currently covered by the **video script** at
[episode-01-claude-code-configuration/](episode-01-claude-code-configuration/), which
teaches all four mechanisms live. It is a shooting script rather than a written lesson,
and splitting it into four `lesson.md` files is the next work.

## Domain 2 — Tool Design & MCP Integration (18%)

| | Task statement | Lesson |
|---|---|---|
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries | planned |
| 2.2 | Implement structured error responses for MCP tools | planned |
| 2.3 | Distribute tools appropriately across agents and configure tool choice | planned |
| 2.4 | Integrate MCP servers into Claude Code and agent workflows | planned |
| 2.5 | Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively | planned |

## Domain 1 — Agentic Architecture & Orchestration (27%)

The largest slice of the exam, and it cannot come first.

| | Task statement | Lesson |
|---|---|---|
| 1.1 | Design and implement agentic loops for autonomous task execution | planned |
| 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns | planned |
| 1.3 | Configure subagent invocation, context passing, and spawning | planned |
| 1.4 | Implement multi-step workflows with enforcement and handoff patterns | planned |
| 1.5 | Apply Agent SDK hooks for tool call interception and data normalization | planned |
| 1.6 | Design task decomposition strategies for complex workflows | planned |
| 1.7 | Manage session state, resumption, and forking | planned |

## Domain 4 — Prompt Engineering & Structured Output (20%)

| | Task statement | Lesson |
|---|---|---|
| 4.1 | Design prompts with explicit criteria to improve precision and reduce false positives | planned |
| 4.2 | Apply few-shot prompting to improve output consistency and quality | planned |
| 4.3 | Enforce structured output using tool use and JSON schemas | planned |
| 4.4 | Implement validation, retry, and feedback loops for extraction quality | planned |
| 4.5 | Design efficient batch processing strategies | planned |
| 4.6 | Design multi-instance and multi-pass review architectures | planned |

## Domain 5 — Context Management & Reliability (15%)

| | Task statement | Lesson |
|---|---|---|
| 5.1 | Manage conversation context to preserve critical information across long interactions | planned |
| 5.2 | Design effective escalation and ambiguity resolution patterns | planned |
| 5.3 | Implement error propagation strategies across multi-agent systems | planned |
| 5.4 | Manage context effectively in large codebase exploration | planned |
| 5.5 | Design human review workflows and confidence calibration | planned |

## The lab runs through all of it

One system, built across the course: **Course Doctor**, an agent that checks training
material against live documentation and reports what went stale, what it could not
check, and what needs a human. It needs all five domains honestly — MCP tools to fetch
and compare, a coordinator with subagents, a JSON schema to make findings
machine-checkable, and context discipline to keep provenance attached to every claim.

See the [repository README](../README.md) for the exam details, how the course is
sourced, and how to run the lab.

## Why task statements and not chapters

The exam guide names what it measures, task statement by task statement, and exam items
are written against those objectives. A chapter structure invented on top of that is a
second thing to keep in sync — and the first time it drifts, a lesson teaches something
the exam does not test. Every claim in every lesson traces to an exam-guide section or a
documentation URL in [SOURCES.md](../SOURCES.md).
