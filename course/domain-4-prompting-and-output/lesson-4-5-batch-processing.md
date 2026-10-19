# Lesson 4.5 — Half price, if you can wait a day

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
**Task Statement 4.5:** Design efficient batch processing strategies.

Lab artifact: Course Doctor's nightly sweep over every lesson submitted as one batch, and
the pre-merge check deliberately left synchronous.

## What you will be able to do afterwards

Decide whether a workload belongs on the batch API, size a submission window against an
SLA you have been given, and recover from a partial failure without resubmitting
everything.

## Why the exam cares

The guide gives three numbers and one prohibition, and they are the whole decision:
**50% cost saving, up to a 24-hour processing window, no guaranteed latency SLA.**

Which makes the judgment mechanical. **Blocking workflows cannot use it** — the guide's
example is a pre-merge check, and a pre-merge check that might take a day is not a check.
**Non-blocking, latency-tolerant work should**: overnight reports, weekly audits, nightly
test generation. Half price for work nobody is waiting on.

Then it names a second-order skill that is unusually concrete: **calculating submission
frequency from an SLA.** Its own worked figure is 4-hour windows to guarantee a 30-hour
SLA against 24-hour batch processing. That is arithmetic you can be asked to do.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Synchronous versus asynchronous.** Waiting for a reply against submitting and collecting
later. *Why it matters here:* it is the entire distinction. *Depth:* any treatment of
message queues.

**Latency tolerance.** How long a result can take before it stops being useful. *Why it
matters here:* it is the property that decides which API. *Depth:* none needed, but be
honest about it — most work is more tolerant than it feels.

**SLA arithmetic.** Working backwards from a promise to a schedule. *Why it matters here:*
the guide asks for it directly. *Depth:* the build.

**Correlation identifier.** A token that ties a response back to its request. *Why it
matters here:* `custom_id`, and without it a batch of results is anonymous. *Depth:*
distributed tracing uses the same idea.

**Partial failure.** Some units succeed, others do not. *Why it matters here:* a batch has
four per-request outcomes and only one is success. *Depth:* the build.

## The idea, before any submission

**Ask one question: is anyone waiting?**

If a human or a pipeline is blocked on the answer, synchronous. If the result is read
later — a morning report, a weekly audit — batch, and take the 50%.

**Then do the arithmetic rather than guessing a cadence.** If you have promised results
within 30 hours and processing may take up to 24, your submission window is the
difference: submit at least every 6 hours, and the guide's own example uses 4 to leave
margin. The margin is not timidity — processing *"may be slowed down based on current
demand"*, and under load *"you may see more requests expiring after 24 hours."*

**And design for partial failure from the start**, because resubmitting the whole batch
to recover three documents is the expensive mistake and the easy one.

## The build

### Step 1 — one request per unit, each with an id

```json
{"custom_id": "lesson-3-1-claim-04", "params": {...}}
{"custom_id": "lesson-3-3-claim-11", "params": {...}}
```

`custom_id` is how a result finds its way home: 1 to 64 characters, alphanumerics, hyphens
and underscores only. Make it *meaningful* — encode the lesson and the claim — because on
a partial failure the id is all you have to work out what to resubmit.

Two hard ceilings: **100,000 requests or 256 MB, whichever comes first.** Exceeding the
size gives a `413 request_too_large`.

### Step 2 — know what a batch cannot do

Three parameters are unsupported: **`stream`**, **`speed`** (fast mode tunes synchronous
latency, which does not apply), and **`max_tokens: 0`** (cache pre-warming, because the
ephemeral entry would expire before any follow-up). Every batched request needs
`max_tokens` of at least 1.

And the structural limit the guide names: **no multi-turn tool calling within a single
request.** There is no client in the loop during asynchronous processing, so you cannot
execute a tool mid-request and feed the result back. A batched request is one round trip.
Note that the documentation frames its exclusions as those three *parameters* rather than
as this limitation — both descriptions are true, at different levels, and the guide's is
the architectural one.

### Step 3 — read the four outcomes

Each request ends as one of:

| Outcome | Meaning | Billed? |
|---|---|---|
| `succeeded` | Request completed; includes the message result | Yes |
| `errored` | Invalid request or an internal error; no message created | **No** |
| `canceled` | You cancelled before it was sent to the model | **No** |
| `expired` | The batch hit its 24-hour expiry before this request was sent | **No** |

Three of four are free, which is worth knowing before you build cost estimates on
submitted volume rather than succeeded volume.

Results are available **when all messages have completed or after 24 hours, whichever
comes first.** So an expiry is not a failure to collect — it is a result you collect with
the rest.

### Step 4 — resubmit only the failures

The guide's named skill: resubmit **only the failed documents, identified by
`custom_id`**, with an appropriate modification — its example being chunking a document
that exceeded context limits. Partial recovery, not a rerun.

### Step 5 — refine on a sample first

The last skill, and the one that saves the most money: **prompt refinement on a sample set
before batch-processing large volumes**, to maximise first-pass success and avoid iterative
resubmission. Fifty requests to find out the prompt is wrong beats fifty thousand.

## Tips

Things that cost somebody an hour.

**Make `custom_id` self-describing, not sequential.** `request-0412` tells you nothing on a
partial failure. `lesson-3-1-claim-04` tells you exactly what to resubmit, and you will be
reading these ids at the worst possible time.

**You are not billed for `errored`, `canceled` or `expired` requests.** So a cost model
built on submitted volume overestimates, and — more usefully — a batch that largely expired
cost you almost nothing. Retry it.

**Expiry is more likely exactly when you are busiest.** Processing slows under demand, so
the run where you submitted the most is the run most likely to see expiries. Build the
schedule for the bad day.

**The 24 hours is a ceiling, not an estimate.** Most batches finish in under an hour. Plan
capacity against the ceiling and your expectations against the hour.

**Test the prompt on fifty before you send fifty thousand.** This is in the guide as a
skill, and it is the single highest-leverage habit here.

## The anti-pattern

From the guide's objectives:

> **Batch processing a blocking workflow.** Its example is a pre-merge check, and the
> failure is definitional: a gate that might answer tomorrow is not a gate.

> **Resubmitting an entire batch to recover the failures**, instead of resubmitting the
> failed `custom_id`s with a modification.

And the one implied by the arithmetic:

> **Choosing a submission cadence by feel instead of from the SLA.** The guide's worked
> example is 4-hour windows for a 30-hour promise against 24-hour processing. A cadence
> picked by instinct meets the SLA until the first slow day.

## What this lesson does not cover

- **Prompt caching inside a batch.** Real, and interacts with batching in ways out of
  scope here; `max_tokens: 0` pre-warming specifically does not work in a batch.
- **Rate limits**, which apply to both the HTTP requests and to pending requests inside a
  batch.
- **Pricing per model.** Model prices change; the 50% relationship is the durable fact.
- **Structured output in a batch** — TS 4.3, and it composes normally.
- **Multi-instance review**, which often *is* batchable — TS 4.6.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 4.5.

| Claim | Source |
|---|---|
| The Message Batches API: 50% cost savings, up to a 24-hour processing window, no guaranteed latency SLA | EG §6, TS 4.5 |
| Batch processing suits non-blocking, latency-tolerant workloads (overnight reports, weekly audits, nightly test generation) and is inappropriate for blocking workflows such as pre-merge checks | EG §6, TS 4.5 |
| The batch API does not support multi-turn tool calling within a single request | EG §6, TS 4.5 |
| `custom_id` fields correlate batch request and response pairs | EG §6, TS 4.5 |
| Calculating submission frequency from SLA constraints, e.g. 4-hour windows to guarantee a 30-hour SLA with 24-hour batch processing | EG §6, TS 4.5 |
| Handling batch failures by resubmitting only the failed documents identified by `custom_id`, with modifications such as chunking documents that exceeded context limits | EG §6, TS 4.5 |
| Using prompt refinement on a sample set before batch-processing large volumes | EG §6, TS 4.5 |
| "most batches finishing in less than 1 hour while reducing costs by 50%" | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
| "You can access batch results when all messages have completed or after 24 hours, whichever comes first. Batches expire if processing does not complete within 24 hours." | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
| A batch is limited to 100,000 requests or 256 MB, whichever is reached first; exceeding the size gives `413 request_too_large` | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
| `custom_id` must be 1 to 64 characters matching `^[a-zA-Z0-9_-]{1,64}$` | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
| Unsupported parameters are `stream`, `speed` and `max_tokens: 0`; each batched request needs `max_tokens` of at least 1 | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
| Four per-request outcomes — `succeeded`, `errored`, `canceled`, `expired` — and you are **not billed** for the last three | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
| "processing may be slowed down based on current demand and your request volume. In that case, you may see more requests expiring after 24 hours" | [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), read 2026-10-17 |
