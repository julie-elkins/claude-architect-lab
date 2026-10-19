# Lesson 5.2 — When to stop trying

**Domain 5: Context Management & Reliability — 15% of CCAR-F**
**Task Statement 5.2:** Design effective escalation and ambiguity resolution patterns.

Lab artifact: Course Doctor asking which lesson you meant instead of picking the closest
match.

## What you will be able to do afterwards

Name the three legitimate escalation triggers, and say why the two most intuitive ones are
both unreliable.

## Why the exam cares

The guide lists the real triggers and then rules out the popular ones.

**Legitimate:** a request for a human, a **policy exception or gap** — and it says
explicitly *not just complex cases* — and an inability to make meaningful progress.

**Unreliable:** *"sentiment-based escalation and self-reported confidence scores are
unreliable proxies for actual case complexity."* Both are the obvious implementations.
Sentiment measures how the person sounds, not how hard the case is; a confidence score
measures a word.

And the sharpest rule, because it inverts a natural instinct: **honour an explicit request
for a human immediately, without first attempting investigation.** The helpful move — let
me just try one thing — is the wrong answer.

## Fundamentals 📘

*Glossed for a newcomer, skippable if you already build with this stack. Each term
carries why it matters in this lesson and where to go for depth.*

**Escalation.** Handing a case to a human. *Why it matters here:* the subject. *Depth:*
lesson 1.4 for the handoff format, which is the other half.

**Proxy measure.** Something easy to observe standing in for something that matters. *Why
it matters here:* sentiment and self-reported confidence are both proxies for complexity,
and the guide says both are bad ones. *Depth:* measurement validity; a proxy is only as
good as its correlation.

**Policy gap.** The rules do not address this case. *Why it matters here:* a named trigger,
and distinct from the case being hard. *Depth:* the build.

**Ambiguity resolution.** Deciding what to do when the input matches several things. *Why
it matters here:* the guide's answer is "ask", not "choose well". *Depth:* the build.

**Calibration.** Whether stated confidence tracks actual accuracy. *Why it matters here:*
uncalibrated confidence is exactly why it fails as a trigger. *Depth:* lesson 5.5.

## The idea, before any criteria

**Three triggers, and none of them is "this is hard."**

- **They asked for a human.** Escalate now. Not after one attempt.
- **Policy is silent or ambiguous** about what they are asking. The guide's own example is
  competitor price matching where policy covers only own-site adjustments. Not a hard case
  — an *unaddressed* one.
- **No meaningful progress is possible.** Distinct from slow.

**Two things that feel like triggers and are not.** Sentiment: an annoyed person with a
simple problem and a calm one with an impossible problem both get mishandled. Self-reported
confidence: it is a word the model produces, and unless calibrated against labelled
outcomes it carries little about difficulty.

**And when the input is ambiguous, ask.** The guide is specific: multiple matches require
**clarification — requesting additional identifiers — rather than heuristic selection.**
Picking the closest match is confident and sometimes wrong, and nothing marks which.

## The build

### Step 1 — the criteria, with examples

```
ESCALATE IMMEDIATELY
  the user asks for a person          -> hand off now; no investigation first
  policy is silent on the request     -> e.g. a claim type the criteria do not cover
  no progress is possible             -> the source does not exist; access is refused

DO NOT ESCALATE ON
  frustration alone, where the issue is within capability
    -> acknowledge it, offer the resolution, escalate only if they reiterate
  the case merely being complex
  a low self-reported confidence score
```

Few-shot examples per branch, per the guide's skill — and lesson 4.2's rule applies: the
example that earns its place is the ambiguous one, the frustrated user with a solvable
problem.

### Step 2 — frustration is not a trigger, and it is not nothing

The guide's wording is careful: **acknowledge the frustration while offering resolution
when the issue is within capability, escalating only if the customer reiterates their
preference.** Both halves. Not ignoring it, and not escalating on it.

### Step 3 — ask, do not guess

```
AMBIGUOUS   "check the configuration lesson"
            three lessons mention configuration

WRONG       pick the one with the closest title
RIGHT       "Three lessons match: 3.1 hierarchy, 3.2 commands and skills,
             3.3 path-specific rules. Which, or all three?"
```

A heuristic selection is a decision the user did not make and cannot see. The ask costs one
turn.

### Step 4 — hand off properly

Escalation is only half done when you decide to escalate. Lesson 1.4 has the format: the
item, the root cause, what was tried, the recommendation, and what was **not** covered. The
receiving human has no transcript.

## Tips

Things that cost somebody an hour.

**"Let me just try one thing first" after someone asks for a human is the named wrong
answer.** It reads as diligence and it is the behaviour the guide rules out.

**Sentiment escalation misroutes in both directions.** Calm impossible cases stay with the
agent; irritated trivial ones go to a human. Both are expensive and only one is visible.

**A policy gap is not a hard case.** This is the distinction people collapse. The rules not
covering something is a reason to escalate even when the answer seems obvious — because
"seems obvious" is the agent making policy.

**Asking for a clarifying identifier is cheaper than being wrong once.** One extra turn
against an action taken on the wrong record.

**Low confidence routes; it does not trigger.** Lesson 4.6's distinction, again. Confidence
can decide *who looks at it*; it should not decide *whether to escalate*.

## The anti-pattern

From the guide's objectives:

> **Sentiment-based escalation** and **self-reported confidence scores** as proxies for
> case complexity — both named unreliable.

> **Attempting investigation before honouring an explicit request for a human.**

> **Heuristic selection among multiple matches** instead of requesting an additional
> identifier.

Exam shape: when one option escalates on how the person sounds or on a confidence number,
and another escalates on a policy gap or an explicit request, the second is the answer.

## What this lesson does not cover

- **The handoff format** — lesson 1.4, and escalation without it moves the problem rather
  than reducing it.
- **Error propagation between agents** — lesson 5.3. An error is not an escalation.
- **Confidence calibration** — lesson 5.5, which is what would make a confidence number
  mean something.
- **Human review routing at scale** — also 5.5.
- **Anything about a specific support product.** The guide's examples are customer-service
  shaped; the reasoning is not.

## Sources

Exam guide **Version 1.0, effective July 2026**, §6, TS 5.2.

| Claim | Source |
|---|---|
| Appropriate escalation triggers: customer requests for a human, policy exceptions or gaps — not just complex cases — and inability to make meaningful progress | EG §6, TS 5.2 |
| The distinction between escalating immediately when a customer explicitly demands it versus offering to resolve when the issue is straightforward | EG §6, TS 5.2 |
| Sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual case complexity | EG §6, TS 5.2 |
| Multiple customer matches require clarification — requesting additional identifiers — rather than heuristic selection | EG §6, TS 5.2 |
| Adding explicit escalation criteria with few-shot examples demonstrating when to escalate versus resolve autonomously | EG §6, TS 5.2 |
| Honouring explicit customer requests for human agents immediately without first attempting investigation | EG §6, TS 5.2 |
| Acknowledging frustration while offering resolution when the issue is within capability, escalating only if the customer reiterates their preference | EG §6, TS 5.2 |
| Escalating when policy is ambiguous or silent on the specific request, e.g. competitor price matching where policy addresses only own-site adjustments | EG §6, TS 5.2 |
| Instructing the agent to ask for additional identifiers when tool results return multiple matches rather than selecting on heuristics | EG §6, TS 5.2 |
| Structured handoff summaries for escalation to humans who lack the conversation transcript | EG §6, TS 1.4 |
