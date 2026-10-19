# Lesson 4.4 — Retrying what a retry can fix

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
**Task Statement 4.4:** Implement validation, retry, and feedback loops for extraction
quality.

Lab artifact: Course Doctor retrying a malformed finding with the validation error
attached, and refusing to retry a claim whose source was never provided.

## What you will be able to do afterwards

Build a retry that improves the second attempt, and recognise the class of failure where
retrying is guaranteed to waste money.

## Why the exam cares

The guide states the one thing people get wrong: **retries are ineffective when the
required information is simply absent from the source document.** Format errors and
structural errors respond to a retry. A missing fact does not.

So the examinable judgment is not *how* to retry — it is *whether*. Three attempts at
extracting a figure that is not in the document produce three failures and a bill.

And it names the mechanism that makes a retry worth anything: **retry with error
feedback** — appending the specific validation errors to the prompt so the second attempt
is informed rather than merely repeated.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Validation.** Checking output against a rule after it is produced. *Why it matters here:*
it is what generates the feedback the retry carries. *Depth:* lesson 4.3 for the schema
layer.

**Semantic versus syntactic error.** Wrong content against malformed shape. *Why it matters
here:* schemas eliminate the second, which is why this task statement is about the first.
*Depth:* lesson 4.3.

**Idempotent retry.** Repeating safely. *Why it matters here:* an extraction retry is safe;
a retry that writes something twice is not. *Depth:* REST semantics.

**Self-correction.** Giving a model its own failed output plus the reason, and asking
again. *Why it matters here:* it is the documented pattern. *Depth:* the build.

**Feedback loop.** Instrumenting output so you can analyse it in aggregate later. *Why it
matters here:* the guide's `detected_pattern` field, and it is the long-game half of this
task statement. *Depth:* the build.

## The idea, before any code

**Classify the failure before you retry it.**

Three kinds, and only two are worth a second attempt:

- **Format or structural** — the output did not parse, fields were in the wrong place, the
  shape was wrong. **Retry works**, especially with the error attached.
- **Semantic** — the values do not reconcile; a total does not sum. **Retry may work**,
  because the model can recheck its own arithmetic when told what failed.
- **Absent information** — the fact is not in the document you supplied. **Retry cannot
  work.** The guide's example is information that exists only in an external document not
  provided. No amount of asking again puts it there.

**Then make the retry carry the evidence.** The guide's skill: a follow-up request
including **the original document, the failed extraction, and the specific validation
errors.** All three. A retry that re-sends only the document is a fresh attempt, not a
correction — and it will usually make the same mistake.

**And design the validation so it can catch semantic errors at all**, which means asking
for the evidence rather than the conclusion. Extract `calculated_total` *beside*
`stated_total`. Add a `conflict_detected` boolean. You are not validating the model; you
are making it surface what would reveal its own error.

## The build

### Step 1 — validate for the errors a schema cannot catch

```
schema-level   does it parse? are the fields present and typed?   -> TS 4.3 handles this
semantic       does quoted_support actually appear on the page?
               is verdict SUPPORTED while quoted_support is empty?
               is conflict_detected false while two sources disagree?
```

The second block is this lesson. Each is a pair of fields that should agree and might not.

### Step 2 — retry with the error attached

```
RETRY PROMPT
  the original lesson text and the fetched page   (unchanged)
  your previous output                            (verbatim)
  validation errors:
    - verdict is SUPPORTED but quoted_support is empty
    - quoted_support must be a literal span from the fetched page
  Correct these specific errors. Change nothing else.
```

"Change nothing else" is doing work. Without it a retry often rewrites the parts that were
fine.

### Step 3 — refuse the retry that cannot succeed

```
if the failure is "the page does not contain this information":
    do NOT retry
    record NOT_IN_DOCS with the URL and the date
    stop
```

This is the guide's judgment call made explicit. The failure is real, the output is
correct, and the honest result is a verdict rather than another attempt.

### Step 4 — instrument for the long game

The guide's `detected_pattern` field: record **which construct triggered a finding**, so
that when a human dismisses findings you can analyse *what kind* they dismiss.

```
{"verdict": "contradicted", "detected_pattern": "numeric_quota_mismatch"}
{"verdict": "contradicted", "detected_pattern": "console_path_renamed"}
```

After forty reviews you can see that `console_path_renamed` is dismissed 80% of the time
and `numeric_quota_mismatch` almost never. That is the data that tells you which category
to disable under lesson 4.1 — and without the field, you have forty dismissals and no
pattern.

## Tips

Things that cost somebody an hour.

**Retrying an absent fact is the most expensive no-op available.** Three attempts, three
identical failures, and a slower answer. Classify first.

**A retry without the previous output is not a correction.** The model cannot fix what it
cannot see, and it will frequently reproduce the same error with different wording.

**Say "change nothing else" or the retry will rewrite the parts that worked.** Then your
second attempt has new errors in previously correct fields and you cannot tell whether you
are converging.

**`detected_pattern` costs one field and is worth more than any single finding.** It is
the only thing that turns dismissals into evidence. Add it before you need it, because it
cannot be backfilled onto reviews already done.

**Extract the evidence, not the conclusion.** `calculated_total` beside `stated_total` lets
a validator catch what no schema can. Asking only for the total means trusting it.

## The anti-pattern

From the guide's objectives:

> **Retrying when the required information is absent from the source.** The guide
> distinguishes this explicitly from format and structural errors, which do respond.

> **A retry without the specific validation errors appended**, which is a repeat rather
> than a correction.

And the one that follows from `detected_pattern`:

> **Collecting dismissals without recording what was dismissed.** You learn that findings
> are being ignored and not which kind, so there is nothing to act on.

## What this lesson does not cover

- **Schema enforcement** — TS 4.3, which removes the syntax class of error entirely and is
  why this lesson is about semantics.
- **Defining what counts as a finding** — TS 4.1.
- **Few-shot examples** — TS 4.2, though a persistent failure is a good candidate to become
  one.
- **Independent review** — TS 4.6. A retry asks the same instance again; that is a
  different mechanism with a different weakness.
- **Human review routing** — Domain 5 TS 5.5, which is where dismissal data ends up being
  useful.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 4.4.

| Claim | Source |
|---|---|
| Retry-with-error-feedback: appending specific validation errors to the prompt on retry to guide correction | EG §6, TS 4.4 |
| The limits of retry: ineffective when the required information is simply absent from the source document, as opposed to format or structural errors | EG §6, TS 4.4 |
| Feedback loop design: tracking which constructs trigger findings via a `detected_pattern` field to enable systematic analysis of dismissal patterns | EG §6, TS 4.4 |
| The difference between semantic validation errors and schema syntax errors, the latter eliminated by tool use | EG §6, TS 4.4 |
| Follow-up requests that include the original document, the failed extraction, and specific validation errors for self-correction | EG §6, TS 4.4 |
| Identifying when retries will be ineffective — information existing only in an external document not provided — versus when they will succeed | EG §6, TS 4.4 |
| Adding `detected_pattern` fields to enable analysis of false positive patterns when developers dismiss findings | EG §6, TS 4.4 |
| Self-correction validation flows: extracting `calculated_total` alongside `stated_total` to flag discrepancies, and `conflict_detected` booleans for inconsistent source data | EG §6, TS 4.4 |
