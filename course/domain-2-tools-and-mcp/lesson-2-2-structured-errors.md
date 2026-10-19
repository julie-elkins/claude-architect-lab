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

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

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
