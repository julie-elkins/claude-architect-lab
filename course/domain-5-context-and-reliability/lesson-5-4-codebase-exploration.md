# Lesson 5.4 — When the session starts talking about typical patterns

**Domain 5: Context Management & Reliability — 15% of CCAR-F**
**Task Statement 5.4:** Manage context effectively in large codebase exploration.

Lab artifact: Course Doctor's exploration findings written to a scratchpad, so phase two
does not depend on phase one still being in context.

## What you will be able to do afterwards

Recognise context degradation by its symptom, persist findings across a context boundary,
and design an exploration that survives a crash.

## Why the exam cares

The guide describes the symptom precisely, and it is the most useful sentence in the task
statement: in extended sessions **models start giving inconsistent answers and referencing
"typical patterns" rather than the specific classes discovered earlier.**

That is a diagnostic. When an agent stops naming the class it read an hour ago and starts
describing what such a class usually looks like, the specific knowledge is gone. Nothing
announces it — the answers stay fluent and become generic.

The remedies it names are all forms of *getting findings out of the conversation*:
scratchpad files, subagent delegation, summarising between phases, and structured state
exports for crash recovery.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Context degradation.** Reliability falling as a session lengthens. *Why it matters here:*
the subject, and it has a recognisable symptom. *Depth:* lesson 5.1's position effects are
one mechanism.

**Scratchpad.** A file the agent writes findings to and reads back. *Why it matters here:*
it is the named remedy, and it works because a file is not a context window. *Depth:* the
build.

**Delegation for isolation.** Handing verbose work to a worker so only its conclusion
returns. *Why it matters here:* exploration is almost entirely verbose reading. *Depth:*
lesson 1.3.

**Phase boundary.** A deliberate point where you summarise before continuing. *Why it
matters here:* the guide's skill of summarising one phase before spawning the next.
*Depth:* the build.

**Manifest.** A record of where each component's state was written. *Why it matters here:*
the named crash-recovery mechanism. *Depth:* the build.

## The idea, before any exploration

**Get the findings out of the conversation.**

Every remedy here is a variant of that. A scratchpad puts them in a file. A subagent keeps
the reading out of your window entirely and returns a summary. A phase summary converts a
long exploration into a short statement before the next phase starts. A manifest puts state
somewhere a new process can find it.

**Delegate the reading, keep the coordination.** The guide's framing: subagents investigate
specific questions — *"find all test files", "trace refund flow dependencies"* — while the
main agent preserves high-level understanding. Specific questions, because a worker given a
vague brief returns a vague summary and you have spent the tokens anyway.

**Summarise at the boundary, not at the end.** Summarise phase one's findings and **inject
them into phase two's initial context.** At the end, the summary has nothing to inform.

**And design for the crash**, because a long exploration is exactly the thing that dies
halfway. Each agent exports its state to a known location; the coordinator loads a manifest
on resume.

## The build

### Step 1 — recognise the symptom

```
EARLY   "materials.py defines read_material_file, which returns MaterialReadingResult
         and refuses with a Refusal carrying error, message and guidance"

LATER   "the library module typically exposes a read function that returns a result
         object, with errors handled in the usual way"
```

The second answer is not wrong. It is *generic*, and the specific knowledge it replaced is
gone. That shift is the signal to persist and reset, not to ask again more firmly.

### Step 2 — the scratchpad

```
FINDINGS.md   (written as discovered, read back when needed)
  materials.py   read_material_file -> MaterialReadingResult | Refusal
                 bounds: 1 MiB, path confined to COURSE_DOCTOR_ROOT
  contracts.py   Diagnostics.what_it_does_not_show, populated on success
  server.py      one tool; thin adapter; converts MaterialRefused to a payload
```

Written once as discovered, re-read on demand. Nothing here depends on the session still
remembering it.

### Step 3 — delegate the verbose phase

```
coordinator  "which lessons cite a URL that no other lesson cites?"
             -> subagent reads 23 lesson files
             -> returns a 6-line answer
```

Twenty-three files read, six lines in the coordinator's context. Lesson 1.3's rule applies:
the worker needs the question in full because it cannot see the conversation.

### Step 4 — summarise between phases, and keep a manifest

```
PHASE 1  map the corpus          -> summary injected into phase 2's opening prompt
PHASE 2  check the citations     -> state exported to state/phase2.json
MANIFEST state/manifest.json     -> names each phase's output file

on resume: load the manifest, read the completed phases, start at the first gap
```

`/compact` is the in-session relief valve for a window filling with discovery output — the
guide names it — but a compaction is lossy, and a scratchpad written before compacting is
not.

## Tips

Things that cost somebody an hour.

**"Typically" is the tell.** When an agent that was naming specific classes starts
describing what such classes usually do, stop asking and start persisting. Pushing harder
produces more confident generic answers.

**Write the scratchpad as you discover, not at the end.** At the end you are summarising
from a degraded context, which is the thing you were trying to work around.

**Give a worker a specific question.** "Explore the codebase" returns a summary of
everything and nothing. "Find every call site of `read_material_file`" returns a list.

**Summarise before spawning the next phase, not after finishing.** The summary's job is to
inform phase two; produced at the end it informs nobody.

**A manifest is cheap and you will only value it once.** The run that dies at hour two is
the one where you find out whether phase one's output was written somewhere findable.

## The anti-pattern

From the guide's objectives:

> **Letting an extended session degrade** until it references typical patterns rather than
> the specific classes it discovered, instead of persisting findings across context
> boundaries.

> **Exploring in the main agent's context** when a subagent could isolate the verbose
> output and return a summary.

And the one implied by the manifest skill:

> **A long exploration with no state exported anywhere.** It works until it does not, and
> then the whole thing restarts.

## What this lesson does not cover

- **Position effects and summarisation risk** — lesson 5.1.
- **Spawning and configuring workers** — lesson 1.3.
- **Session resumption** — lesson 1.7. This is crash recovery within a planned
  exploration; that is returning to a saved conversation.
- **The built-in search tools and incremental reading** — lesson 2.5, which is the
  tool-level version of the same discipline.
- **Checkpointing**, which rewinds rather than persisting forward.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 5.4.

| Claim | Source |
|---|---|
| Context degradation in extended sessions: models start giving inconsistent answers and referencing "typical patterns" rather than specific classes discovered earlier | EG §6, TS 5.4 |
| The role of scratchpad files for persisting key findings across context boundaries | EG §6, TS 5.4 |
| Subagent delegation for isolating verbose exploration output while the main agent coordinates high-level understanding | EG §6, TS 5.4 |
| Structured state persistence for crash recovery: each agent exports state to a known location and the coordinator loads a manifest on resume | EG §6, TS 5.4 |
| Spawning subagents to investigate specific questions, e.g. "find all test files", "trace refund flow dependencies" | EG §6, TS 5.4 |
| Having agents maintain scratchpad files recording key findings and referencing them for subsequent questions to counteract degradation | EG §6, TS 5.4 |
| Summarising key findings from one exploration phase before spawning subagents for the next, injecting summaries into initial context | EG §6, TS 5.4 |
| Designing crash recovery using structured agent state exports (manifests) that the coordinator loads on resume | EG §6, TS 5.4 |
| Using `/compact` to reduce context usage during extended exploration when context fills with verbose discovery output | EG §6, TS 5.4 |
| A non-fork subagent starts fresh with no conversation history and only its final result returns to the parent | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
