# Lesson 5.3 — Two ways to be wrong about a failure

**Domain 5: Context Management & Reliability — 15% of CCAR-F**
**Task Statement 5.3:** Implement error propagation strategies across multi-agent systems.

Lab artifact: a Course Doctor worker that recovers what it can, propagates what it cannot,
and a synthesis that says where it had no sources.

## What you will be able to do afterwards

Propagate a failure with enough context for a coordinator to decide — and avoid both of the
named anti-patterns, which are opposites.

## Why the exam cares

The guide names two anti-patterns in the same breath, and they pull in opposite directions:

> **"silently suppressing errors (returning empty results as success) or terminating
> entire workflows on single failures are both anti-patterns"**

Which tells you the answer is neither extreme, and that is the examinable judgment. Recover
locally, propagate what you cannot resolve, and never let a failure render as a clean
result.

It also repeats the distinction from lesson 2.2 because it matters more at system scale:
**access failures versus valid empty results.** A timeout and a query that legitimately
matched nothing are both "no data" to a coordinator that cannot tell them apart.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Error propagation.** Passing a failure upward with context. *Why it matters here:* the
subject. *Depth:* exception-chaining practice in any language.

**Local recovery.** Handling a transient failure where it happened. *Why it matters here:*
the guide's preferred first response. *Depth:* retry patterns; lesson 4.4 for the limits.

**Partial result.** What you did get before failing. *Why it matters here:* it is the
difference between a useful failure and "failed". *Depth:* the build.

**Coverage annotation.** Marking which parts of an answer are well-supported and which have
gaps. *Why it matters here:* the guide's named skill, and the thing that stops a thin
report reading as complete. *Depth:* the build.

**Fail loudly versus fail silently.** Whether a problem announces itself. *Why it matters
here:* "returning empty results as success" is the silent version, and it is named. *Depth:*
lesson 2.2.

## The idea, before any code

**Three layers, in order.**

**Recover locally** what is transient — a timeout, a rate limit, a flaky connection. The
coordinator does not need to know about a retry that worked.

**Propagate with context** what you cannot resolve. The guide lists what to include:
**failure type, what was attempted, partial results, and potential alternatives.** Four
things, and the coordinator cannot make an intelligent recovery decision from fewer.
"Search unavailable" is the guide's own example of a status that hides everything useful.

**Annotate the aggregate.** When the synthesis is written, mark which findings are
well-supported and which topic areas have gaps **because sources were unavailable.** Absent
that, a report missing a third of its subject reads exactly like a complete one.

**And keep the two "no data" cases distinct at every layer.** A failed access needs a retry
decision. A valid empty result is an answer. Lesson 2.2's rule — different types, not one
type with a flag — holds here, because a flag survives one hop and gets dropped at the
next.

## The build

### Step 1 — the worker's reply when it cannot finish

```json
{
  "status": "unresolved",
  "failure_type": "fetch_timeout",
  "attempted": "GET https://code.claude.com/docs/en/memory, twice, 20s timeout",
  "partial_results": [
    {"claim": "files above load at launch", "verdict": "supported"}
  ],
  "alternatives_not_tried": ["the cached copy in the workspace", "the llms.txt index"],
  "not_covered": ["four remaining claims in this lesson"]
}
```

Five fields past the status, and each answers a question the coordinator would otherwise
have to guess: what broke, what was tried, what survived, what else exists, what is
missing.

### Step 2 — distinguish the two empties

```
lesson cites nothing                 -> {"urls": [], "urls_found": 0}   a FINDING
the lesson file could not be read    -> a Refusal object                a FAILURE
```

Two types. A coordinator receiving the first reports "this lesson cites no sources." A
coordinator receiving the second knows nothing was checked.

### Step 3 — recover locally, and say that you did

```
attempt 1   timeout
attempt 2   200
report      {"status": "ok", "retries": 1}
```

The retry worked, so it is not an error — but recording it is how you find out later that
one source times out constantly.

### Step 4 — annotate the synthesis

```
FINDINGS           11 claims checked across 3 lessons
WELL SUPPORTED     8 claims, each with a quoted span and a read date
GAPS               3 claims in lesson 3.3 — the rules frontmatter page was
                   unreachable in both attempts, so NONE of them was checked
NOT ATTEMPTED      lessons 4.x and 5.x were outside this run's scope
```

Two of those four blocks exist to stop the first one being read as the whole picture.

## Tips

Things that cost somebody an hour.

**"Returning empty results as success" is the failure you will actually ship.** It is not
laziness — it is what happens when the error path returns the same shape as the success
path. Make them different types and it becomes impossible.

**Terminating the workflow on one failure is the overcorrection, and it is equally named.**
Fourteen lessons checked and one unreachable page should not discard the fourteen.

**A failure reply without `attempted` forces the coordinator to re-derive it.** Which it
will do by retrying, which is the thing you were trying to inform.

**`alternatives_not_tried` is the field nobody includes and the coordinator most wants.**
It is the difference between "this is impossible" and "this route failed."

**A report with no "gaps" section is claiming complete coverage whether you meant to or
not.** Silence reads as healthy. Writing the section is the only way to say otherwise.

## The anti-pattern

Quoted, because the guide names both and they are opposites:

> **"silently suppressing errors (returning empty results as success) or terminating
> entire workflows on single failures are both anti-patterns"**

And the information-hiding one:

> **A generic error status that hides context from the coordinator** — "search unavailable"
> being the guide's own example.

Exam shape: when one option swallows the error and another aborts everything, both are
wrong; look for the one that recovers locally and propagates with context.

## What this lesson does not cover

- **One tool's error shape** — lesson 2.2, which is this at single-tool scale.
- **Retry policy and its limits** — lesson 4.4.
- **Escalating to a human** — lesson 5.2. An unresolved error is not automatically an
  escalation.
- **Coordinator architecture** — lesson 1.2, which is why all this flows through one place.
- **Observability of the system as a whole**, which is a real subject and not in this task
  statement's objectives.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 5.3.

| Claim | Source |
|---|---|
| Structured error context — failure type, attempted query, partial results, alternative approaches — enables intelligent coordinator recovery decisions | EG §6, TS 5.3 |
| The distinction between access failures (timeouts needing retry decisions) and valid empty results (successful queries with no matches) | EG §6, TS 5.3 |
| Generic error statuses such as "search unavailable" hide valuable context from the coordinator | EG §6, TS 5.3 |
| Silently suppressing errors by returning empty results as success, and terminating entire workflows on single failures, are both anti-patterns | EG §6, TS 5.3 |
| Returning structured error context including failure type, what was attempted, partial results and potential alternatives | EG §6, TS 5.3 |
| Subagents implementing local recovery for transient failures and propagating only errors they cannot resolve, including what was attempted and partial results | EG §6, TS 5.3 |
| Structuring synthesis output with coverage annotations indicating which findings are well-supported versus which topic areas have gaps due to unavailable sources | EG §6, TS 5.3 |
| The MCP `isError` flag and the four-way error taxonomy | EG §6, TS 2.2 |
