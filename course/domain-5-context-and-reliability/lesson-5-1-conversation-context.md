# Lesson 5.1 — What a summary quietly throws away

**Domain 5: Context Management & Reliability — 15% of CCAR-F**
**Task Statement 5.1:** Manage conversation context to preserve critical information
across long interactions.

Lab artifact: Course Doctor's case-facts block, carried outside the summarised history.

## What you will be able to do afterwards

Keep the facts that must survive a long session out of the summary — and place a long input
so the middle of it is not where your important findings live.

## Why the exam cares

The guide names two failure modes that are invisible while they happen.

**Progressive summarisation risk:** condensing **numerical values, percentages, dates and
customer-stated expectations** into vague summaries. A summary that says "the customer
discussed a refund" has lost the amount, the date and the order number — and reads
perfectly well.

**The "lost in the middle" effect:** models *"reliably process information at the beginning
and end of long inputs but may omit findings from middle sections."* So a long aggregated
input is not uniformly attended, and where you put something changes whether it is used.

Both are examinable because both have cheap, specific remedies.

## Fundamentals

**Progressive summarisation.** Replacing older history with a shorter version, repeatedly.
*Why it matters here:* each pass loses detail, and the losses compound. *Depth:* lesson 1.1
on compaction.

**Position effects.** Where something sits in a long input affects how reliably it is used.
*Why it matters here:* the lost-in-the-middle finding. *Depth:* the retrieval literature on
positional bias.

**Transactional fact.** A precise value — an amount, a date, an identifier. *Why it matters
here:* exactly the class a summary destroys. *Depth:* the build.

**Context layer.** A block of information carried separately from the conversation rather
than inside it. *Why it matters here:* it is the remedy. *Depth:* the build.

**Signal-to-token ratio.** How much of what a tool returns is relevant. *Why it matters
here:* the guide's own figure — 40+ fields per lookup when 5 matter. *Depth:* lesson 2.2.

## The idea, before any design

**Decide what must survive, and keep it outside the thing that shrinks.**

A summary is lossy by construction, so the answer is not a better summary. It is a
**persistent facts block** — amounts, dates, order numbers, statuses — included in every
prompt *outside* the summarised history. The summary can compress the narrative; the facts
are not part of the narrative.

**Then trim at the source.** A tool returning forty fields when five are relevant spends
the other thirty-five in every subsequent turn, because context accumulates. Trim before
it lands, not after it is a problem.

**And place long inputs deliberately.** Key findings at the beginning, explicit section
headers through the detail. You are not making it prettier — you are keeping important
material out of the position where it is least reliably read.

## The build

### Step 1 — the facts block

```
CASE FACTS (carried in every prompt; not part of summarised history)
  corpus        121 chunks at ~/course-corpus-content
  depths set    62 of 121, MLA only
  verified      0 of 121
  threshold     365 days
  lessons       24 of 29 written
```

Five lines, every one a value a summary would turn into "most of the corpus has been
processed."

### Step 2 — trim the tool output before it accumulates

```
RETURNED       path, text, hash, size, mtime, encoding, mode, inode, 34 more fields
KEPT           path, text, hash
```

Three fields instead of forty. The other thirty-seven were paid for once on arrival and
again on every turn after.

### Step 3 — place the long input

```
1  KEY FINDINGS         (first — the part that must be read)
2  ## Lesson 3.1        explicit header
3  ## Lesson 3.3        explicit header
   ...
N  WHAT WAS NOT COVERED (last — the other reliable position)
```

Findings first, headers throughout, coverage last. Both ends used on purpose, and nothing
important buried at 60%.

### Step 4 — make upstream agents return structure, not prose

Two guide skills that pair: require subagents to include **metadata — dates, source
locations, methodological context — in structured outputs**, and modify upstream agents to
return **structured data rather than verbose content** when the downstream agent has a
limited budget.

A worker that returns three paragraphs forces the synthesiser to spend budget re-reading
them. One that returns `{claim, url, verdict, date}` does not.

## Tips

Things that cost somebody an hour.

**A summary that reads well has still lost your numbers.** Fluency is not the signal. Check
whether a specific amount, date or identifier survived — those go first and they go
silently.

**Trim tool output at the boundary, not when context gets tight.** By the time it is tight
the fields are already in every prior turn, and you cannot retroactively un-spend them.

**Put what must be read first or last.** The middle of a long input is the least reliable
place for anything load-bearing, and it is where chronological ordering naturally puts your
most recent findings.

**"Not covered" belongs at the end, where it will be read.** Buried in the middle it is
decorative.

**A facts block is cheap and almost nobody writes one.** Five lines in every prompt, and it
is the difference between a session that still knows the threshold on turn forty and one
that has been told "a threshold was discussed."

## The anti-pattern

From the guide's objectives:

> **Progressive summarisation that condenses numerical values, percentages, dates and
> stated expectations into vague summaries.**

> **Tool results accumulating in context disproportionately to their relevance** — the
> guide's own example being 40+ fields per lookup when only 5 are relevant.

And the positional one:

> **Treating a long input as uniformly attended.** Models process the beginning and end
> reliably and *"may omit findings from middle sections."*

## What this lesson does not cover

- **Compaction mechanics and `/compact`** — lesson 5.4.
- **Escalation when context runs out** — lesson 5.2 is about escalation triggers, which are
  a different subject.
- **Error context across agents** — lesson 5.3.
- **Session resumption** — lesson 1.7. This lesson is about one long session; that one is
  about crossing between sessions.
- **Prompt caching**, which makes a stable facts block cheaper and is out of scope here.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 5.1.

| Claim | Source |
|---|---|
| Progressive summarisation risks condensing numerical values, percentages, dates and customer-stated expectations into vague summaries | EG §6, TS 5.1 |
| The "lost in the middle" effect: models reliably process information at the beginning and end of long inputs but may omit findings from middle sections | EG §6, TS 5.1 |
| Tool results accumulate in context and consume tokens disproportionately to their relevance, e.g. 40+ fields per order lookup when only 5 are relevant | EG §6, TS 5.1 |
| The importance of passing complete conversation history in subsequent API requests to maintain coherence | EG §6, TS 5.1 |
| Extracting transactional facts — amounts, dates, order numbers, statuses — into a persistent "case facts" block included in each prompt, outside summarised history | EG §6, TS 5.1 |
| Trimming verbose tool outputs to only relevant fields before they accumulate | EG §6, TS 5.1 |
| Placing key findings summaries at the beginning of aggregated inputs and organising detailed results with explicit section headers to mitigate position effects | EG §6, TS 5.1 |
| Requiring subagents to include metadata — dates, source locations, methodological context — in structured outputs to support accurate downstream synthesis | EG §6, TS 5.1 |
| Modifying upstream agents to return structured data rather than verbose content when downstream agents have limited context budgets | EG §6, TS 5.1 |
| Context does not reset between turns; everything accumulates, and compaction replaces older messages with a summary so early instructions may not be preserved | [agent loop docs](https://code.claude.com/docs/en/agent-sdk/agent-loop), read 2026-10-17 |
