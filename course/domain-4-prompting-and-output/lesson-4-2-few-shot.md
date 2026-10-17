# Lesson 4.2 — Show the ambiguous case

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
**Task Statement 4.2:** Apply few-shot prompting to improve output consistency and
quality.

Lab artifact: three worked examples that teach Course Doctor the hard call, not the easy
one.

## What you will be able to do afterwards

Choose few-shot examples that make the model *generalise* rather than pattern-match — which
means choosing the awkward cases on purpose.

## Why the exam cares

The guide's claim is unqualified: **few-shot examples are the most effective technique for
achieving consistently formatted, actionable output when detailed instructions alone
produce inconsistent results.**

Read that against lesson 4.1 and the pair becomes the domain's thesis. When the *criterion*
is vague, define it. When the criterion is fine and the *output* is still inconsistent,
examples beat more instruction. Neither is fixed by stronger wording.

And the guide is specific about which examples: ones that **demonstrate ambiguous-case
handling**, and that **enable generalisation to novel patterns rather than matching only
pre-specified cases.** That is the difference between two and three examples, and it is
the examinable part.

## Fundamentals

**Few-shot prompting.** Including worked input/output pairs in the prompt. *Why it matters
here:* it is the technique. *Depth:* any prompting guide; the mechanics are trivial and
the selection is not.

**Generalisation versus matching.** Applying a principle to a new case against recognising
a seen case. *Why it matters here:* it is the guide's stated goal, and it decides which
examples to pick. *Depth:* the build.

**Ambiguous case.** An input where two plausible answers exist. *Why it matters here:* the
guide names these as what examples are *for*. *Depth:* the build.

**Hallucination in extraction.** Inventing a value not present in the source. *Why it
matters here:* the guide names few-shot as effective against it specifically. *Depth:*
lesson 4.3's optional-field discussion.

**Format consistency.** The same shape every time. *Why it matters here:* the easiest win,
and the least interesting. *Depth:* a schema is stronger — lesson 4.3.

## The idea, before any examples

**Two examples teach the format. The third teaches the judgement.**

That is the whole lesson. Two input/output pairs showing a clean case establish the shape,
and a model can match that shape without understanding anything. The example that does the
real work is the one where **two answers were plausible and you show which was chosen and
why.**

The guide's phrasing for this skill is worth keeping: examples that **"show reasoning for
why one action was chosen over plausible alternatives."** Not the answer — the reasoning
to the answer, in the example itself.

**And examples are the right fix for extraction hallucination**, because they can
demonstrate the behaviour an instruction describes badly: here is a document that does not
state the figure, and here is the output with the field left as `unclear`. One pair teaches
that more reliably than a paragraph asking the model not to guess.

## The build

### Step 1 — two for the format

```
Input:  lesson claims "files above the working directory load at launch";
        cited page states the same in the same words
Output: {"verdict": "supported", "quoted_support": "<exact line>"}

Input:  lesson claims a 10 GB limit; cited page states 20 GB
Output: {"verdict": "contradicted", "quoted_support": "<exact line>"}
```

Clean, unambiguous, and between them they fix the shape: a verdict plus the quote that
justifies it.

### Step 2 — the third one, which is the point

```
Input:  lesson claims "a project file does not suppress a parent one";
        cited page describes loading order and never addresses suppression
Output: {"verdict": "not_in_docs",
         "reasoning": "The page is SILENT on this claim. Silence is not
                       contradiction and it is not support. NOT_IN_DOCS is
                       chosen over SUPPORTED because nothing states the claim,
                       and over CONTRADICTED because nothing denies it."}
```

That is the case where a model would otherwise reach for `supported`, because the page is
*about* the right subject. The example shows the alternatives considered and rejected —
which is what lets the model handle the *next* silent page, not just this one.

### Step 3 — add one against the specific error you are seeing

The guide names two patterns worth an example each:

**Distinguishing an acceptable pattern from a genuine issue**, to cut false positives
without losing generalisation. For Course Doctor: a lesson quoting a doc line in slightly
different words is `supported`, not `contradicted`.

**Varied source structures.** Its own examples are inline citations against bibliographies,
and methodology sections against embedded detail. One pair per structure, and the model
stops producing empty extractions when the shape changes.

### Step 4 — show the format you actually want

The guide's skill names the fields: **location, issue, severity, suggested fix.** An
example containing all four, in order, does more for consistency than a sentence describing
them — and if you also have a schema (TS 4.3), the example teaches the *content* while the
schema enforces the *shape*.

## Tips

Things that cost somebody an hour.

**Two examples teach matching; the third teaches generalising.** If all your examples are
clean cases, you have taught the format and nothing else — and the model will handle the
awkward case by picking whichever of your examples it most resembles.

**Put the reasoning inside the example.** An example that shows only the answer teaches the
answer. One that shows why the alternative was rejected teaches the rule.

**Pick your examples from the errors you are actually getting.** Generic examples fix
generic problems. If extractions come back empty on bibliography-style sources, the next
example is a bibliography.

**Few-shot fixes inconsistency; a schema fixes invalidity.** They are not alternatives, and
reaching for examples when the problem is malformed JSON is solving the wrong layer.

**An example demonstrating an "I don't know" output is the highest-value pair you can
write.** It is also the one nobody writes, because every example people choose is a success
case.

## The anti-pattern

From the guide's objectives:

> **Detailed instructions where examples are needed.** The guide's claim is that few-shot
> is *the most effective technique* when instructions alone produce inconsistent output —
> so adding more instruction to an inconsistency problem is the named mistake.

> **Examples that cover only pre-specified cases**, producing matching rather than
> generalisation.

Exam shape: if one option adds instruction and another adds two to four examples for the
ambiguous case, the examples win — and the guide's own number is **2–4 targeted examples**,
not twenty.

## What this lesson does not cover

- **Defining the criterion** — TS 4.1. Examples teach a criterion; they do not substitute
  for having one.
- **Schemas** — TS 4.3.
- **Retry with error feedback** — TS 4.4, which is a different use of examples: the failure
  becomes the example.
- **Prompt caching**, which makes a long example block cheaper on repeat and is out of
  scope here.
- **How many examples is too many.** The guide says 2–4 for ambiguous scenarios; it does
  not state an upper bound, and this lesson does not invent one.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 4.2.

| Claim | Source |
|---|---|
| Few-shot examples are the most effective technique for consistently formatted, actionable output when detailed instructions alone produce inconsistent results | EG §6, TS 4.2 |
| The role of few-shot examples in demonstrating ambiguous-case handling, e.g. tool selection for ambiguous requests, branch-level test coverage gaps | EG §6, TS 4.2 |
| Few-shot examples enable generalisation to novel patterns rather than matching only pre-specified cases | EG §6, TS 4.2 |
| Few-shot examples reduce hallucination in extraction tasks, e.g. informal measurements, varied document structures | EG §6, TS 4.2 |
| Creating 2–4 targeted examples for ambiguous scenarios that show reasoning for why one action was chosen over plausible alternatives | EG §6, TS 4.2 |
| Including examples demonstrating the desired output format: location, issue, severity, suggested fix | EG §6, TS 4.2 |
| Examples distinguishing acceptable code patterns from genuine issues, reducing false positives while enabling generalisation | EG §6, TS 4.2 |
| Examples demonstrating varied document structures — inline citations versus bibliographies, methodology sections versus embedded details | EG §6, TS 4.2 |
| Examples showing correct extraction from varied formats to address empty or null extraction of required fields | EG §6, TS 4.2 |
