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

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

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
