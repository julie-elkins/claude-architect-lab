# Lesson 4.6 — The author is the worst reviewer

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
**Task Statement 4.6:** Design multi-instance and multi-pass review architectures.

Lab artifact: Course Doctor's findings reviewed by a second instance that never saw them
being written.

## What you will be able to do afterwards

Explain why asking a model to check its own work is structurally weaker than asking a
fresh one, and split a large review into passes that do not compete for attention.

## Why the exam cares

The guide gives a mechanism rather than an opinion: **a model retains reasoning context
from generation, making it less likely to question its own decisions in the same session.**

That is not "models are overconfident." It is specific: the reasoning that produced the
output is still present, so the review inherits the assumptions rather than testing them.

And it ranks the alternatives explicitly: **independent review instances, without prior
reasoning context, are more effective at catching subtle issues than self-review
instructions or extended thinking.** Both of those are the tempting options, and both are
named as weaker.

## Fundamentals

**Reviewer independence.** The reviewer did not produce the work. *Why it matters here:* it
is the whole mechanism, and it is the reason human code review exists. *Depth:* any
treatment of review practice; the argument transfers unchanged.

**Reasoning context.** The chain of thought that produced an output, still in the
conversation. *Why it matters here:* it is what makes self-review weak. *Depth:* lesson 1.3
on what a fresh subagent does and does not inherit.

**Attention dilution.** One pass holding too many concerns, so each gets less. *Why it
matters here:* the stated reason to split passes. *Depth:* lesson 1.6, which is the same
pattern as a decomposition strategy.

**Local versus cross-cutting.** Problems inside one item against problems between items.
*Why it matters here:* they need different inputs, so they need different passes. *Depth:*
lesson 1.6.

**Calibration.** Whether a stated confidence matches observed accuracy. *Why it matters
here:* self-reported confidence is useful for *routing* and not for *filtering*. *Depth:*
Domain 5 TS 5.5.

## The idea, before any architecture

**Independence is structural, not attitudinal.** You cannot instruct your way to it. A
"review your output carefully" instruction is given to the instance that holds the
reasoning, so it is asking the author to be their own reviewer more sincerely.

So: spawn a second instance **with no prior reasoning context** — the output, the source,
the criteria, and nothing about how the output came to be. It will question things the
author cannot.

**Then split by what each pass needs to see.** A per-item pass wants one item in full. A
cross-item pass wants every item's summary. Those are different inputs, which is why they
cannot be the same pass — and the guide names the cost of trying: attention dilution and
**contradictory findings.**

**And use confidence for routing, not filtering.** The guide's skill is verification passes
where the model **self-reports confidence alongside each finding to enable calibrated
review routing.** That is a very different use from lesson 4.1's criticism of
confidence-based *filtering*. As a filter it is a word; as a routing signal, compared
against observed accuracy, it has information in it.

## The build

### Step 1 — the generator, then a stranger

```
Instance A   writes findings for lesson 3.1
             -> hands over: the findings, the lesson, the cited pages, the criteria
             -> hands over NOTHING about its reasoning

Instance B   never saw A's conversation
             asks: does each quoted_support actually appear on that page?
                   is any verdict unsupported by its own evidence?
                   what did A not check?
```

B's last question is the one A structurally cannot ask well, because A knows what it
intended to cover.

Mechanically this is a fresh subagent rather than a fork — lesson 1.3 — since a fork
inherits the whole conversation and would reproduce exactly the context you are trying to
remove.

### Step 2 — per-item passes

```
PASS A, per lesson    input: one lesson, its citations, its fetched pages
                      finds: claims unsupported by their own cited source
```

Full attention on one item. Fifteen runs, independent, parallelisable.

### Step 3 — one integration pass, on the summaries

```
PASS B, cross lesson  input: all fifteen PASS A SUMMARIES
                      finds: two lessons contradicting each other
                             a task statement covered twice or not at all
                             a term used differently in two places
```

Summaries, not sources. Feeding pass B fifteen full lessons recreates the dilution the
split was meant to avoid — and the contradictions it is looking for are visible in the
summaries.

### Step 4 — confidence as a routing field

```
{"finding": "...", "confidence": "low", "why_uncertain": "page uses different wording"}
```

Low confidence routes to a human; high confidence routes to a sample check. That is
routing. What it must not become is `if confidence == "low": discard`, which is the
filtering lesson 4.1 rules out — and which quietly drops the findings most worth a look.

## Tips

Things that cost somebody an hour.

**"Review your own output carefully" is an instruction to the one party who cannot.** The
guide ranks it below an independent instance explicitly, and extended thinking too.

**Use a fresh subagent, not a fork, for the reviewer.** A fork inherits the entire
conversation — which is precisely the reasoning context you are removing. Same word,
opposite effect.

**The integration pass wants summaries.** This is the most common mistake in multi-pass
design: giving the cross-item pass everything, and reproducing the problem.

**Ask the reviewer what the author did not check.** It is the highest-yield question in the
whole architecture and the one an author answers worst.

**Confidence routes; it does not filter.** Discarding low-confidence findings throws away
the ones most likely to need judgement, and it looks like precision improving.

## The anti-pattern

From the guide's objectives:

> **Self-review in the generating session**, or reaching for a self-review instruction or
> extended thinking, instead of an independent instance without prior reasoning context.

> **A single large review pass** instead of per-item local passes plus a separate
> integration pass — the named costs being attention dilution and contradictory findings.

Exam shape: when one option adds an instruction to self-check and another adds a second
instance, the second instance wins. The guide's mechanism — retained reasoning context —
is why, and that mechanism is worth being able to state.

## What this lesson does not cover

- **Spawning and configuring the reviewer** — lesson 1.3.
- **Decomposition strategy** — lesson 1.6, which is this pattern at the workflow level.
- **Calibrating confidence against labelled data** — Domain 5 TS 5.5. Here confidence is a
  routing field; there it is a measured quantity.
- **Defining the review criteria** — TS 4.1. An independent reviewer with vague criteria is
  independently vague.
- **Cost.** Two instances cost roughly twice as much, and the guide does not treat the
  trade-off; neither does this lesson.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 4.6.

| Claim | Source |
|---|---|
| Self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session | EG §6, TS 4.6 |
| Independent review instances, without prior reasoning context, are more effective at catching subtle issues than self-review instructions or extended thinking | EG §6, TS 4.6 |
| Multi-pass review: splitting large reviews into per-file local analysis passes plus cross-file integration passes to avoid attention dilution and contradictory findings | EG §6, TS 4.6 |
| Using a second independent instance to review generated code without the generator's reasoning context | EG §6, TS 4.6 |
| Splitting large multi-file reviews into focused per-file passes for local issues plus separate integration passes for cross-file data flow analysis | EG §6, TS 4.6 |
| Running verification passes where the model self-reports confidence alongside each finding to enable calibrated review routing | EG §6, TS 4.6 |
| A session that generated code is less effective at reviewing its own changes than an independent review instance | EG §6, TS 3.6 |
| A fork inherits the entire conversation, where a non-fork subagent starts fresh with no conversation history | [sub-agents docs](https://code.claude.com/docs/en/sub-agents), read 2026-10-17 |
