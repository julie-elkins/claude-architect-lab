# Lesson 4.1 — Criteria, not adverbs

**Domain 4: Prompt Engineering & Structured Output — 20% of CCAR-F**
**Task Statement 4.1:** Design prompts with explicit criteria to improve precision and
reduce false positives.

Lab artifact: Course Doctor's severity criteria, written as categories with examples
rather than as a request to be careful.

## What you will be able to do afterwards

Replace an instruction that asks for better judgement with criteria that define it — and
explain why one noisy finding category damages trust in the accurate ones.

## Why the exam cares

The guide names the failing instruction by quoting it: **"be conservative"** and **"only
report high-confidence findings"** *fail to improve precision compared to specific
categorical criteria.*

That is a strong claim stated plainly, and it is the whole task statement. Confidence-based
filtering feels like a tightening and changes nothing measurable, because "high
confidence" is not a property the model can calibrate on request — it is a word.

The guide then gives the contrast, also quoted: **"flag comments only when claimed
behavior contradicts actual code behavior"** against **"check that comments are
accurate."** The first is a test. The second is a hope.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Precision and recall.** Precision is how many flagged things are real; recall is how
many real things got flagged. *Why it matters here:* this task statement is entirely about
precision, and the two trade off. *Depth:* any introduction to classification metrics.

**False positive.** A finding that is not a problem. *Why it matters here:* it is the unit
of damage. *Depth:* below — the damage is not where people expect.

**Operational definition.** A criterion stated so two people would classify the same case
the same way. *Why it matters here:* it is what "explicit criteria" means. *Depth:*
measurement theory; the same discipline as writing a rubric.

**Category versus confidence.** Filtering by *what kind of thing it is* against filtering
by *how sure you are.* *Why it matters here:* the guide says the first works and the second
does not. *Depth:* the build.

**Trust as a shared resource.** One component's noise spending another's credibility. *Why
it matters here:* the guide's most interesting claim. *Depth:* the build.

## The idea, before any prompt

**Write a test, not an adjective.**

Every vague instruction can be converted by asking: *what would I have to observe to call
this a finding?* "Comments should be accurate" becomes "the comment states behaviour that
contradicts what the code does." Now two reviewers agree, and so does the model.

**Filter by category, not by confidence.** Decide which *kinds* of issue to report — bugs,
security — and which to skip — minor style, patterns local to this codebase. That is a
list you can write down. "Only high-confidence findings" is not.

**And understand what a noisy category costs**, because it is not what you would guess.
The guide's claim: **high false positive categories undermine confidence in the accurate
ones.** Trust is not per-category. A reviewer who dismisses four bad style findings starts
skimming the security findings too, and the security findings were right.

Which is why the guide's remedy is so blunt: **temporarily disable the noisy category**
while you improve its prompt. Not soften it — turn it off. A category that is wrong half
the time is spending the credibility of the ones that are right.

## The build

### Step 1 — convert the adverb

```
BEFORE  "Be conservative about flagging a claim as contradicted."

AFTER   "Flag CONTRADICTED only when the cited page states something that cannot
         both be true with the lesson's claim. A page that is silent on the claim
         is NOT_IN_DOCS. A page that supports it in different words is SUPPORTED."
```

The second is three tests and a default. Nothing in it asks for care.

### Step 2 — define severity by example, not by adjective

The guide's skill is explicit severity criteria **with concrete examples for each level.**
So:

```
HIGH      a numeric claim the current page contradicts
          example: lesson says 10 GB, page says 20 GB
MEDIUM    a navigation or naming change; the concept still holds
          example: a console path that has been renamed
LOW       a wording difference with no behavioural consequence
UNKNOWN   the page could not be fetched
          NOT a severity — an absence of evidence
```

An example per level is what makes two runs classify the same case the same way. "Use your
judgement about severity" guarantees they will not.

### Step 3 — say what to skip, in the same breath

```
REPORT  factual contradictions, dead citations, missing read dates
SKIP    British versus American spelling, sentence length, heading style,
        anything that is a house convention rather than an error
```

Writing the skip list is what stops the model finding things to say. Without it, a review
asked for findings produces findings.

### Step 4 — turn off what you cannot trust yet

If one category is producing noise, disable it and keep the rest. The alternative — leaving
it on while you iterate — spends the trust the other categories earned, and you will not
notice until someone stops reading the output.

## Tips

Things that cost somebody an hour.

**If your fix to a precision problem is an adverb, it is not a fix.** "Be more careful",
"be conservative", "only flag clear cases" — all named by the guide as ineffective. The
tell is that you cannot say what changed about the test.

**One noisy category poisons the accurate ones.** This is the counterintuitive part and it
is the guide's own claim. Precision is not evaluated per category by the person reading;
it is evaluated on the report.

**A skip list is as important as a report list, and half as likely to get written.** A
model asked only what to report will report things.

**Severity without examples is severity by vibe.** Two runs will disagree, and so will two
readers, and nobody will be able to say who is right.

**"UNKNOWN" is not a severity level.** It is the absence of evidence, and filing it as
low-severity turns an unchecked thing into a checked-and-minor thing. Keep it in its own
category.

## The anti-pattern

Quoted, because the guide names them:

> **"Be conservative"** and **"only report high-confidence findings"** — general
> instructions that *fail to improve precision compared to specific categorical criteria.*

> **Confidence-based filtering** in place of a defined report-versus-skip list.

> **Leaving a high-false-positive category enabled** while you improve it, rather than
> temporarily disabling it.

Exam shape: when one option rewrites the instruction more firmly and another defines a
categorical criterion, the criterion wins. This domain's whole thesis is that wording
strength is not a mechanism.

## What this lesson does not cover

- **Few-shot examples** — TS 4.2, and often the better fix when the *format* rather than
  the *criterion* is inconsistent.
- **Schemas** — TS 4.3. A schema constrains shape; criteria constrain judgement.
- **Retry and validation** — TS 4.4.
- **Confidence self-reporting**, which TS 4.6 treats as a routing signal rather than a
  filter — a different use from the one criticised here.
- **Measuring precision.** This lesson is about defining criteria, not about validating
  them; Domain 5 TS 5.5 covers sampling and calibration.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 4.1.

| Claim | Source |
|---|---|
| The importance of explicit criteria over vague instructions, e.g. "flag comments only when claimed behavior contradicts actual code behavior" versus "check that comments are accurate" | EG §6, TS 4.1 |
| General instructions like "be conservative" or "only report high-confidence findings" fail to improve precision compared to specific categorical criteria | EG §6, TS 4.1 |
| High false positive categories undermine confidence in accurate categories | EG §6, TS 4.1 |
| Writing specific review criteria defining which issues to report (bugs, security) versus skip (minor style, local patterns) rather than relying on confidence-based filtering | EG §6, TS 4.1 |
| Temporarily disabling high false-positive categories to restore developer trust while improving prompts for those categories | EG §6, TS 4.1 |
| Defining explicit severity criteria with concrete code examples for each severity level to achieve consistent classification | EG §6, TS 4.1 |
